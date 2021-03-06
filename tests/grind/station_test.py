#!/usr/bin/env python

# stdlib modules
import sys
import os.path
import pickle

# third party modules
import numpy as np

homedir = os.path.dirname(os.path.abspath(__file__))  # where is this script?
shakedir = os.path.abspath(os.path.join(homedir, '..', '..'))
sys.path.insert(0, shakedir)

# local imports
from shakelib.grind.station import StationList

#
# Set SAVE to True to write new versions of the output to disk,
# set it to False to actually run the tests.
#
SAVE = False


def test_station():

    homedir = os.path.dirname(os.path.abspath(__file__))

    #
    # First test the Calexico data on its own
    #
    event = 'Calexico'

    datadir = os.path.abspath(os.path.join(homedir, 'station_data'))
    datadir = os.path.abspath(os.path.join(datadir, event, 'input'))

    inputfile = os.path.join(datadir, 'stationlist_dat.xml')
    dyfifile = os.path.join(datadir, 'ciim3_dat.xml')
    xmlfiles = [inputfile, dyfifile]

    stations = StationList.loadFromXML(xmlfiles, ":memory:")

    df1 = stations.getStationDataframe(1)
    df2 = stations.getStationDataframe(0)

    ppath = os.path.abspath(os.path.join(datadir, '..', 'database',
                                         'test1.pickle'))
    if SAVE:
        ldf = [df1, df2]
        with open(ppath, 'wb') as f:
            pickle.dump(ldf, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(ppath, 'rb') as f:
            ldf = pickle.load(f)

        saved_df1 = ldf[0]
        saved_df2 = ldf[1]

        compare_dataframes(saved_df1, df1)
        compare_dataframes(saved_df2, df2)

    #
    # Should at least hit this code
    #
    imtlist = stations.getIMTtypes()
    assert 'PGA' in imtlist
    assert 'PGV' in imtlist

    #
    # Add the Northridge data to the Calexico data
    #
    event = 'northridge'
    datadir = os.path.abspath(os.path.join(homedir, 'station_data'))
    datadir = os.path.abspath(os.path.join(datadir, event, 'input'))

    inputfile = os.path.join(datadir, 'hist_dat.xml')
    dyfifile = os.path.join(datadir, 'dyfi_dat.xml')
    xmlfiles = [inputfile, dyfifile]

    stations = stations.addData(xmlfiles)

    df1 = stations.getStationDataframe(1)
    df2 = stations.getStationDataframe(0)

    ppath = os.path.abspath(os.path.join(datadir, '..', 'database',
                                         'test2.pickle'))
    if SAVE:
        ldf = [df1, df2]
        with open(ppath, 'wb') as f:
            pickle.dump(ldf, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(ppath, 'rb') as f:
            ldf = pickle.load(f)

        saved_df1 = ldf[0]
        saved_df2 = ldf[1]

        compare_dataframes(saved_df1, df1)
        compare_dataframes(saved_df2, df2)


def test_station2():

    homedir = os.path.dirname(os.path.abspath(__file__))

    event = 'wenchuan'

    datadir = os.path.abspath(os.path.join(homedir, 'station_data'))
    datadir = os.path.abspath(os.path.join(datadir, event, 'input'))

    inputfile = os.path.join(datadir, 'stationlist.xml')
    xmlfiles = [inputfile]

    stations = StationList.loadFromXML(xmlfiles, ":memory:")

    df1 = stations.getStationDataframe(1)
    df2 = stations.getStationDataframe(0)

    ppath = os.path.abspath(os.path.join(datadir, '..', 'database',
                                         'test3.pickle'))
    if SAVE:
        ldf = [df1, df2]
        with open(ppath, 'wb') as f:
            pickle.dump(ldf, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(ppath, 'rb') as f:
            ldf = pickle.load(f)

        saved_df1 = ldf[0]
        saved_df2 = ldf[1]

        compare_dataframes(saved_df1, df1)
        compare_dataframes(saved_df2, df2)

        sql = stations.dumpToSQL()

        stations2 = StationList.loadFromSQL(sql)

        df1 = stations2.getStationDataframe(1)
        df2 = stations2.getStationDataframe(0)

        compare_dataframes(saved_df1, df1)
        compare_dataframes(saved_df2, df2)


def compare_dataframes(df1, df2):

    assert sorted(list(df1.keys())) == sorted(list(df2.keys()))

    idx1 = np.argsort(df1['id'])
    idx2 = np.argsort(df2['id'])

    for key in df1.keys():
        if df1[key].dtype == np.float:
            assert np.allclose(df1[key][idx1], df2[key][idx2], equal_nan=True)
        else:
            assert (df1[key][idx1] == df2[key][idx2]).all()


if __name__ == '__main__':
    test_station()
    test_station2()
