import streamlit

streamlit.title("My Mom's New Healthy Breakfast")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pd
my_fruit_list=pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list=my_fruit_list.set_index('Fruit')
# streamlit.dataframe(my_fruit_list)
# Lets put a pick list here so that they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some Fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# Let's Call the Fruityvice API from Our Streamlit App!
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/kiwi")
#  just writes the data on the screen
# streamlit.text(fruityvice_response.json()) 

# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output it the screen as table
streamlit.dataframe(fruityvice_normalized)

# Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
# New Section to display user fruityvice api response
streamlit.header("Fruityvice Fruit Advice! as per user choice")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response_user = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
fruityvice_normalized_user = pd.json_normalize(fruityvice_response_user.json())
streamlit.dataframe(fruityvice_normalized_user)

