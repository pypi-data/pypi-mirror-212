"""lkcom - a Python library of useful routines.

This module contains data input and output utilities.

Copyright 2015-2023 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import os
import pathlib
import io
import zipfile
import glob
from pathlib import Path
import json
import time
import datetime
import h5py

import numpy as np

from lkcom.util import isarray
from lkcom.string import check_lstr_in_str, strip_whitespace, strip_nonnum


def get_file_sz(FileName):
    return os.path.getsize(FileName)


def get_file_creation_date(file_name):
    if file_name:
        return os.path.getctime(file_name)


def get_file_creation_date_str(file_name):
    date = get_file_creation_date(file_name)
    if date:
        return time.strftime("%Y-%m-%d", time.gmtime(date))


def get_file_mod_date(file_name):
    if file_name:
        return os.path.getmtime(file_name)


def get_file_mod_date_str(file_name):
    date = get_file_mod_date(file_name)
    if date:
        return time.strftime("%Y-%m-%d", time.gmtime(date))


def get_file_timestamp_str(file_name, format='%Y-%m-%d', parent_file_ext=None):
    """Get file time stamp string based on OS creation date.

    The parent_file_ext argument can be used to check whether the parent
    directory contains an h5 or zip file from which the data file could have
    been produced later and thus would have an incorrect creation timestamp.
    """
    data_file_name = file_name
    if parent_file_ext:
        parent_file_names = list_files_with_extension(get_parent_dir(file_name), parent_file_ext)
        if len(parent_file_names == 1):
            print("Using parent file timestamp")
            data_file_name = parent_file_names[0]
        elif len(parent_file_names > 1):
            print("WARNING: Multiple parent files found in the parent directory, using the first one")
            data_file_name = parent_file_names[0]

    return get_file_creation_date_str(data_file_name)



def parse_csv_header(file_name, key):
    """Find a value for a given key in the header of a CSV file.

    The expected CSV file format is:
    # Comments, key1: value1, key2: value2, ...
    # Var1 (Unit1), Var2 (Unit2)
    [Data]

    """
    with open(file_name) as file_h:
        for line in file_h:
            if line[0] != '#':
                break
            if line.find(key) != -1:
                return line.split(key)[1].split(',')[0]


def read_json(file_name_arg):
    """Read a JSON file.

    If 'file_name_arg' is a single file name the file is parsed as json and an
    exception is raised if hat fails. If 'file_name_arg' is a list list of file
    names the files are read until one of them is successfully parsed as a
    JSON.
    """
    if isarray(file_name_arg):
        for file_name in file_name_arg:
            if check_file_exists(file_name):
                return json.load(open(file_name))
        return None
    else:
        file_name = file_name_arg
        return json.load(open(file_name))


def json_multiget(data, key_arg, default_val=None):
    """Get a JSON value from multiple keys."""
    if isarray(key_arg):
        for key in key_arg:
            val = data.get(key)
            if val:
                return val
        return default_val
    else:
        return data.get(key_arg, default_val)


def list_zi_h5_traces(file_name=None):
    """List traces in a Zurich Instruments H5 file."""
    file_name = get_zi_h5_file_name(file_name)

    data_file = h5py.File(file_name, 'r')
    keys = list(data_file.keys())
    data_names = []
    print("Data file '{:s}' contents: ".format(Path(file_name).stem))
    for key_ind, key in enumerate(keys):
        header_names = data_file.get(
            key + '/dev1940/demods/0/sample/chunkheader')[()].dtype.names
        name_ind = [ind for ind, name in enumerate(header_names)
                    if name == 'name'][0]
        data_name = data_file.get(
            key + '/dev1940/demods/0/sample/chunkheader')[0][name_ind].decode()
        print(key_ind, data_name)
        data_names.append(data_name)

    return data_names


def get_zi_h5_file_name(file_name=None, fail_on_no_file=True):
    """Find a Zurich Instruments .h5 file in the current dir."""
    if file_name is None:
        file_names = list_files_with_extension('.', ext='h5')
        if len(file_names) == 0:
            raise ValueError("No .h5 files found")
        elif len(file_names) == 1:
            file_name = file_names[0]
        else:
            print("Multiple .h5 file founds, this program only supports a "
                  "single file per folder")
            file_name = file_names[0]

    if fail_on_no_file and not file_name:
        raise ValueError("No file name given")

    return file_name


def get_zi_h5_trace(file_name=None, trace_name=None, trace_index=None):
    """Get trace data from a Zurich Instruments .h5 file"""
    file_name = get_zi_h5_file_name(file_name)
    data_file = h5py.File(file_name, 'r')
    keys = list(data_file.keys())

    data_names = list_zi_h5_traces(file_name)

    if not trace_index:
        for ind, data_name in enumerate(data_names):
            if data_name == trace_name:
                trace_index = ind
                break

        if trace_index is None:
            raise RuntimeError("Trace '{:}' not found".format(trace_name))

    key = keys[trace_index]

    farr = np.array(data_file.get(key + '/dev1940/demods/0/sample/frequency'))
    varr = np.array(data_file.get(key + '/dev1940/demods/0/sample/r'))
    parr_dbm = 10*np.log10(varr**2/50*1E3)
    rbwarr = np.array(data_file.get('000/dev1940/demods/0/sample/bandwidth'))
    if (np.diff(rbwarr[np.logical_not(np.isnan(rbwarr))]) != 0).any():
        print("WARNING: data has variable bandwidth")

    return {'farr': farr, 'parr_dbm': parr_dbm, 'varr': varr,
            'rbw': np.mean(rbwarr), 'rbwarr': rbwarr}


def extract_zi_h5_traces(file_name=None):
    """Extract traces from Zurich Instruments H5 files"""
    file_name = get_zi_h5_file_name(file_name)

    data_file = h5py.File(file_name, 'r')
    keys = list(data_file.keys())

    data_names = list_zi_h5_traces(file_name)

    for key_ind, key in enumerate(keys):
        data_name = data_names[key_ind]
        print("Exporting " + data_name)
        farr = np.array(data_file.get(
            key + '/dev1940/demods/0/sample/frequency'))
        varr = np.array(data_file.get(
            key + '/dev1940/demods/0/sample/r'))
        parr_dbm = 10*np.log10(varr**2/50*1E3)
        bw = np.array(data_file.get(key+ '/dev1940/demods/0/sample/bandwidth'))
        parr_dbmhz = parr_dbm - 10*np.log10(bw)
        if (np.diff(bw[np.logical_not(np.isnan(bw))]) != 0).any():
            print("WARNING: data has variable bandwidth")
            bw_str = '{:.0f} - {:.0f} Hz'.format(np.nanmin(bw), np.nanmax(bw))
        else:
            bw_str = '{:.0f}'.format(np.nanmean(bw))
        file_name = '{:d}_{:s}.dat'.format(
            key_ind, data_name.replace(':', '_'))
        header_str = \
            'HF2LI sweeper data, index: {:d}, name: {:s}, bw: {:s}'.format(
                key_ind, data_name, bw_str)

        header_str += '\nFrequency (Hz), Amplitude (dBm), PSD (dBm/Hz)'
        np.savetxt(file_name, np.transpose([farr, parr_dbm, parr_dbmhz]), delimiter=',',
                   header=header_str)

    print("\nAll done.")
    input("Press any key to continue...")


def check_file_exists(file_path):
    """Check if a file exists."""
    try:
        return os.path.isfile(file_path)
    except FileNotFoundError:
        return False


def read_tek_csv(FileName):
    """Read Tektronix CSV file."""
    return np.loadtxt(FileName, skiprows=21, delimiter=',')


def read_bin_file(file_name):
    """Read a serialized 3D array.

    Read a binary file containting a serialized 3D array of uint32 values. The
    first three words of the array are the original 3D array dimmensions.

    Btw, this is the default way that LabVIEW writes binary data.
    """
    if Path(file_name).suffix == '.zip':
        # Look for DAT files inside the ZIP archive
        zip_contents = zipfile.ZipFile(file_name).namelist()
        for zip_file_name in zip_contents:
            if Path(zip_file_name).suffix == '.dat':
                # Seems like numpy cannot read binary data from a ZIP file
                # using fromfile() if the file handle is provided using
                # zipfile. This is due to the fact that fromfile() relies on
                # fileno which is not provided by the zipfile.ZipFile object.
                # A workaround is to use ZipFile.read() to read the raw byte
                # array from the ZIP archive and then frombuffer to parse the
                # byte array into a numpy array.
                serdata = np.frombuffer(
                    zipfile.ZipFile(file_name).read(zip_file_name),
                    dtype='uint32')
                break
    else:
        serdata = np.fromfile(file_name, dtype='uint32')

    serdata = serdata.newbyteorder()

    num_pages = serdata[0]
    num_rows = serdata[1]
    num_col = serdata[2]
    page_sz = num_rows*num_col

    serdata = serdata[3:]

    data = np.ndarray([num_rows, num_col, num_pages], dtype='uint32')

    for ind_pg in range(num_pages):
        data[:, :, ind_pg] = np.reshape(
            serdata[ind_pg*page_sz:(ind_pg+1)*page_sz], [num_rows, num_col])

    return data


def list_files_with_extension(
        path=None, ext="dat", recursive_dir_search=False,
        name_exclude_filter=None, name_include_filter=None):
    """List files that have a specific extension."""

    if isinstance(ext, list):
        file_list = []
        for ext1 in ext:
            file_list += list_files_with_extension(
                path=path, ext=ext1, name_exclude_filter=name_exclude_filter,
                name_include_filter=name_include_filter)
        return file_list

    if ext[0] == '.':
        print("Specify extension as 'txt', do not include the dot")

    if path is None:
        path = '.\\'

    if not check_dir_exists(path):
        print("Directory does not exist")
        return None

    if recursive_dir_search:
        List = []
        for root, subdirs, files in os.walk(path):
            List += [Path(root) / Path(file_name) for file_name in files]
    else:
        List = [Path(entry) for entry in os.listdir(path)]

    Paths = []

    for FileName in List:
        filter_hit = False
        if name_exclude_filter:
            if isarray(name_exclude_filter):
                for name_exclude_filter1 in name_exclude_filter:
                    if(str(FileName).find(name_exclude_filter1) != -1):
                        filter_hit = True
                        break
            else:
                if(str(FileName).find(name_exclude_filter1) != -1):
                    filter_hit = True
                    break

        if name_include_filter:
            if(str(FileName).lower().find(name_include_filter.lower()) == -1):
                filter_hit = True
                continue

        if not filter_hit and FileName.suffix[1:] == ext:
            Paths.append(str(Path(path) / FileName))

    return Paths


def list_files_with_filter(filter_str="*"):
    return glob.glob(filter_str)


def list_dirs(path):
    dir_names = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                dir_names.append(entry.name)

    return dir_names


def list_files_by_pattern(path, match_pattern=None, excl_pattern=None,
                          with_path=False):
    """List files that include a given pattern.

    List file names in the given path that conntain all strings in the pattern
    list.
    """
    file_names = os.listdir(path)
    matched_file_names = []
    for file_name in file_names:
        if match_pattern:
            match_result = check_lstr_in_str(file_name, match_pattern)
        else:
            match_result = [False]
        if excl_pattern:
            excl_result = [not elem for elem in
                           check_lstr_in_str(file_name, excl_pattern)]
        else:
            excl_result = [True]
        if all(elem is True for elem in match_result) \
                and all(elem is True for elem in excl_result):
            matched_file_names.append(file_name)

    if with_path:
        return [Path(path).joinpath(Path(file_name)) for
                file_name in matched_file_names]
    else:
        return matched_file_names


def check_file_exists(file_path):
    """Check if a file exists."""
    try:
        return os.path.isfile(file_path)
    except FileNotFoundError:
        return False


def check_dir_exists(dir_path):
    """Check if a directory exists."""
    try:
        return os.path.isdir(dir_path)
    except FileNotFoundError:
        return False


def get_parent_dir(file_name):
    """Get the absolute path to the parent directory of a file"""
    return Path(file_name).parent.absolute()


def open_csv_file(file_name, archive_file_name=None):
    """Open a CSV file with ZIP archive support.

    Open a CSV file which can reside in a ZIP archive.
    """
    if archive_file_name:
        archive = zipfile.ZipFile(archive_file_name, mode='r')
        file = io.BufferedReader(
            archive.open(file_name, mode='r'))
    else:
        file = open(file_name)

    return file


def read_big_file(FileName, max_row=None):
    f_sz = get_file_sz(FileName)

    fin = open(FileName, 'r')
    line = ' '
    ind = 0
    try:
        while(1):
            line = fin.readline()

            if(line == ''):
                break

            l_data = line.split('\t')

            if(ind == 0):
                l_sz = len(line)
                num_row = int(np.ceil(f_sz/l_sz))
                f_num_row = num_row
                if max_row is not None and num_row > max_row:
                    num_row = max_row
                num_col = len(l_data)

                D = np.ndarray([num_row, num_col])

            for indC in range(0, num_col):
                D[ind, indC] = float(l_data[indC])

            ind = ind + 1

            if ind % 1E5 == 0:
                print("{:d}k lines read, {:.3f} of chunk, {:.3f} "
                      "of file".format(ind/1E3, ind/num_row, ind/f_num_row))

            if max_row is not None and ind >= max_row:
                break
    except Exception:
        print("Error while reading")

    fin.close()

    return np.resize(D, [ind, num_col])


def read_starlab_file(FileName, max_row=None):
    """Read a text log file produced by StarLab.

    StarLab logs data with second timestamps. Times are converted to hours to
    match PowerMeter data.
    """
    f_sz = get_file_sz(FileName)

    fin = open(FileName, 'r')
    line = ''
    ind = 0
    try:
        with open(FileName) as fin:
            for line in fin:
                if line == '' or line[0] == ';' or line[0] == '!' \
                        or line == '\n':
                    continue

                if line.find('Timestamp') != -1:
                    continue

                l_data = [val_str.strip() for val_str in line.split('\t')]

                if ind == 0:
                    l_sz = len(line)
                    num_row = int(np.ceil(f_sz/l_sz))
                    f_num_row = num_row
                    if max_row is not None and num_row > max_row:
                        num_row = max_row
                    num_col = len(l_data)

                    D = np.ndarray([num_row, num_col])

                if len(l_data) < num_col:
                    print("Line {:d} is truncated, skipping".format(ind))
                    continue

                for indC in range(0, num_col):
                    try:
                        D[ind, indC] = float(l_data[indC])
                    except ValueError:
                        D[ind, indC] = np.nan

                ind = ind + 1

                if ind % 1E5 == 0:
                    print("{:d}k lines read, {:.3f} of chunk, {:.3f} of "
                          "file".format(ind/1E3, ind/num_row, ind/f_num_row))

                if max_row is not None and ind >= max_row:
                    break

    except Exception as excpt:
        print("Error while reading file at ind {:d}: {:}".format(ind, excpt))

    fin.close()

    D = np.resize(D, [ind, num_col])

    data = dict()
    for ind in range(num_col - 2):
        vals = D[:, ind+1]
        mask = np.logical_not(np.isnan(vals))

        # StarLab data is in seconds, convert to hours as PowerMeter
        data['tarr{:d}'.format(ind)] = D[mask, 0]/60/60

        data['vals{:d}'.format(ind)] = vals[mask]

    return data


def read_text_sa_file(file_name):
    """Read a generic text file containing spectrum analyzer data."""
    data = np.loadtxt(file_name, delimiter=',')

    rbw = None
    attn = None
    with open(file_name) as file_h:
        for line in file_h:
            if line[0] != '#':
                break
            if line.find('bw:') != -1:
                rbw_str = line.split('bw: ')[1].split(',')[0]
                if rbw_str.find('-') != -1:
                    rbw = 'variable'
                else:
                    rbw = float(line.split('bw: ')[1].split(',')[0])

    cfg = {'RBW': rbw, 'Attenuation': attn}

    return data, cfg


def read_rigol_sa_csv(file_name):
    with open(file_name) as f:
        cfg = {}
        for line in f:
            if line.find('DATA,') >= 0:
                break
            param, val = line.split(',')
            val = strip_whitespace(val)
            if len(strip_nonnum(val)) > 0:
                if val.find('.') >= 0 or val.find('e') > 0:
                    cfg[param] = float(val)
                else:
                    cfg[param] = int(val)
    return [np.loadtxt(file_name, skiprows=32, delimiter=','), cfg]


def read_power_meter_data(file_name=None):
    """Read PowerMeter data with timestamps."""
    if file_name is None:
        file_name = list_files_with_extension(
            ext='dat', name_include_filter='powerData')[0]

    print("Loading PowerMeter data from {:}...".format(file_name))
    pwr_log_data = np.loadtxt(
        file_name, skiprows=2, delimiter='\t', usecols=[0, 3])

    pwr_log = dict()
    pwr_log['t0'] = datetime.datetime.strptime(
        str(np.loadtxt(
            file_name, delimiter='\t',
            skiprows=2, usecols=2, max_rows=1, dtype='str')),
        "%y%m%d %H:%M:%S.%f")

    pwr_log['tarr'] = pwr_log_data[:, 0]
    pwr_log['vals'] = pwr_log_data[:, 1]

    return pwr_log


def read_pharos_log(file_name=None):
    """Read sensor data from PHAROS log files.

    Currently only temperature and humidity sensors are supported.
    """
    log_data = np.loadtxt(
        file_name, delimiter='\t',
        dtype={'names': ('hours', 'timestamp', 'val'),
               'formats': ('float', datetime.datetime, 'float')})

    if file_name.find('temp') != -1:
        file_name_fmt = "Ambient temperature %Y-%m-%d %H-%M.dat"
    elif file_name.find('humidity') != -1:
        file_name_fmt = "Ambient humidity %Y-%m-%d %H-%M.dat"
    else:
        print("Can't determine sensor type from file name")
        return None

    # PHAROS1 log files do not have datestamps, only hours. File names contain
    # the full timestamp or approximately the last datapoint. Therefore,
    # timestamps for all datapoints can be restored by counting back from the
    # last datapoint.

    # Full timestamp of the last datapoint from file name
    ts1 = datetime.datetime.strptime(file_name, file_name_fmt)

    # Timestamp of the last datapoint from the data log, without the date
    ts2 = datetime.datetime.strptime(log_data[-1][1], "%H:%M:%S.%f")

    # Replace the year month and day of the data log timestamp with the one
    # from the file name
    ts2 = ts2.replace(year=ts1.year, month=ts1.month, day=ts1.day)

    log = dict()
    log['t0'] = ts2 - datetime.timedelta(seconds=log_data[-1][0])
    log['tarr'] = np.array([entry[0]/60/60 for entry in log_data])
    log['vals'] = np.array([entry[2] for entry in log_data])

    return log


def read_ezlog(file_name):
    """Read temperature and RH data from EZ logger CSV file."""
    log_data = np.loadtxt(
        file_name, skiprows=11, delimiter=',', usecols=[1, 2, 3],
        dtype={'names': ('date', 'temp', 'rh'),
               'formats': (datetime.datetime, 'float', 'float')})

    log = dict()
    log['t0'] = datetime.datetime.strptime(log_data[0][0], "%Y/%m/%d %H:%M:%S")

    log['tarr'] = [(datetime.datetime.strptime(entry[0], "%Y/%m/%d %H:%M:%S") -
                   log['t0']).total_seconds()/60/60 for entry in log_data]
    log['temp'] = [entry[1] for entry in log_data]
    log['rh'] = [entry[2] for entry in log_data]
    return log


def read_beam_steering_log(dir_list=None):
    """Read T4 beam steering positioning log."""
    signal_names = [
        'A Motor X', 'A Motor Y', 'B Motor X', 'B Motor Y',
        'A Measured X', 'A Measured Y', 'B Measured X', 'B Measured Y',
        'A FeedbackState', 'B FeedbackState', 'A Total Power', 'B Total Power']
    pos_log = [dict() for signal in signal_names]

    for ind, signal in enumerate(signal_names):
        pos_log[ind]['tarr'] = np.array([])
        pos_log[ind]['val'] = np.array([])
        pos_log[ind]['signal_names'] = signal_names

    if not dir_list:
        for dir_name_month in list_dirs('positioning'):
            for dir_name_day in list_dirs('positioning/' + dir_name_month):
                dir_list = 'positioning/' + dir_name_month + '/' + dir_name_day

    for dir in dir_list:
        for ind, signal in enumerate(signal_names):
            file_name = dir + '/{:s}.txt'.format(signal)
            if not check_file_exists(file_name):
                print("File '{:}' not found, skipping signal".format(file_name))
                continue
            print("Reading file ", file_name)
            try:
                if Path(Path(file_name).parts[0]).suffix == '.zip':
                    zip_file_name = Path(Path(file_name).parts[0])
                    archive = zipfile.ZipFile(zip_file_name, mode='r')
                    file = io.BufferedReader(
                        archive.open(Path(
                            *Path(file_name).parts[1:]).as_posix(), mode='r'))
                else:
                    file = open(file_name)

                pos_log_data = np.loadtxt(
                    file, delimiter=',', usecols=[0, 2],
                    dtype={'names': ('date', 'pos'),
                           'formats': (datetime.datetime, 'float')})

                if pos_log[ind].get('t0') is None:
                    pos_log[ind]['t0'] = datetime.datetime.strptime(
                        pos_log_data[0][0], "%Y-%m-%d %H:%M:%S.%f")

                pos_log[ind]['tarr'] = np.append(
                    pos_log[ind]['tarr'],
                    np.array([(datetime.datetime.strptime(entry[0],
                              "%Y-%m-%d %H:%M:%S.%f")
                               - pos_log[ind]['t0']).total_seconds()/60/60
                              for entry in pos_log_data]))

                pos_log[ind]['val'] = np.append(
                    pos_log[ind]['val'],
                    np.array([entry[1] for entry in pos_log_data]))

            except ValueError as excpt:
                print("Failed to read log file with exception", excpt)
                print("Retrying line-by-line")
                if Path(Path(file_name).parts[0]).suffix == '.zip':
                    file = io.BufferedReader(
                        archive.open(Path(
                            *Path(file_name).parts[1:]).as_posix(), mode='r'))
                else:
                    file = open(file_name)

                for line in file:
                    if isinstance(line, bytes):
                        line = line.decode('utf-8')
                    col_data = line.split(',')

                    # Make sure there are exacly three columns in the line
                    if len(col_data) != 3:
                        continue

                    # Parse the timestamp and do some sanity checks
                    try:
                        data_ts = datetime.datetime.strptime(
                            col_data[0], "%Y-%m-%d %H:%M:%S.%f")
                        if data_ts.year < 1990 or data_ts.year > 2100:
                            continue

                        data_val = float(col_data[2])
                        if np.abs(data_val) > 1000:
                            continue
                    except Exception:
                        continue

                    if pos_log[ind].get('t0') is None:
                        pos_log[ind]['t0'] = data_ts

                    pos_log[ind]['tarr'] = np.append(
                        pos_log[ind]['tarr'],
                        float((data_ts -
                               pos_log[ind]['t0']).total_seconds()/60/60))

                    pos_log[ind]['val'] = np.append(
                        pos_log[ind]['val'],
                        data_val)

    return pos_log


def read_powerscanner_tsv(file_name=None, ):
    """Read a PowerScanner TSV file.

    The file contains tab-separated values. The header is three rows, likely
    alwayws, but may be different if the data is unnamed.

    The columns are wavelength in nm, transmission in % for s and p
    polarization and background in counts. When transmission is in %, the
    background column is likely unuseable.
    """
    try:
        with open(file_name) as data_file:
            header = data_file.readline()

        col_names = [col_name.lower() for col_name in header.split('\t')]

        data_keys = {'wavl', 'trans_s', 'trans_p'}
        data_col_names = {'wavl': 'wavelength', 'trans_s': 'transmittance(s)', 'trans_p': 'transmittance(p)'}
        data_fac = {'wavl': 1, 'trans_s': 1E-2, 'trans_p': 1E-2}

        # File column to data key mapping
        data_col_inds = dict([(data_key, None) for data_key in data_keys])

        for ind, file_col_name in enumerate(col_names):
            for data_key in data_col_names.keys():
                if file_col_name == data_col_names[data_key]:
                    data_col_inds[data_key] = ind

        if data_col_inds['wavl'] is None:
            raise Exception("Could not find wavelength column")

        if data_col_inds['trans_s'] is None and data_col_inds['trans_p']:
            raise Exception("Could not find transmission columns")

        filter_data = np.loadtxt(file_name, skiprows=3, delimiter='\t')

        # Output data dict
        data = dict([(data_key, None) for data_key in data_keys])

        for data_key in data_col_inds.keys():
            data[data_key] = filter_data[:, data_col_inds[data_key]]*data_fac[data_key]

        return data
    except Exception as excpt:
        if isinstance(excpt, OSError) and excpt.errno == 9:
            print("Cannot open data file due to OSError 9. If the file is on OneDrive, it is likely the file is not synched to the local computer. ")
        else:
            print("A general exception occurred while reading the data file")

        raise excpt


def float_loc_parser(str):
    """Localized float parser to handle comma decimal separation."""
    return float(str.decode('utf8').replace(',', '.'))


def read_rdisp_temporal_envelope(file_name):
    """Read RDisp temporal envelope."""

    fid = open(file_name)
    fid.readline()
    data = None
    data_cols = None
    for line in fid:
        data_row = line.split(',')
        if data_cols:
            for ind, val in enumerate(data_row):
                if val:
                    data_cols[ind].append(float(val))
        else:
            data_cols = [[float(val)] for val in data_row]

    col_names = 'tarr_tl', 'ampl_tl', 'tarr', 'ampl'
    data = {}
    for ind, col_name in enumerate(col_names):
        data[col_name] = np.array(data_cols[ind])

    if np.all(data['tarr_tl'] == 0):
        data['tarr_tl'] = np.linspace(-1000, 1000, len(data['tarr_tl']))
        print("WARNING: CSV file contains no time values, assuming -1 ps to 1 ps")

    if np.all(data['tarr'] == 0):
        data['tarr'] = np.linspace(-1000, 1000, len(data['tarr']))
        print("WARNING: CSV file contains no time values, assuming -1 ps to 1 ps")

    return data




def read_frog_temporal_envelope(dir_name):
    """Read FROG retrieval temporal envelope."""
    if check_dir_exists(dir_name):
        file_name = list_files_with_extension(
            dir_name, ext='dat', name_include_filter='Ek')[0]
    elif check_file_exists(dir_name):
        file_name = dir_name

    data = np.loadtxt(file_name)

    return {'tarr': data[:, 0], 'ampl': data[:, 1]}


def read_d_scan_spectrum(dir_name):
    """Read spectrum from a Sphere Photonics d-scan retrieval."""
    file_name = list_files_with_extension(dir_name, ext='txt', name_include_filter='spectrum')[0]

    data = np.loadtxt(file_name, converters={0: float_loc_parser, 1:float_loc_parser, 2:float_loc_parser, 3:float_loc_parser}, skiprows=1)

    return {'wavl': data[:, 0], 'spec': data[:, 1], 'spec_ret': data[:, 2], 'spec_phase': data[:, 3]}


def read_d_scan_temporal_envelope(dir_name):
    """Read temporal envelope from a Sphere Photonics d-scan retrieval."""
    file_name = list_files_with_extension(dir_name, ext='txt', name_include_filter='retrieved_pulse')[0]

    data = np.loadtxt(file_name, converters={0: float_loc_parser, 1:float_loc_parser, 2:float_loc_parser}, skiprows=1)

    return {'tarr': data[:, 0], 'ampl_ds': data[:, 1], 'ampl_tl': data[:, 2]}


def parse_data_setup_json(data_file_name):
    """Read a setup.json file if it exists."""
    setup_file_path = pathlib.Path(data_file_name).absolute().parent / 'setup.json'
    if check_file_exists(setup_file_path):
        print("Parsing " + setup_file_path.name)
        return json.load(open(setup_file_path))
    else:
        print("Data file has no setup.json")
        return {}
