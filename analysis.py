import streamlit as st
import pandas
import plotly.express as px
st.title('Analytics Dashboard')
st.caption('Haven Analytics')
st.set_page_config( layout = 'wide')
df = pandas.read_csv('data/train.csv')
df = df.drop(columns = ['Row ID', 'Order ID','Ship Date','Ship Mode','Customer ID','Country','Postal Code','Product ID','Customer Name'])

print(df.info())


df['Order Date'] = df['Order Date'].astype(str).str.strip()
df['Order Date'] = pandas.to_datetime(df['Order Date'], errors = 'coerce')
df.dropna(subset=['Order Date'])

st.sidebar.header('Filter')
category = st.sidebar.multiselect('Select Category', options = df['Category'].unique(), default = df['Category'].unique())
region = st.sidebar.multiselect('Select Region', options = df['Region'].unique(), default = df['Region'].unique())
min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
date_range = st.sidebar.date_input('Select Order Date Range', value=(min_date, max_date), min_value = min_date, max_value = max_date )


if len(date_range) == 2:
	start_date, end_date = date_range
else:
	start_date = end_date = date_range

filtered_df = df[(df['Region'].isin(region))&
(df['Category'].isin(category)) & 
(df['Order Date'] >= pandas.to_datetime(start_date	))&
 (df['Order Date'] <= pandas.to_datetime(end_date)) ]


col1, col2, = st.columns(2)
col1.metric("Total Sales",  f"{filtered_df['Sales'].sum():.2f}")
col2.metric("Orders", f"{filtered_df.shape[0]}")

col3, col4 = st.columns(2)
category_data =  filtered_df.groupby('Category')['Sales'].sum().reset_index()

fig1 = px.pie(
	category_data, 
	names = "Category",
	values = 'Sales', 
	title= 'Sales by Category'
	)
regional_data = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig2 = px.pie(
	regional_data, 
	names = 'Region',
	values = 'Sales',
	title = 'Sales by Region'
	)

col4.plotly_chart(fig1, use_container_width = True)
col3.plotly_chart(fig2, use_container_width = True)

filtered_df['Month'] = filtered_df['Order Date'].dt.to_period("M")
monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()

monthly_sales['Month'] = monthly_sales['Month'].astype(str)

fig3 = px.line(
monthly_sales, 
x = 'Month',
y = 'Sales',
title = 'Monthly Salary trend'
	)

st.plotly_chart(fig3, use_container_width=True)
