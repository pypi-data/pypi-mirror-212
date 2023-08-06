class NaNFixer:
    """
    A class to fix missing values (NaN) in data using various strategies.

    Parameters:
        strategy (str): The strategy to use for fixing missing values. Supported strategies are 'mean',
                        'median', and 'mode'. Default is 'mean'.

    Methods:
        fix_nan(data):
            Fixes missing values in the input data using the specified strategy.

    Example usage:
        # Assuming you have a DataFrame named 'df' with missing values
        fixer = NaNFixer(strategy='mean')
        fixed_df = fixer.fix_nan(df)
    """
    def __init__(self, strategy='mean'):
        self.strategy = strategy
    
    def fix_nan(self, data):
        """
        Fixes missing values in the input data using the specified strategy.

        Parameters:
            data (pandas.DataFrame): The input data containing missing values.

        Returns:
            pandas.DataFrame: The data with missing values replaced according to the specified strategy.

        Raises:
            ValueError: If an invalid strategy is provided. Supported strategies are 'mean', 'median', and 'mode'.
        """
        if self.strategy == 'mean':
            return data.fillna(data.mean())
        elif self.strategy == 'median':
            return data.fillna(data.median())
        elif self.strategy == 'mode':
            return data.fillna(data.mode().iloc[0])
        else:
            raise ValueError('Invalid strategy. Supported strategies are: mean, median, mode.')
