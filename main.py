import pandas as pd
import json, warnings
from data_cleaner import data_cleaner
from json_flattener import flatten_json
warnings.filterwarnings('ignore')
# Load data
with open('green-p-parking-2019.json') as f:
    data = json.loads(f.read())
# normalize the carparks dictionairy
df = pd.json_normalize(data['carparks'])
# The number of ids
num_lots = len(df['id'])
# extract period information into list
rate_details = df['rate_details.periods'].tolist()
# apply flatten_json function to each element *found in json_flattener.py*
df_flat = pd.DataFrame([flatten_json(x) for x in rate_details])
# initialize list and append it with unique values
listoflists = []
for col in df_flat:
    listoflists.append(df_flat[col].unique())
# create a df of unique values
rates_df = pd.DataFrame(listoflists)
# initialize another list and write regex pattern
re_lists = []
rx = (r"(\$?(?:\d+,)*\d+\.\d+\-?)")
# extract strings matching the regex pattern to the empty list
for col in rates_df:
    re_lists.append(rates_df[col].str.extract(rx))
# format the list of extracted terms *found in data_cleaner.py*
max_rate_val = data_cleaner(re_lists)
# set payments list condition and create boolean index
paymt_keep = [['Coins', 'Charge (Visa / Mastercard / American Express Only)']]
df["correct_payment"] = df['payment_methods'].isin(paymt_keep)
# convert column to numeric and calculate sums with index
df['capacity'] = pd.to_numeric(df['capacity'])
total_capacity = df['capacity'].sum()
correct = df.loc[df['correct_payment'] == True, 'capacity'].sum()
incorrect = df.loc[df['correct_payment'] == False, 'capacity'].sum()
# print question answers
print("The total number of carparks in toronto is: ", num_lots, "parking lots (considering they all have different latitudinal, longitudinal, and slug values).")
print("The max rate value for any given period is: ",  "$", max_rate_val[0])
print('The total capacity of lots that take only coins and any type of charge is: ', correct)
print('The total capacity of lots that take other combinations of payment is: ', incorrect)
print('The total capacity is: ', total_capacity, "parking spots")
print('The dataset itself was in good condition, with very few missing values. I would opt to flatten the structures at least one level and rename the columns to retrieve the information easier. I think it would interesting to provide some other datasets from Toronto Open Data such as the Parking Lot Facilities dataset that includes data on parking lots operated by the City of Toronto.')