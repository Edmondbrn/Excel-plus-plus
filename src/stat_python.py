import pandas as pd
import pingouin as pg
import scipy.stats as st
import numpy as np
import scikit_posthocs as sp


def wilcox_test(data : pd.DataFrame, col_num: str, 
                col_catego : str, cat1 : str, cat2 : str, 
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

    filter1 = data[col_catego] == cat1
    filter2 = data[col_catego] == cat2
    model = pg.ttest(data.loc[filter1, col_num], data.loc[filter2, col_num], paired = paired, alternative = alternative)
    return model


def kruskall(data : pd.DataFrame, num_var : str, factor : str, method : str = "bonferroni"):
    """
    factor : column with the categorical data
    factor_bis : another column to filter data before the test if necessary
    var_bis : the value to check in the col_catego_bis
    """
   
    model = pg.kruskal(data, num_var, factor)
    if model["p-unc"].values[0] < 0.05:
        # Perform Dunn's test
        dunn_result = sp.posthoc_dunn(data, val_col = num_var, group_col= factor , p_adjust= method)
        return model, dunn_result
    else:
        return model

def anova(data : pd.DataFrame, num_var : str, factor : list[str], pval_corr : str = "tukey"):
    """
    num_var : column with the numerical data
    factor : list of column with factor variables
    """
    model = pg.anova(data,num_var, factor)
    if model["p-unc"].values[0] < 0.05 :
        if pval_corr == "tukey":
            tukey_test = tukey(data, num_var, factor[0])
            tukey_test = format_tukey(tukey_test)
        elif pval_corr == "bonferroni" or pval_corr == "fdr":
            pass
        return model, tukey_test
    return model

def tukey(data, col_num, col_cat):
    model = pg.pairwise_tukey(col_num, between = col_cat, data = data)
    return model

def format_tukey(tukey_test):
    """
    Format the Tukey test result to match the Dunn test result format.
    
    Parameters:
    tukey_test (pd.DataFrame): The result of Tukey's HSD test.
    
    Returns:
    pd.DataFrame: The formatted result.
    """
    # Extract unique categories
    categories = pd.unique(tukey_test[['A', 'B']].values.ravel('K'))
    categories.sort()
    
    # Create an empty DataFrame with categories as both rows and columns
    formatted_tukey = pd.DataFrame(index=categories, columns=categories)
    
    # Fill the DataFrame with p-values
    for _, row in tukey_test.iterrows():
        formatted_tukey.at[row['A'], row['B']] = row['p-tukey']
        formatted_tukey.at[row['B'], row['A']] = row['p-tukey']
    
    return formatted_tukey

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
    model = pg.corr(x = data[col1], y = data[col2], method = method, alternative = alternative)
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

def correction(pval : list[float], method : str):
    """
    Function to correct the pvalue with the precised method
    """
    pval = np.array(pval)
    if method == "bonferonni":
        pval = pval * len(pval)
    elif method == "fdr":
        pval = st.false_discovery_control(pval)

    return pval



def dico_function(data : pd.DataFrame, col_num : str = None, col_num2 : str = None, col_num3 : str = None,
                  col_cat : str = None, value_cat1 : str = None, value_cat2 : str = None, 
                  col_catego_2 : str = None, value_catego_2 : str = None,
                  col_catego_3 : str = None,
                  corr_method : str = None, regression_method : str = None, pairwise_corr : str = "bonferroni",
                  paired : bool = False, alternative : str = "two-sided"):
    """
    Function which stores all the statistical tests to use them later in the plot.py file
    """
    dict_test = {
        "ttest": lambda: student_test(data, col_num, col_cat, value_cat1, value_cat2, col_catego_2, value_catego_2, paired, alternative),
        "wilcox": lambda: wilcox_test(data, col_num, col_cat, value_cat1, value_cat2, col_catego_2, value_catego_2, paired, alternative),
        "chi2": lambda: chi2(data, col_cat, col_catego_2, paired),
        "fisher": lambda: fisher(data, col_cat, col_catego_2, alternative),
        "anova": lambda: anova(data, col_num, [col_cat, col_catego_2, col_catego_3], pairwise_corr),
        "kruskall": lambda: kruskall(data, col_num, col_cat, pairwise_corr, col_catego_2, value_catego_2),
        "corr": lambda: corr(data, col_num, col_num2, corr_method, alternative),
        "regression": lambda: regression(data, col_num, col_num2, regression_method)
    }

    return dict_test
