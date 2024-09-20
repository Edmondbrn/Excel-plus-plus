import pandas as pd
import os 
from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns
from pingouin import qqplot
from stat_python import *

os.chdir(os.path.dirname(__file__))

class plot():

    def __init__(self, pandas_table, type, xvar, yvar, col, zvar : str = None, test = None, plot_NA = False):
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
        self.Z_var = zvar

        self.cat1_content = None # value for student / wilcoxon / anova / kruskall tests
        self.cat2_content = None
        self.paired = None
        self.alternative = None
        self.correction_method = None
        self.correlation_method = None
        self.regression_type = None

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
        self.maxi = 0
        self.choose_stat_function() # compute the p values
        if len(self.model) > 1 :
            print(self.model[0].columns)
            print(self.model)
            if self.model[0]["p-unc"].values[0] > 0.05:
                return
            else:
                self.model = self.model[1]
        for self.cpt in range(len(self.unique_x) - 1):# browse all the factor
            self.var1 = self.unique_x[self.cpt]
            for self.j in range(self.cpt +1, len(self.unique_x)): # create all the pairs if necessary
                self.var2 = self.unique_x[self.j]
                try:
                    self.pvalue = self.model.loc[self.var1, self.var2]
                except:
                    self.pvalue = self.model["p-val"].values[0]
            
                if self.pvalue < 0.05 and not self.plot_NA: # display only significant test
                    self.plot_stat()
                # else: # print all the test 
                    # self.plot_stat()                
                   
    def choose_stat_function(self):
        """
        Method which performs the statistic test
        """
        self.check_var_type()
        self.numeric = self.variable_types["numerical"]
        self.categorical = self.variable_types["categorical"]
        if self.test == "ttest":
            self.model = student_test(self.data, self.numeric[0], self.categorical[0], self.cat1_content, self.cat2_content, self.paired, self.alternative)
        elif self.test == "wilcox":
            self.model = wilcox_test(self.data, self.numeric[0], self.categorical[0], self.cat1_content, self.cat2_content, self.paired, self.alternative)
        elif self.test == "fisher" :
            self.model = fisher(self.data, self.categorical[0], self.categorical[1], self.alternative)
        elif self.test == "chi2":
            self.model = chi2(self.data, self.categorical[0], self.categorical[1], self.paired)
        elif self.test == "kruskall":
            self.model = kruskall(self.data, self.numeric[0], self.categorical[0], self.correction_method)
            print("test")
        elif self.test == "anova":
            self.model = anova(self.data, self.numeric[0], self.categorical, self.correction_method)
        elif self.test == "corr":
            self.model = corr(self.data, self.numeric[0], self.numeric[1], self.correlation_method, self.alternative)
        elif self.test == "regression":
            self.model = regression(self.data, self.numeric[0], self.numeric[1], self.regression_type)
        else:
            self.model = kruskall(self.data, self.numeric[0], self.categorical[0], self.correction_method)


    def check_var_type(self):
        """
        Method to ckeck and attribute the type to variable selected by the user
        """
        self.variable_types = {"numerical": [], "categorical" : []}
        for var in [v for v in [self.X_var, self.Y_var, self.Z_var] if v is not None]:            
            if pd.api.types.is_numeric_dtype(self.data[var]) and len(self.data[var].unique()) > 2: # select categorical variable and binary ones
                self.variable_types["numerical"].append(var)
            else :
                self.variable_types["categorical"].append(var)

    def plot_stat(self) -> None:
        """
        Function to add * and segment for statistical annotations
        """
        self.ratio = 1.05
        self.star_ratio = 1.01
        self.star_size = 12

        self.max_1 = max(self.data.loc[self.data[self.X_var] == self.var1, self.Y_var])
        self.max_2 = max((self.data.loc[self.data[self.X_var] == self.var2, self.Y_var]))
        self.maxi = max(self.max_1, self.max_2, self.maxi)
        self.maxi = self.maxi * self.ratio
   
        self.plot += annotate("segment", x=self.var1, xend=self.var2, y = self.maxi, yend = self.maxi, color="black")
        self.plot += annotate("segment", x=self.var1, xend=self.var1, y = self.maxi - 0.01 * self.maxi, yend = self.maxi, color = "black")
        self.plot += annotate("segment", x=self.var2, xend=self.var2, y = self.maxi - 0.01 * self.maxi, yend = self.maxi, color = "black")
        self.plot += annotate("text")
        for threshold in sorted(self.dict_stat.keys(), reverse=False): # help to quantify the annotation for stat
            if self.pvalue < threshold:
                print(self.pvalue)
                self.symbol = self.dict_stat[threshold]
                print(self.symbol)
                self.plot += annotate("text", x=(self.cpt + 1 + self.j + 1) / 2, y = self.maxi * self.star_ratio , label= self.symbol, 
                                    ha='center', va='bottom', color="black", size = self.star_size)
                break

    
    def set_cat1_content(self, value):
        self.cat1_content = value

    def set_cat2_content(self, value):
        self.cat2_content = value

    def set_paired(self, value):
        self.paired = value

    def set_alternative(self, value):
        self.alternative = value

    def set_correction_method(self, value):
        self.correction_method = value

    def set_correlation_method(self, value):
        self.correlation_method = value

    def set_regression_type(self, value):
        self.regression_type = value

    # Method to reset all variables to None
    def reset_variables(self):
        self.cat1_content = None
        self.cat2_content = None
        self.paired = None
        self.alternative = None
        self.correction_method = None
        self.correlation_method = None
        self.regression_type = None