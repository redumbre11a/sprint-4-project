import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

df['manufacturer'] = df['model'].apply(lambda x:
x.split()[0])


# Replace missing values in the model_year column with median by car model
df['model_year'] = df['model_year'].fillna(df.groupby(['model'])['model_year'].transform('median'))

# Replace missing values in the cylinders column with median by car model
df['cylinders'] = df['cylinders'].fillna(df.groupby(['model'])['cylinders'].transform('median'))

# Replace missing values in the odometer column with median by model_year
df['odometer'] = df['odometer'].fillna(df.groupby(['model_year'])['odometer'].transform('median'))

# Replace missing values in the paint color column with "unknown"
df['paint_color'].fillna('unknown', inplace=True)

# Replace missing values in the is_4wd column with 0
df['is_4wd'].fillna(0, inplace=True)


# Drop rows with missing odometer values
df.dropna(subset=['odometer'], inplace=True)

# Convert 'model_year' column to datetime
df['model_year'] = pd.to_datetime(df['model_year'], format='%Y')

# Extract only the year from the datetime
df['model_year'] = df['model_year'].dt.year


# Perform exploratory analysis

st.header('Car Analysis App')
st.subheader('Exploring Car Advertisement Data')

# data viewer
# create a text header above the dataframe
st.header('Data Viewer') 
# display the dataframe with streamlit
st.dataframe(df)

# vehicle types by manufacturer
st.header('Vehicle types by manufacturer')
# create a plotly histogram figure
fig = px.histogram(df, x='manufacturer', color='type')
# display the figure with streamlit
st.write(fig)

# histogram of condition vs model year
st.header('Histogram of `condition` vs `model_year`')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

# histogram of car prices
st.header('Histogram of Car Prices')
fig = px.histogram(df, x='price')
st.plotly_chart(fig)

# scatter plot of mileage vs price
st.header('Scatter Plot of Mileage vs Price')
fig = px.scatter(df, x='odometer', y='price')
st.plotly_chart(fig)

# compare price distribution between manufacturers
st.header('Compare price distribution between manufacturers')
# get a list of car manufactureres
manufac_list = sorted(df['manufacturer'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                                label='Select manufacturer 1', # title of the select box
                                options=manufac_list, #options listed in the select box
                                index=manufac_list.index('chevrolet') # default pre-selected option
                                )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                                label='Select manufacturer 2',
                                options=manufac_list,
                                index=manufac_list.index('hyundai')
                                )
#filter the dataframe
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                    x='price',
                    nbins=30,
                    color='manufacturer',
                    histnorm=histnorm,
                    barmode='overlay')

# display the figure with streamlit
st.write(fig)