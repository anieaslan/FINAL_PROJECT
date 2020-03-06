import streamlit as st
import sqlite3
from PIL import Image
import altair as alt
import pandas as pd
pd.set_option('display.max_colwidth', -1)

# image = Image.open('LEGO.jpg')

st.markdown("<h1 style='text-align: center; color: red;'>LET'S BUILD WITH LEGOS</h1>", 
unsafe_allow_html=True)

# st.image(image, caption="Everything is AWSESOME!!!!!", 
# use_column_width=True)

# audio_file = open('Awesome.ogg', 'rb')

# audio_bytes = audio_file.read()

# st.audio(audio_bytes, format='audio/ogg')

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

# TO ADD A SIMPLE PICTURE OF WHAT I NEED TO SHOW
# pics = {
#     "Moderate": "lego_.jpeg",
#     "Intermediate": "",
#     "Recreational": "",
#     "Advanced": "",
#     "Masters": ""
# }

diffList = my_cursor.fetchall() #The fetchAll() method retrieves all (remaining) rows of a query result, returning them as a sequence of sequences.

option = st.sidebar.selectbox(
    'Please choose what difficulty do you prefer?', 
    diffList, 
    format_func=showdifficulty)

# pic = st.selectbox("Picture choices", list(pics.keys()), 0)

# st.image(diffList[pic], use_column_width=True, caption=diffList[pic])

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
    # Rename the SQLite Column
    # renameTable = "ALTER TABLE 'partList' RENAME COLUMN '0' TO 'NewColumn'"

    # my_cursor.execute(renameTable)
    
    partList = my_cursor.fetchall()

    st.table(partList)

    
    
    #.rename(columns={'PartName', 'ImageUrl', 'Colour', 'Quantity'}))
    # st.table(partList) #ADDING markdown as suggested does not solve the issue #.to_html(escape=False, index=False), unsafe_allow_html=True))
    # st.write(st.table(partList).to_html(escape=False, index=False), unsafe_allow_html=True) # TO HYPERLINK THE URLS



# def add_stream_url(track_ids):
# 	return [f'https://open.spotify.com/track/{t}' for t in track_ids]

    # def make_clickable(url, text):
    #     return f'<a target="_blank" href="{url}">{text}</a>'

# # show data
# if st.checkbox('Include Preview URLs'):
# 	partlist[1] = add_stream_url(df.track_id)
# 	partlist[1] = partlist[1].apply(make_clickable, args = ('Listen',))
# 	st.write(partlist.to_html(escape = False), unsafe_allow_html = True)
# else:
# 	st.write(partlist)


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