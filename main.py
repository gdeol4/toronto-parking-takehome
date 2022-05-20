import pandas as pd
import numpy as np
import json
import warnings
from data_cleaner import data_cleaner
from json_flattener import flatten_json
warnings.filterwarnings('ignore')

with open('green-p-parking-2019.json') as f:
    data = json.loads(f.read())

df = pd.json_normalize(data['carparks'])
rate_details = df['rate_details.periods'].tolist()

df_flat = pd.DataFrame([flatten_json(x) for x in rate_details])

listoflists = []

for col in df_flat:
    listoflists.append(df_flat[col].unique())

rates_df = pd.DataFrame(listoflists)

re_lists = []
rx = (r"(\$?(?:\d+,)*\d+\.\d+\-?)")

for col in rates_df:
    re_lists.append(rates_df[col].str.extract(rx))

max_rate_val = data_cleaner(re_lists)

print("The max rate value for any given period is: ",  "$", max_rate_val, )