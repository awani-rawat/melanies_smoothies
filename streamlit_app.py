# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
pd_df = my_dataframe.to_pandas()

name = st.text_input('Name on Smoothie:')
st.write('The name on smoothie will be: ', name)

ingredients_list = st.multiselect('choose upto 5 ingredients', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        #search_on= pd_df.loc[pd_df['fruit_name'] == fruit, 'search_on'].iloc[0]
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for '+ fruit + ' is '+ search_on)
        st.subheader(fruit + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name+"""' )"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')
    if time_to_insert:
    #if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name}!', icon="✅")
    

