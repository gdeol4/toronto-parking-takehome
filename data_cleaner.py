import pandas as pd

def data_cleaner(list_of_dfs): # input argument is a list of dfs
    final_df = pd.concat(list_of_dfs) # concatonate the dataframes
    final_df.rename(columns = {0:'rate_values'}, inplace = True) # rename column
    final_df = final_df.dropna() # drop na; unnecessary
    final_df["rate_values"] = final_df["rate_values"].str[1:] # remove the $
    final_df = pd.to_numeric(final_df['rate_values']) # convert from str to num
    max_rate_val = final_df.max() # find the highest value
    
    return max_rate_val, final_df