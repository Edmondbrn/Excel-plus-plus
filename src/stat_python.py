import pandas as pd
import pingouin as pg
import scipy.stats as st



def wilcox_test(data : pd.DataFrame, col_num: str, 
                col_catego : str, cat1 : str, cat2 : str, 
                col_catego_bis : str = None, catbis : str = None,
                paired : bool = False, alternative = "two-sided"):
    """
    Function which performs a wilcoxon MannWhitney test in python.
    data : the dataframa with all the value
    col_num : name of the column which contains the numerical value to study
    col_catégo : column with the catégorical data
    cat1 : fisrt value of the categorical data
    cat2 : second value of the categorical data
    col_ctago_bis : another column to filter data before the test if necessary
    catbis : the value to check in the col_catego_bis
    paired : booléen to know if data are independant or not (change the type of test)
    """
    if col_catego_bis and catbis:
        filter1 = (data[col_catego] == cat1) & (data[col_catego_bis] == catbis)
        filter2 = (data[col_catego] == cat2) & (data[col_catego_bis] == catbis)
    else:
        filter1 = data[col_catego] == cat1
        filter2 = data[col_catego] == cat2

    if paired:
        model = pg.wilcoxon(
            data.loc[filter1, col_num],
            data.loc[filter2, col_num],
            alternative=alternative
        )
    else:
        model = pg.mwu(
            data.loc[filter1, col_num],
            data.loc[filter2, col_num],
            alternative = alternative
        )
    
    return model


def student_test(data : pd.DataFrame, col_num: str, 
                col_catego : str, cat1 : str, cat2 : str, 
                col_catego_bis : str = None, catbis : str = None,
                paired : bool = False, alternative = "two-sided"):
    """
    Function which performs a wilcoxon MannWhitney test in python.
    data : the dataframa with all the value
    col_num : name of the column which contains the numerical value to study
    col_catégo : column with the catégorical data
    cat1 : fisrt value of the categorical data
    cat2 : second value of the categorical data
    col_ctago_bis : another column to filter data before the test if necessary
    catbis : the value to check in the col_catego_bis
    paired : booléen to know if data are independant or not (change the type of test)
    """
    if col_catego_bis and catbis:
        filter1 = (data[col_catego] == cat1) & (data[col_catego_bis] == catbis)
        filter2 = (data[col_catego] == cat2) & (data[col_catego_bis] == catbis)
    else:
        filter1 = data[col_catego] == cat1
        filter2 = data[col_catego] == cat2
    model = pg.ttest(data.loc[filter1, col_num], data.loc[filter2, col_num], paired = paired, alternative = alternative)
    return model


def kruskall(data : pd.DataFrame, num_var : str, factor : str, factor_bis : str = None, var_bis : str = None):
    """
    factor : column with the categorical data
    factor_bis : another column to filter data before the test if necessary
    var_bis : the value to check in the col_catego_bis
    """
    if factor_bis: # if you want to filter data before the test
        data = data.loc[data[factor_bis] == var_bis]
    model = pg.kruskal(data, num_var, factor)
    return model

def anova(data : pd.DataFrame, num_var : str, factor : list[str]):
    """
    num_var : column with the numerical data
    factor : list of column with factor variables
    """
    model = pg.anova(data,num_var, factor)
    return model

def table(data: pd.DataFrame, col1: str, col2 : str, col3 : str = None) -> pd.DataFrame:
    """
    data : datframe with all the data
    col1 :  first categorical data
    col 2 : second categorical data
    col 3 : third one for two ways ANOVA
    """
    if col3:
        liste_cate = [data[col2], data[col3]]
        data = pd.crosstab(data[col1], liste_cate)
    else:
        data = pd.crosstab(data[col1], data[col2])
    return data

def chi2(data : pd.DataFrame, col1 : str, col2 : str, paired = False):
    if len(data[col1].unique()) < 2 or len(data[col2].unique()) < 2:
        print("tets")
        raise Exception("Error, the factor doesn't have at least 2 levels.")
    else:
        if not paired:
            model = pg.chi2_independence(data, col1, col2)
        else:
            model = pg.chi2_mcnemar(data, col1, col2)
        return model
    

def fisher(data : pd.DataFrame, col1 : str, col2 :str, alternative : str = "two-sided"):
    """
    data : datframe with all the data
    col1 :  first categorical data
    col 2 : second categorical data
    alternative : two-sided, less, greater
    """
    contingency = table(data, col1, col2)
    model = st.fisher_exact(contingency, alternative)
    return model

def corr(data, col1 : str, col2 : str, method : str, alternative : str = 'two-sided'):
    """
    data : pandas dataframe

    col1 : fisrt column with numerical data

    col2 : second column

    method :
        pearson: Pearson product-moment correlation

        spearman: Spearman rank-order correlation

        kendall: Kendall’s correlation (for ordinal data)

        bicor: Biweight midcorrelation (robust)

        percbend: Percentage bend correlation (robust)

        shepherd: Shepherd’s pi correlation (robust)

    alternative : two-sided, less, greater
    """
    model = pg.corr(x = data[col1], y = data[col2], method = method, alternative = "two-sided")
    return model

def regression(data : pd.DataFrame, x : str, y :str, type : str = "linear"):
    """
    data : pandas dataframe

    x : fisrt column with numerical data

    y : second column with numerical or categorical

    type : linear, logistic
    """
    if type == "linear":
        model = pg.linear_regression(data[x], data[y])
    elif type == "logistic":
        data["y_bis"] = (data[y] == data[y].unique()[0]).astype(int)
        model = pg.logistic_regression(data[x], data["y_bis"], penalty = "l2")
    return model


df = pd.read_csv("ressources/fusion_ctrl.csv", sep = ",")
# print(wilcox_test(df, "Shannon_16S", "Irrigation_NRPS", "Watered", "Drought", "WEEK", 4))
# print(student_test(df, "Shannon_16S", "Irrigation_NRPS", "Watered", "Drought", "WEEK", 4))
# print(kruskall(df, "Shannon_16S", "Irrigation_NRPS"))
# print(anova(df, "Shannon_16S", ["Irrigation_NRPS", "WEEK"]))

# print(chi2(df, "Irrigation_NRPS", "Irrigation_NRPS", True))
# print(fisher(df, "Irrigation_NRPS", "Irrigation_NRPS"))
print(regression(df, x = "Shannon_NRPS", y = "Irrigation_NRPS", type =  "logistic"))