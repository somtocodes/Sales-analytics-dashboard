import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
	page_title = "Haven Analytics Dahsboard"
	layout = 'wide'
)

st.title('Analytics Dashboard')
st.caption('Interactive sales dashboard')

#load and clean data
@st.cache_data
def load_data():
	df = pd.read_csv('data/train.csv')
	
	#drop unneccessary columns
	columns_to_drop =  ['Row ID', 'Order ID','Ship Date','Ship Mode','Customer ID','Country','Postal Code','Product ID','Customer Name'])
	df =  df.drop(columns = columns_to_drop)
	
	df['Order Date'] = pandas.to_datetime(df['Order Date'], errors = 'coerce')
	df.dropna(subset=['Order Date'])

	return df
	
df = load_data()
#sidebar filters
st.sidebar.header('Filters')
category = st.sidebar.multiselect(
	'Select Category', 
	options = df['Category'].unique(),
	default = df['Category'].unique()
)
region = st.sidebar.multiselect(
	'Select Region',
	options = df['Region'].unique(),
	default = df['Region'].unique()
)
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()

date_range = st.sidebar.date_input(
	'Select Order Date Range',
	value=(min_date, max_date),
	min_value = min_date,
	max_value = max_date
)

# Apply filters
if len(date_range) == 2:
	start_date, end_date = date_range
else:
	start_date = end_date = date_range

filtered_df = df[
(df['Region'].isin(region))&
(df['Category'].isin(category)) & 
(df['Order Date'].dt.date >= start_date)&
(df['Order Date'].dt.date <= end_date)]


col1, col2, col3 = st.columns(3)
col1.metric("Total Sales",  f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Orders", f"{filtered_df.shape[0]:,}")
col3.metric("Averge Order Value", f"${filtered_df['Sales'].mean():,.2f}" if not filtered_df.empty else "$0.00" )

colA, colB = st.columns(2)
# Sales by category
category_data =  filtered_df.groupby('Category')['Sales'].sum().reset_index()

fig1 = px.pie(
	category_data, 
	names = "Category",
	values = 'Sales', 
	title= 'Sales Distribution by Category',
	hole = 0.4
)
regional_data = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig2 = px.pie(
	regional_data, 
	names = 'Region',
	values = 'Sales',
	title = 'Sales Distribution by Region',
	hole = 0.4
)

colA.plotly_chart(fig1, use_container_width = True)
colB.plotly_chart(fig2, use_container_width = True)

# Monthly Sales Trend
filtered_df['Month'] = filtered_df['Order Date'].dt.to_period("M").astype(str)
monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()

monthly_sales['Month'] = monthly_sales['Month'].astype(str)

fig3 = px.line(
	monthly_sales, 
	x = 'Month',
	y = 'Sales',
	title = 'Monthly Salary trend',
	markers = True
)

fig3.update_layout(xaxis_title='Month', yaxis_title="Sales ($)")
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View Filtered Data"):
	st.dataframe(filtered_df, use_container_width = True)
