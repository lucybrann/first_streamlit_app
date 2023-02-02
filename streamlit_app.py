#import packages
import streamlit as st
import pandas as pd
import snowflake.connector
from urllib.error import URLError

st.title("Lucy's Lovely Brannigan Brunch")

st.header("Brunch Menu ( ALL DAY<3 )")
st.text("Caramelised Bacon Pancakes with yoghurt")
st.text("Brannigan Special")


st.header("Drinks Menu")

st.subheader("Hot Drinks")
st.text("Breakfast Tea")
st.text("Coffee")
st.text("Sticky Toffee Pudding Hot Chocolate")

st.subheader("Cold Drinks")
st.text("Orange Juice")
st.text("Apple Juice")

#create your own smoothie section
#user interaction yeeehaw
st.subheader("Build your own fruit smoothie ! ")


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#change index
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Select your favourite fruits !! :", list(my_fruit_list.index), ['Strawberries'])

#create new dataframe of just the fruits selected
fruits_to_show = my_fruit_list.loc[fruits_selected]

#show nutritional info
st.dataframe(fruits_to_show)

#new section to display fruityvice api
import requests
st.header("what fruit would you like to know about ?")

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# normalises the json -- so puts it as a normalised table format
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())


# shows the table as a dataframe
st.dataframe(fruityvice_normalized)

#connect python to snowflake yee
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")

#my_data_row = my_cur.fetchone()

my_data_rows = my_cur.fetchall() #return all !!
st.header("The fruit list contains:")
st.dataframe(my_data_rows)

#ask if they want new fruit
add_my_fruit = st.text_input('What fruit would you like to add to the list?')
st.write('Thank you for adding ', add_my_fruit)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit') ")
