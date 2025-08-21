# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(  f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)


title = st.text_input("Name on SMoothie:")
st.write("The name on zour Smoothie will be ", title)
 

#option = st.selectbox(
#    "What is your favourite fruit? ",
#   ("Banana", "Strawberries", "Peaches"),
#)
 
#st.write("Your favourite fruit is:", option)
cnx =  st.connection("snowflake")
session = cnx.session()
#get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections = 5)

if ingredients_list:
  ingredients_string = ''

for fruit_chosen in ingredients_list:
  ingredients_string  += fruit_chosen + ' '
  smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
  #st.text(smoothiefroot_response)
  sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

#st.dataframe(data=my_dataframe, use_container_width=True)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + title + """')"""

st.write(my_insert_stmt)

time_to_insert = st.button('Submit order') 

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


 

    

