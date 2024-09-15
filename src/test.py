from plotnine import *
import stat_python as st
import pandas as pd

df = pd.read_csv("ressources/fusion_ctrl.csv")

dict_stat = {0.05 : "*", 0.01 : "* *", 0.001 : "* * *", 0.0001 : "* * * *"}
theme_set(theme_bw()) # change background
plot = (ggplot(data = df))
plot += geom_boxplot(aes(x = "Group_16S", y = "Shannon_NRPS", color = "Group_16S"))
unique_x = df["Group_16S"].unique() # get all the value in the column
unique_x.sort()



y = 1
for cpt in range(len(unique_x) - 1):# browse all the factor
    var1 = unique_x[cpt]
    for j in range(cpt +1, len(unique_x)): # create all the pair if necessary
        var2 = unique_x[j]
        model = st.student_test(df, "Shannon_NRPS", "Group_16S", var1 , var2)
        print(f"P-value between {var1} and {var2} : {model['p-val'].values[0]}")
        pvalue = model['p-val'].values[0]
        if pvalue  < 0.05:
        # Ajouter des segments entre les boîtes
            maxi = max(max(df.loc[df["Group_16S"] == var1, "Shannon_NRPS"]), max(df.loc[df["Group_16S"] == var2, "Shannon_NRPS"]))
            plot += annotate("segment", x=var1, xend=var2, y = maxi + 0.15 * y, yend = maxi + 0.15 * y, color="black")
            plot += annotate("segment", x=var1, xend=var1, y = maxi + 0.15 * y - 0.01 * maxi, yend = maxi + 0.15 * y, color = "black")
            plot += annotate("segment", x=var2, xend=var2, y = maxi + 0.15 * y - 0.01 * maxi, yend = maxi + 0.15 * y, color = "black")
            plot += annotate("text")
            for threshold in sorted(dict_stat.keys(), reverse=False):
                if pvalue < threshold:
                    symbol = dict_stat[threshold]
                    break
                        
            # Ajouter le texte de l'annotation
            plot += annotate("text", x=(cpt + 1 + j + 1) / 2, y=maxi + 0.15 * y + 0.02, label=symbol, ha='center', va='bottom', color="black")
            y += 1
plot.show()