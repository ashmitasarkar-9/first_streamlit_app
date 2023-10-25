import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Breakfast")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas as pd
my_fruit_list=pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list=my_fruit_list.set_index('Fruit')
# streamlit.dataframe(my_fruit_list)
# Lets put a pick list here so that they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some Fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# create the repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response_user = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized_user = pd.json_normalize(fruityvice_response_user.json())
  return fruityvice_normalized_user
  
# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# Let's Call the Fruityvice API from Our Streamlit App!
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/kiwi")
#  just writes the data on the screen
# streamlit.text(fruityvice_response.json()) 

# take the json version of the response and normalize it
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output it the screen as table
# streamlit.dataframe(fruityvice_normalized)

# Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
# New Section to display user fruityvice api response
# streamlit.header("Fruityvice Fruit Advice! as per user choice")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get info.")
  else:
    back_from_func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_func)
except URLError as e:
  streamlit.error()

# dont run anything past here while we troubleshot
# streamlit.stop()
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into FRUIT_LOAD_LIST values('" + new_fruit +"')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_func = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_func)


# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_row)

# Adding 2nd Text entry box

streamlit.write('Thanks for adding ', add_my_fruit)

# This will not work properly, but just go with it now
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")





