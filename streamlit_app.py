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


#create function
def get_fruity_vice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) # normalises the json -- so puts it as a normalised table format
    return fruityvice_normalized

#try except statement
try: 
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('Please select a fruit.')
  else:
    data_returned = get_fruity_vice_data(fruit_choice)
    st.dataframe(data_returned) # returns the table as a dataframe
except URLError as e:
  st.error()
  


#new buttons to update list

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
    
def insert_into_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values (' " + new_fruit + "')")
        return 'Thank you for adding '+ new_fruit

#add a button to load fruit data
if st.button('Get new Fruit Load list'):
    #connect python to snowflake yee
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)
    my_cnx.close()
    
#add a button to add fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add to the list ?')
if st.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_function = insert_into_snowflake(add_my_fruit)
    st.text(back_from_function)
    my_cnx.close()
