#%% Setup
import numpy as np
import pandas as pd
from scipy.stats import shapiro


from functions import (
    create_table_categorical,
    create_graph_categorical,
    create_table_numeric_continuous,
    create_graph_numeric_continuous,
    bivariate,
    create_table_bivariate_summary,
    create_table_bivariate_html,
    create_graph_bivariate_html,
    create_graph_h_bivariate_html
    )


#%%
# Read files
file_name = "Bank Customer Churn Prediction"
df = pd.read_csv(f"./source/{file_name}.csv")


# -> there is no duplciated customer
df.duplicated("customer_id").sum()

# -> there is no missing values
df.isna().sum()

# -> remove cols not useful
df.drop("customer_id", axis = 1, inplace = True)

# -> preprocessing
df_base = df.copy()

# "products_number"
df["products_number"] = np.where(df["products_number"] >= 4 , ">=4", df["products_number"].astype(int).astype(str))

# tenure
var_name = 'tenure'
c1 = df[var_name].between(0,  2,      inclusive = "both")
c2 = df[var_name].between(2,  4,      inclusive = "right")
c3 = df[var_name].between(4,  6,      inclusive = "right")
c4 = df[var_name].between(6,  8,      inclusive = "right")
c5 = df[var_name].between(8,  10,     inclusive = "right")
c6 = df[var_name].between(10, np.inf, inclusive = "neither")

df[var_name] = np.where(
    c1, '[0, 2]', np.where(
        c2, '(2, 4]', np.where(
            c3, '(4, 6]', np.where(
                c4, '(6, 8]', np.where(
                    c5, '(8, 10]', '>10' 
                    )
                )
            )
        )
    ) 

#%% bivariate
numerical_variables = [
    "products_number",
    "tenure",
    "credit_score",
    "age",
    "estimated_salary"
    ]

categorical_variables = [
    "country", 
    "gender", 
    "credit_card",
    "active_member",
    "balance",
    ]

target_variable = 'churn'

df = df_base

# balance
var_name = 'balance'
c1 = df[var_name].between(-np.inf,  1884.34, inclusive = "neither")
df[var_name] = np.where(c1, '< 1884.34', '>= 1884.34')

df_bivariate = bivariate(
    df,
    numerical_variables,
    categorical_variables,
    target_variable)

df_bivariate.rename(columns = {"Indicador":"Feature"}, inplace = True)
df = (
  df_bivariate[["Feature", "Cramer's V", "Discriminância"]]
  .drop_duplicates()
  .sort_values(by = ["Cramer's V", "Feature"], ascending = False)
  .reset_index(drop = True)
  )

    

        


