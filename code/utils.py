# Python Script which contains useful help functions for making transformations to target and feature dataset

#Function which sums up the number of vehicles per StartTime.
def groupby_stationid(df):
    return df[['StartTime','NumberOfVehicles']].groupby('StartTime').sum().reset_index()

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
