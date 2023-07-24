"""
General processing of the prices and signals.
"""

def calc_mean(df, method, window=None):
    """
    Calculates the mean of the dataframe provided using the provided method.

    Arguments:
        df: pd.DataFrame. The mean will be calculated per column.
        method: any of None, 'rolling', 'expanding'
        window: any of None, int
    
    For 'rolling' and 'expanding' methods window must be an int.
    """

    if method == None:
        return df.mean()
    
    # We reach this part of the code if method is 'rolling' or 'expanding'. Hence, window should be an interger.
    if type(window) != int:
        print('The passed method should have a valid interger window.')
        raise ValueError(f'window is of type {type(window)}.')
    
    if method == 'rolling':
        calc = df.rolling(window=window, min_periods=1).mean()
    

    
