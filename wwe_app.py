# Import python packages
import streamlit as st
import requests 
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: WWE Superstar Data :cup_with_straw: {st.__version__}")
st.write(
  """Know your Superstar
  """
)

superstar = st.text_input("Enter the name of Superstar")
st.write(superstar)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("ss.public.superstars").select(col('SUPERSTAR'))

if superstar:
    player_info = session.table("ss.public.superstars").filter(col('SUPERSTAR') == superstar)
    st.dataframe(player_info, use_container_width=True)

st.stop()
my_dataframe = session.table("ss.public.superstars")
st.dataframe(my_dataframe, use_container_width=True)


#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """' , '"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
   
    time_to_insert = st.button('Submit Order')
    #st.stop()

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order + '!', icon="✅")
