import streamlit as st
import pandas as pd
import numpy as np
import json
import warnings
from data_cleaner import data_cleaner
from json_flattener import flatten_json
warnings.filterwarnings('ignore')

st.title("Toronto parking insights")
st.text("Answers and insights to the 2019 'Green P Parking' dataset." )

st.subheader("Questions to answer:")

st.markdown("1. What is the number of parking lots in Toronto?")
st.markdown("2.	What is the maximum rate with a dollar value for any period across all parking lots?")
st.markdown("3.	What is the total capacity across all parking lots? What is the total capacity of parking lots that only accept both “Coins” and any type of “Charge”?")
st.markdown("4.	What changes would you make to this data set? Why?")

with open('green-p-parking-2019.json') as f:
    data = json.loads(f.read())

df = pd.json_normalize(data['carparks'])

with st.expander("Question 1"):
     st.write("The length of the id feature is the number of lots")
     with st.echo():
         num_lots = len(df['id'])

#num_lots = len(df['id'])

with st.expander("Question 2"):
     st.markdown("The feature ```rate_details``` has a nested dictionairy value, the first level key: 'period' contains the rate information.")
     st.markdown("The function ```flatten_json``` flattens the dictionairy.")

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

paymt_keep = [['Coins', 'Charge (Visa / Mastercard / American Express Only)']]

df["correct_payment"] = df['payment_methods'].isin(paymt_keep)

correct = df.loc[df['correct_payment'] == True, 'capacity'].sum()
incorrect = df.loc[df['correct_payment'] == False, 'capacity'].sum()



st.write("The total number of carparks in toronto is: ", num_lots, "parking lots")
st.write("The max rate value for any given period is: ",  "$", max_rate_val)
st.write('The total capacity of lots that take only coins and any type of charge is: ', correct)
st.write('The total capacity of lots that take other combinations of payment is: ', incorrect)
st.write('The total capacity is: ', total_capacity, "parking spots")