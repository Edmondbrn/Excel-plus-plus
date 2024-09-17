import pandas as pd
import os 
from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns
from pingouin import qqplot
from stat_python import *

os.chdir(os.path.dirname(__file__))

class plot():

    def __init__(self, pandas_table, type, xvar, yvar, col, test = None, plot_NA = False):
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
        self.Fill = None
        self.facet = None # facet of the plot (sub plot)
        self.Facet_size = 14 if self.facet is not None else None
        self.angle_X = 0 # angle for X axis
        self.angle_Y = 0 # angle for Y axis

        self.data = pandas_table # value for the pandas dataframe
        self.X_var = xvar
        self.Y_var = yvar
        self.test = test # value for teh test to perform if necessary
        self.plot_NA = plot_NA
        self.plot = None # the value to contain the plot itself

    
    def plot_data(self):
        """
        Method that creates the base plot for everything
        """
        
        geom_mapping = {
        "violin": geom_violin(),
        "box": geom_boxplot(),
        "bar": None,
        "hist": geom_histogram(binwidth=0.5),
        "scatter": geom_point(),
        "regression": geom_smooth(method="lm")
    }
        if self.type == "bar":
            self.format_bar()
            self.plot = ggplot(data=self.data_format, mapping=aes(x="group", y='mean', fill = "group"))
            self.plot += geom_bar(stat="identity")
            self.plot += geom_errorbar(aes(ymin='xmin', ymax='xmax'), color="black")
        else:
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

    def format_bar(self):
        """
        Function that transforms data and compute the import value for a barplot
        """
        self.data_format = self.data.groupby(self.X_var)[self.Y_var].agg(["mean", "median", "std"]).reset_index() # remove index column name
        self.data_format['xmin'] = self.data_format['mean'] - self.data_format['std']
        self.data_format['xmax'] = self.data_format['mean'] + self.data_format['std']
        self.data_format.rename(columns={self.X_var: 'group'}, inplace=True)

    def qqplot(self):
        """
        Method to plot the quantile-quantile plot for the noramlity check
        """
        sns.set_theme("darkgrid")
        qqplot(x = self.X_var, dist = "norm", confidence = True)
        plt.savefig("tmp/qqplot_raw.png")

    def stat_annot(self):
        """
        Function which compute statistical test and display significant or all results
        """
        self.dict_stat = {0.05 : "*", 0.01 : "* *", 0.001 : "* * *", 0.0001 : "* * * *"}
        theme_set(theme_bw()) # change background
        self.unique_x = self.data[self.X_var].unique() # get all the value in the column
        self.unique_x.sort() # organize them by alphabetical order
        self.y = 1
        for self.cpt in range(len(self.unique_x) - 1):# browse all the factor
            self.var1 = self.unique_x[self.cpt]
            for self.j in range(self.cpt +1, len(self.unique_x)): # create all the pairs if necessary
                self.var2 = self.unique_x[self.j]

                model = st.student_test(df, self.Y_var, self.X_var, var1 , var2)

                self.pvalue = model['p-val'].values[0]
                self.pvalue = self.pval_correction
                if self.pvalue < 0.05 and not self.plot_NA: # display only significant test
                    self.plot_stat
                else: # print all the test 
                    self.plot_stat                
                   

    def plot_stat(self) -> None:
        """
        Function to add * and segment for statistical annotations
        """
        self.maxi = max(max(self.data.loc[self.data[self.X_var] == self.var1, self.Y_var]), 
                        max(self.data.loc[self.data[self.X_var] == self.var2, self.Y_var]))
        
        self.plot += annotate("segment", x=self.var1, xend=self.var2, y = self.maxi + 0.15 * self.y, yend = self.maxi + 0.15 * self.y, color="black")
        self.plot += annotate("segment", x=self.var1, xend=self.var1, y = self.maxi + 0.15 * self.y - 0.01 * self.maxi, yend = self.maxi + 0.15 * self.y, color = "black")
        self.plot += annotate("segment", x=self.var2, xend=self.var2, y = self.maxi + 0.15 * self.y - 0.01 * self.maxi, yend = self.maxi + 0.15 * self.y, color = "black")
        self.plot += annotate("text")
        for threshold in sorted(self.dict_stat.keys(), reverse=False): # help to quantify the annotation for stat
            if self.pvalue < threshold:
                symbol = self.dict_stat[threshold]
                break
        self.plot += annotate("text", x=(self.cpt + 1 + self.j + 1) / 2, y = self.maxi + 0.15 * self.y + 0.02, label=symbol, ha='center', va='bottom', color="black")
        self.y += 1

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


        
















