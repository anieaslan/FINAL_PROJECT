![IronHack Logo](https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/upload_d5c5793015fec3be28a63c4fa3dd4d55.png)

# Final Project Demo

## Overview

This demo is meant to serve as a simplified version of the type of analysis expected from you for your final project. In the sections below, we will go through each step of the data analysis workflow applying the appropriate operations at each step. You can use the code snippets and examples below as a guide for your own final project, but also feel free to go beyond what we have done and apply whichever methods are applicable to the data set you have chosen.

## The Data

The data set we will be using for this demo is from several data sets concatenated from https://brickset.com/. The data set contains a variety of features for over 15,000 LEGO sets and 30,000 different parts.

## Data Ingestion

In order to work with the final data set, we first had to ingest it. The file containing the data was in CSV format, so after downloading it, we used the `read_csv` method to read the data into a Pandas data frame.

```python
import pandas as pd

data = pd.read_csv('db_cleaned.csv')
```

Next, we checked that the data set loaded correctly by checking the shape of the data frame, looking at the first few rows of the data, and evaluating the column names to ensure that they look as we would expect.

```python
data.shape

```

```python
data.head(10)
```

```python
print(list(data.columns))

```

From this initial assessment, it looks like we have successfully ingested the data set. We can now move on to evaluating the quality of the data, cleaning it, and wrangling it so that it is ready to be analyzed and modeled.

## Data Wrangling and Cleaning

One of the first things we did in the wrangling and cleaning phase of the workflow is ensure that each data set joined each other into one BIG SET. We used to have separate data , as PARTS , SET-NUMBERS , ALLSETS , INVENTORY-BYSET

* There are several fields that are currently numeric that should be categorical. We can identify these via a combination of their column name and their low number of unique values.

* There are several fields in the data that contain null values. We will need to figure out how to address those.

* We had to create a for_loop to retrieve the inventory in each set since 2000 with more than 15 pieces per set.

## Data Storage

Once the data had been ingested and cleaned, we stored it in a MySQL database. 

```python
engine = create_engine('sqlite:///bd.db', echo=False)
```

We then used `to_sql` and to create the needed tables.

```python

dfSets = legoDf[['SetNumber','name', 'binned']]
dfSets.drop_duplicates(inplace=True)
dfSets.to_sql('Sets', con = engine, if_exists = 'append', chunksize = 1000, index=False)
```

```python

dfParts = legoDf[['PartID','PartName', 'ImageURL', 'Colour', 'SetCount']]
dfParts.drop_duplicates(inplace=True)
dfParts.to_sql('Parts', con = engine, if_exists = 'append', chunksize = 1000, index=False)
```

```python

dfSetParts = legoDf[['PartID','SetNumber', 'Quantity']]
dfSetParts.drop_duplicates(inplace=True)
dfSetParts.to_sql('PartSets', con = engine, if_exists = 'append', chunksize = 1000, index=False)
```

To have an example of the QUERY see below code: 

```python

connection = sqlite3.connect('bd.db')
my_cursor = connection.execute("SELECT * from Sets where binned = ? and Name LIKE ?", ['Moderate','%car%'])
setList = my_cursor.fetchall()
setList
```

We can also see the above results in a table.

```python

my_cursor = connection.execute("SELECT p.* from PartSets ps inner join Parts p on ps.PartId = p.PartId where ps.SetNumber = ?", ['10012-1'])
partList = my_cursor.fetchall()
partList
```

## Data Exploration and Analysis



## Conclusion

In this demo final project, we have wrangled several data sets consisting of over 15,000 LEGO sets, their parts, quantities needed, colors, etc. We have followed the steps of the data analysis workflow, starting with data ingestion, wrangling and cleaning, and exploration and analysis before moving on to the BIG QUERY. In the end, we were able to pull all needed pieces depending on the difficulty of the user's input in order to retreieve the wanted set.
