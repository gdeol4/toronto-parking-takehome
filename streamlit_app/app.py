import streamlit as st
import pandas as pd
import numpy as np
import json
import warnings
from data_cleaner import data_cleaner
from json_flattener import flatten_json
warnings.filterwarnings('ignore')
# metadata
st.title("City parking lot insights")
st.subheader("Answers and insights to the 2019 'Green P Parking' dataset." )
st.text("Gurkamal Singh Deol")
st.markdown("###### Longitudinal and latitudinal values of the parking lots plotted:")
# load data
with open('green-p-parking-2019.json') as f:
    data = json.loads(f.read())
# normalize json and put into df
df = pd.json_normalize(data['carparks'])
######## Mapping the lots ########
df_cords = df[['lat', 'lng']] # subset df
df_cords.columns = ['lat', 'lon'] # rename columns
all_columns = list(df_cords) # creates list of all column headers
df_cords[all_columns] = df_cords[all_columns].astype(float) # change tye to float

st.map(df_cords)
st.subheader("Questions and answer:")
########## Question 1 ##########
st.markdown("###### 1. What is the number of parking lots in Toronto?")
with st.expander("Answer: Simple counting"):
     st.write("The length of the id feature is the number of lots")
     with st.echo():
         num_lots = len(df['id'])
     st.write(num_lots)

     st.write("However, when checking the ```address``` field only 244 unique values appear. When sorting by ```address``` three different lots are listed under one address: ")
     with st.echo():
        unqiue_lots = len(df.address.unique())
     st.write(unqiue_lots)
     st.write(df.iloc[:, : 4].sort_values(by=['address']).head())
        
     st.write("This is because a few smaller parking lots are clustered close together in some areas. And since each of these has a unique latitude ```lat``` and longitude ```lng``` value, it can be considered a unique parking lot.")
     with st.echo():
        unqiue_lat = len(df.lat.unique())
        unqiue_lng = len(df.lng.unique())
    
     st.write("Unique latitudinal values: ", unqiue_lat)
     st.write("Unique longitudinal values: ", unqiue_lng)
########## Question 2 ##########
st.markdown("###### 2.	What is the maximum rate with a dollar value for any period across all parking lots?")
with st.expander("Answer: Finding the max rate with flattening and regex"):
     st.write("The highest rate value is found within the nested dictionary, so the first step was to flatten the structure.")
     st.write("The function that performs this is named ```flatten_json``` in the ```json_flattener``` module. The source code for this function is found at the bottom of this section")
     st.write("To prepare the data, the period rate details were extracted to a list. Using list comprehension the dictionaries were flattened: ")
     with st.echo():
         rate_details = df['rate_details.periods'].tolist()
         df_flat = pd.DataFrame([flatten_json(x) for x in rate_details])

     st.write("The resulting dataframe uses the nested keys as column names and the value as row values, creating 45 fields. Many values are duplicated such as: ```Saturday - Sunday & Holidays``` and ```$14.00```")
     st.write(df_flat.iloc[:, : 3].head())
     st.write("To remedy this, a list of each column was made containing only unique values and structured into another dataframe:")
     with st.echo():
        listoflists = []
        for col in df_flat:
            listoflists.append(df_flat[col].unique())
        rates_df = pd.DataFrame(listoflists)

     st.write(rates_df.iloc[:, : 3].head())
     st.write("To extract only the rate values ```str.extract()``` was used to append ```re_lists``` with values from each column matching the input regex pattern:")
     with st.echo():
        re_lists = []
        rx = (r"(\$?(?:\d+,)*\d+\.\d+\-?)")
        for col in rates_df:
            re_lists.append(rates_df[col].str.extract(rx))

     st.write("The ```re_list``` variable is now a list of 45 lists which can be processed by the ```data_cleaner``` function from the ```data_cleaner``` module.")
     st.write("The ```data_cleaner``` function uses pandas to format and return the max numerical value which should be the highest rate value for any period:")
     with st.echo():
         def data_cleaner(list_of_dfs):
            final_df = pd.concat(list_of_dfs)
            final_df.rename(columns = {0:'rate_values'}, inplace = True)
            final_df = final_df.dropna()
            final_df["rate_values"] = final_df["rate_values"].str[1:]
            final_df = pd.to_numeric(final_df['rate_values'])
            max_rate_val = final_df.max()
            return max_rate_val, final_df

     with st.echo():
         max_rate_val = data_cleaner(re_lists)
     st.write("The final result of ```data_cleaner```: ")
     st.write(max_rate_val[1].head())
     st.write("The maximum rate value is: ", max_rate_val[0])
     st.write("The ```flatten_json``` function:")
     with st.echo():
         def flatten_json(nested_json: dict, exclude: list=['']) -> dict:
             out = dict()
             def flatten(x: (list, dict, str), name: str='', exclude=exclude):
                 if type(x) is dict:
                     for a in x:
                         if a not in exclude:
                            flatten(x[a], f'{name}{a}_')
                 elif type(x) is list:
                    i = 0
                    for a in x:
                        flatten(a, f'{name}{i}_')
                        i += 1
                 else:
                    out[name[:-1]] = x

                    flatten(nested_json)
                 return out
########## Question 3 ##########
st.markdown("###### 3.	What is the total capacity across all parking lots? What is the total capacity of parking lots that only accept both “Coins” and any type of “Charge”?")
with st.expander("Answer: Calculating capacity using boolean indexing"):
     st.write("The total cpacity of lots accepting only ```coins``` AND ```Charge``` can be found using boolean indexing by first defining a list of target payments in the ```paymt_keep``` variable.")
     with st.echo():
          paymt_keep = [['Coins', 'Charge (Visa / Mastercard / American Express Only)']]
     
     st.write("The original dataframe has the field ```payment_methods``` which has a list of payment options as its row value. To get the number of rows that have a value equal to the ```paymnt_keep``` variable, the index field named ```correct_payment``` is created. The value is boolean, with ```True``` as payment condition being satisfied.")
     with st.echo():
         df["correct_payment"] = df['payment_methods'].isin(paymt_keep)
     
     st.write(df["correct_payment"].head())
     st.write("Lastly, to get the capacity of these lots, the ```capacity``` field is converted to numeric values so that ```capacity``` of the rows where ```correct_payment``` = ```True``` can be summed")
     with st.echo():
         df['capacity'] = pd.to_numeric(df['capacity'])
         correct = df.loc[df['correct_payment'] == True, 'capacity'].sum()
         incorrect = df.loc[df['correct_payment'] == False, 'capacity'].sum()

     st.write('The total capacity of lots that take only coins and any type of charge is: ', correct)
     st.write('The total capacity of lots that take other combinations of payment is: ', incorrect)
     st.write('The total capacity is: ', correct+incorrect, "parking spots")
st.markdown("###### 4.	What changes would you make to this data set? Why?")
st.markdown("The dataset itself was in good condition, with very few missing values. I would opt to flatten the structures at least one level and rename the columns to retrieve the information easier. I think it would interesting to provide some other datasets from Toronto Open Data such as the Parking Lot Facilities dataset that includes data on parking lots operated by the City of Toronto.")
#num_lots = len(df['id'])