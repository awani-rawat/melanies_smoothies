# Import python packages
import streamlit as st
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name = st.text_input('Name on Smoothie:')
st.write('The name on smoothie will be: ', name)

ingredients_list = st.multiselect('choose upto 5 ingredients', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name+"""' )"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')
    if time_to_insert:
    #if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name}!', icon="✅")
    
