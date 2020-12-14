import numpy as np
import pandas as pd


def cost_hata_distance(L, f, hB, hR=1.8, Cm=0.):
    '''Calculate distance between RBS and user, assuming COST Hata RF 
    propagation model, https://en.wikipedia.org/wiki/COST_Hata_model.
    
      o L:  Median path loss in dB
      o f:  Carrier frequency/band in MHz
      o hB: RBS antenna height in meters
      o hR: Mobile station antenna height in meters
      o Cm: Constant offset in dB; 0. for suburban and 3. for metropolitan
            areas
    '''
    d = 1000 * 10 ** ((L - 46.3 - 33.9 * np.log10(f) + 13.82 * np.log10(hB) + (3.2 * (np.log10(11.75 * hR)) ** 2 - 4.97) - Cm) / (44.9 - 6.55 * np.log10(hB)))
    return d


def groupby_band(df):
    '''Group by band and sum up path loss values of cells on the same band.
    
    Assume `df` has the following columns:
    
      o StartTime: Starting date/time of 15-min sample interval, (obj)
      o Band: Carrier frequency in MHz of each cell, (int64)
      o CellId: Local cell id in LTE eNB, (int64)
      o PL_00 to PL_20: Path loss values in dB bins, (float64)
    '''
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    values = df.columns[3:]
    df = df.pivot_table(values=values, index='StartTime', columns='Band', 
                        aggfunc='sum').reset_index()
    df.columns = df.columns.map('{0[0]}|{0[1]}'.format)
    df = df.rename(columns={'StartTime|': 'StartTime'})
    
    return df


def groupby_stationid(df):
    '''Sum up vehicle counts for all sensors, for each sampling interval.
    
    Assume `df` has the following columns:
    
        o StartTime: Starting date + time of 15-min sample interval
        o StationId: Id (int64) of traffic sensor/station
        o NumberOfVehicles: 15-min aggregate vehicle count
    '''
    stations = df['StationId'].unique()
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    df = df.set_index('StartTime')
    df2 = pd.DataFrame(columns=stations)
    for station in stations:
        df2[station] = df[df['StationId'] == station]['NumberOfVehicles']
    df2.dropna(inplace=True)
    df2['NumberOfVehicles'] = df2.iloc[:, -len(stations):].sum(axis=1)
    df2 = df2.reset_index()
    
    return df2[['StartTime', 'NumberOfVehicles']]


def ts_train_test_split(X, y, train_range, test_range):
  '''Time-series train/test split, where train/test data is specified by 
  tuples consisting of start/end datetime values.
  '''
  X_train = X.loc[train_range[0]: train_range[1]]
  y_train = y.loc[train_range[0]: train_range[1]]
  X_test = X.loc[test_range[0]: test_range[1]]
  y_test = y.loc[test_range[0]: test_range[1]]
  return X_train, X_test, y_train, y_test