import matplotlib.pyplot as plt

class DataFrameVisualizer:
    """
    A class for visualizing data in a DataFrame using various plot types.
    
    Parameters:
        dataframe (pandas.DataFrame): The input DataFrame containing the data.
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    def plot_bar(self, x_column, y_column, title=None, xlabel=None, ylabel=None):
        """
        Create and display a bar plot from the DataFrame.
        
        Parameters:
            x_column (str): The column name to use for the x-axis.
            y_column (str): The column name to use for the y-axis.
            title (str, optional): The title of the plot.
            xlabel (str, optional): The label for the x-axis.
            ylabel (str, optional): The label for the y-axis.
        """
        
        plt.figure(figsize=(10, 6))
        plt.bar(self.dataframe[x_column], self.dataframe[y_column])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90)
        plt.show()
    
    def plot_line(self, x_column, y_column, title=None, xlabel=None, ylabel=None):
        """
        Create and display a line plot from the DataFrame.
        
        Parameters:
            x_column (str): The column name to use for the x-axis.
            y_column (str): The column name to use for the y-axis.
            title (str, optional): The title of the plot.
            xlabel (str, optional): The label for the x-axis.
            ylabel (str, optional): The label for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.dataframe[x_column], self.dataframe[y_column])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90)
        plt.show()
    
    def plot_pie(self, column, title=None):
        """
        Create and display a pie chart from the DataFrame.
        
        Parameters:
            column (str): The column name to use for the pie chart.
            title (str, optional): The title of the plot.
        """
        plt.figure(figsize=(10, 6))
        plt.pie(self.dataframe[column], labels=self.dataframe.index, autopct='%1.1f%%')
        plt.title(title)
        plt.show()