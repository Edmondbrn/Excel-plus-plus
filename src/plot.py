import pandas as pd
import os 
from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg

os.chdir(os.path.dirname(__file__))

class plot():

    def __init__(self, pandas_table, type, xvar, yvar, col):
        self.type = type # type of plot
        self.xlab_size = 12 # size of the x variable
        self.ylab_size = 12 # same for y
        self.Title_size = 15
        self.Legend_size = 15
        self.Title = "" # title of the plot
        self.xlab_title = "" # title of the X axis
        self.ylab_title = "" # title of the Y axis
        self.Legend = ""
        self.Color = col # color by for the plot (sub selection)
        self.facet = None # facet of the plot (sub plot)
        self.Facet_size = 14 if self.facet is not None else None
        self.angle_X = 0 # angle for X axis
        self.angle_Y = 0 # angle for Y axis

        self.data = pandas_table # value for the pandas dataframe
        self.X_var = xvar
        self.Y_var = yvar
        self.plot = None

    
    def plot_data(self):
        """
        Method that creates the base plot for everything
        """
        
        geom_mapping = {
        "violin": geom_violin(),
        "box": geom_boxplot(),
        "bar": geom_bar(stat="identity"),
        "scatter": geom_point(),
        "regression": geom_smooth(method="lm")
    }
        # Ajoutez l'esthétique color dans le mapping global de ggplot
        self.plot = ggplot(data=self.data, mapping=aes(x=self.X_var, y=self.Y_var, color=self.Color))
        self.plot += geom_mapping.get(self.type, "Error with the plot type. Please check your input.")

        self.plot += theme(
            axis_text_x=element_text(size=self.xlab_size, angle=self.angle_X),
            axis_text_y=element_text(size=self.ylab_size, angle=self.angle_Y),
            axis_title=element_text(size=self.Title_size),
            plot_title=element_text(size=self.Title_size, ha='center'),  # Adjust title size and position
            strip_text=element_text(size=self.Facet_size)
        )

        self.plot += labs(
            title=self.Title,
            x=self.xlab_title,
            y=self.ylab_title
        )
        
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        self.plot.save("tmp/plot_raw.png")
        return self.plot
    

    def qqplot(self):
        """
        Method to plot the quantile-quantile plot for the noramlity check
        """
        sns.set_theme("darkgrid")
        pg.qqplot(x = self.X_var, dist = "norm", confidence = True)
        plt.savefig("tmp/qqplot_raw.png")


    # # setters
    # def setType(self, value):
    #     self.type = value
    
    # def setSize_X(self, value):
    #     self.size_X = value
    
    # def setSize_Y(self, value):
    #     self.size_Y = value
    
    # def setTitle(self, value):
    #     self.title = value
    
    # def setXlab(self, value):
    #     self.xlab = value

    # def setYlab(self, value):
    #     self.ylab = value

    # def setColor(self, value):
    #     self.color = value

    # def setFacet(self, value):
    #     self.facet = value

    # def setAngle_X(self, value):
    #     self.angle_X = value

    # def setAngle_Y(self, value):
    #     self.angle_Y = value

    # def setX_var(self, value):
    #     self.X_var = value

    # def setY_var(self, value):
    #     self.Y_var = value

    # def setFacet_size(self, value):
    #     self.facet_size = value

    # def setLegend(self, value):
    #     self.legend = value


        
















