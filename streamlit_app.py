#import packages
import streamlit as st
import pandas as pd

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

st.multiselect("Select your favourite fruits !! :", list(my_fruit_list.index))

#show nutritional info
st.dataframe(my_fruit_list)
