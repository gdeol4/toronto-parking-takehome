import pandas as pd

def data_cleaner(list_of_dfs):
    final_df = pd.concat(list_of_dfs)
    final_df.rename(columns = {0:'rate_values'}, inplace = True)
    final_df = final_df.dropna()
    final_df["rate_values"] = final_df["rate_values"].str[1:]
    final_df = pd.to_numeric(final_df['rate_values'])
    max_rate_val = final_df.max()
    
    return max_rate_val, final_df