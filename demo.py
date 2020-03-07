import streamlit as st
import sqlite3
from PIL import Image
import altair as alt
import pandas as pd
pd.set_option('display.max_colwidth', -1)

st.markdown("<h1 style='text-align: center; color: red;'>LET'S BUILD WITH LEGOS</h1>", 
unsafe_allow_html=True)

video_file = open('Everything.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

    
def showLabel(option):
    return option[1]

def showdifficulty(option):
    return option[0]

#VISUALIZE RAW DATA

st.markdown("<h1 style='text-align: center; color: green;'>Raw data</h1>", unsafe_allow_html=True)

data = st.cache(pd.read_csv)('db_cleaned.csv')

st.write(data[:1000])

# GET THE USERS PREFERENCES

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.markdown("<h1 style='text-align: center; color: blue;'>Here are the pieces that you need</h1>", unsafe_allow_html=True)

connection = sqlite3.connect('bd.db')

my_cursor = connection.execute("SELECT DISTINCT binned from Sets")

diffList = my_cursor.fetchall() #The fetchAll() method retrieves all (remaining) rows of a query result, returning them as a sequence of sequences.

option = st.sidebar.selectbox(
    'Please choose what difficulty do you prefer?', 
    diffList, 
    format_func=showdifficulty)

name = st.sidebar.text_input(
    'Now, enter what you would like to build!'
    )

my_cursor = connection.execute(
    "SELECT SetNumber, Name from Sets where binned = ? and Name LIKE ?", 
    [option[0],
    '%' + name + '%']
    )

setList = my_cursor.fetchall()

legoSelected = st.sidebar.selectbox(
    'From previous selection, now select LEGO set to build', 
    setList, 
    format_func=showLabel
    )

if legoSelected is not None:
    my_cursor = connection.execute(
        "SELECT p.PartName, p.ImageUrl, p.Colour, ps.Quantity from PartSets ps inner join Parts p on ps.PartId = p.PartId where ps.SetNumber = ?", 
        [legoSelected[0]]   
        )
    
    partList = my_cursor.fetchall()

    st.table(partList)

    
#FINAL VISUALIZATIONS

# st.subheader('Fun LEGO facts')

# source = st.cache(pd.read_csv)('db_cleaned.csv')

# altair_chart = alt.Chart(source).mark_area().encode(
#     alt.X('yearmonth(year):T',
#     axis=alt.Axis(format='%Y', domain=False)),
#     alt.Y('sum(Quantity):Q', stack='center', axis=None),
#     alt.Color('series:N',
#     scale=alt.Scale(scheme='category20b')))
# st.write(altair_chart)