class MyPlots:
    """
    A class for creating customized plots using seaborn.

    Attributes:
        PALETTE (str): The default color palette for the plots.
        HEIGHT (int): The default height of the plots.
        ASPECT (int): The default aspect ratio of the plots.

    Methods:
        __init__(data, xlim_low=None, xlim_high=None): Initialize the MyPlots instance.
        my_catplot(x, y, hue=None, kind='bar'): Create a categorical plot.

    Example usage:
        my_plots = MyPlots(data)
        my_plots.my_catplot('x_column', 'y_column', hue='category_column', kind='bar')
    """

    PALETTE = 'colorblind'
    HEIGHT = 4
    ASPECT = 2

    def __init__(self, data, xlim_low=None, xlim_high=None):
        """
        Initialize the MyPlots instance.

        Args:
            data: The data to be used for plotting.
            xlim_low (float or None): The lower limit for the x-axis. Default is None.
            xlim_high (float or None): The upper limit for the x-axis. Default is None.
        """
        self.data = data
        self.xlim_low = xlim_low
        self.xlim_high = xlim_high

    def my_catplot(self, x, y, hue=None, kind='bar'):
        """
        Create a categorical plot using seaborn's catplot.

        Args:
            x (str): The column name or key in the data for the x-axis.
            y (str): The column name or key in the data for the y-axis.
            hue (str or None): The column name or key in the data for grouping the data by color. Default is None.
            kind (str): The type of plot to create. Default is 'bar'.

        Returns:
            None
        """
        sns.catplot(data=self.data, x=x, y=y, hue=hue, kind=kind, palette=MyPlots.PALETTE, height=MyPlots.HEIGHT, aspect=MyPlots.ASPECT)
        plt.xlim(self.xlim_low, self.xlim_high)
        plt.show()