# Python Script which contains useful help functions for making transformations to target and feature dataset

#Function which sums up the number of vehicles per StartTime.
def groupby_stationid(df):
    return df[['StartTime','NumberOfVehicles']].groupby('StartTime').sum().reset_index()

#Function which takes the mean of each band per timestamp
def groupby_band(df):
    return df[['StartTime']+[x for x in df.columns if 'PL' in x]].groupby('StartTime').mean().reset_index()
