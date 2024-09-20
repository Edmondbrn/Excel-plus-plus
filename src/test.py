# from plotnine import *
# import stat_python as st
# import pandas as pd

# df = pd.read_csv("ressources/fusion_ctrl.csv")

# dict_stat = {0.05 : "*", 0.01 : "* *", 0.001 : "* * *", 0.0001 : "* * * *"}
# theme_set(theme_bw()) # change background
# plot = (ggplot(data = df))
# plot += geom_boxplot(aes(x = "Group_16S", y = "Shannon_NRPS", color = "Group_16S"))
# unique_x = df["Group_16S"].unique() # get all the value in the column
# unique_x.sort()



# # y = 1
# maxi = 0
# for cpt in range(len(unique_x) - 1):# browse all the factor
#     var1 = unique_x[cpt]
#     for j in range(cpt +1, len(unique_x)): # create all the pair if necessary
#         var2 = unique_x[j]
#         model = st.student_test(df, "Shannon_NRPS", "Group_16S", var1 , var2)
#         print(f"P-value between {var1} and {var2} : {model['p-val'].values[0]}")
#         pvalue = model['p-val'].values[0]
#         if pvalue  < 0.05:
#         # Ajouter des segments entre les boîtes
#             max_1 = max(df.loc[df["Group_16S"] == var1, "Shannon_NRPS"])
#             max_2 = max(df.loc[df["Group_16S"] == var2, "Shannon_NRPS"])
#             maxi = max(max_1, max_2, maxi)
           
#             maxi = 1.05 * maxi
          
#             plot += annotate("segment", x=var1, xend=var2, y = maxi, yend = maxi, color="black")
#             plot += annotate("segment", x=var1, xend=var1, y = maxi - 0.01 * maxi, yend = maxi, color = "black")
#             plot += annotate("segment", x=var2, xend=var2, y = maxi - 0.01 * maxi, yend = maxi, color = "black")
#             plot += annotate("text")
#             for threshold in sorted(dict_stat.keys(), reverse=False):
#                 if pvalue < threshold:
#                     symbol = dict_stat[threshold]
#                     break
                        
#             # Ajouter le texte de l'annotation
#             plot += annotate("text", x=(cpt + 1 + j + 1) / 2, y= 1.01 * maxi, label=symbol, ha='center', va='bottom', color="black", size = 12)
#             # y += 1
# plot.show()

import pandas as pd
import scipy.stats as stats
import scikit_posthocs as sp
import pingouin as pg

def anova(data : pd.DataFrame, num_var : str, factor : list[str], pval_corr : str = "tukey"):
    """
    num_var : column with the numerical data
    factor : list of column with factor variables
    """
    model = pg.anova(data,num_var, factor)
    if model["p-unc"] < 0.05 :
        if pval_corr == "tukey":
            tukey_test = tukey(data, num_var, factor[0])
            tukey_test = format_tukey(tukey_test)
        elif pval_corr == "bonferroni" or pval_corr == "fdr":
            pass
    return model, tukey_test

def tukey(data, col_num, col_cat):
    model = pg.pairwise_tukey(dv = col_num, between = col_cat, data = data)
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

# Étape 1: Créer un DataFrame d'exemple
data = {
    'value': [5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8],
    'group': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D']
}
df = pd.DataFrame(data)

# Étape 2: Effectuer le test de Kruskal-Wallis
groups = [group['value'].values for name, group in df.groupby('group')]
kruskal_result = stats.kruskal(*groups)
print(f"Kruskal-Wallis test p-value: {kruskal_result.pvalue}")

# Étape 3: Si le test de Kruskal-Wallis est significatif, effectuer le test de Dunn
if kruskal_result.pvalue > 0.05:
    print(df)
    dunn_result = tukey(df, col_num='value', col_cat='group')
    dunn_result = format_tukey(dunn_result)
    print("Dunn's test results with Bonferroni correction:")
    print(dunn_result)
    print(dunn_result.loc["A", 'B'])
else:
    print("Kruskal-Wallis test not significant, no need for Dunn's test.")