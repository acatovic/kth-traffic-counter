# Python Script which contains useful help functions for making transformations to target and feature dataset

#Function which sums up the number of vehicles per StartTime.
def groupby_stationid(df):
    return df[['StartTime','NumberOfVehicles']].groupby('StartTime').sum().reset_index()