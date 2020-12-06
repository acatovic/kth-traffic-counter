# Python Script which contains useful help functions for making transformations to target and feature dataset

import pandas as pd

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
    

#Function which takes the mean of each band per timestamp
def groupby_band(df,mode):
    df = df.copy()
    if mode == 'aggregate_mean':
        return df[['StartTime']+[x for x in df.columns if 'PL' in x]].groupby('StartTime').mean().reset_index()
    elif mode =='pivot_band':
        pivot_vals = [x for x in df.columns if 'PL_' in x]
        df = df.pivot_table(values=pivot_vals, index='StartTime', columns='Band',aggfunc='mean').reset_index()
        df.columns = df.columns.map('{0[0]}|{0[1]}'.format)
        df = df.rename(columns={'StartTime|':'StartTime'})
        return df
