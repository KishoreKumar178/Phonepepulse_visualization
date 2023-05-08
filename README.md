# Phonepepulse_visualization

I have created the dashboard for phonepe pulse data.
It consists of 4 parts
*	Geo visualizations
*	Transaction analysis
*	User analysis
*	Top 10 Data

# Geo Visualization
It consists of year and Quarter wise transaction data in the India map based on
states and districts.
 
# Transaction analysis
It has 3 Tabs,
*	Overall
*	State
*	District
Each tab will give you insights about the transaction data in the particular Transaction mode.
 
# User Analysis
It has 3 Tabs,
*	Overall
*	State
*	District
*Each tab will give you insights about the user data.
   
# Top 10 Data
It has 2 Tabs,
*	Overall
*	State
*Each tab will give you insights about Top 10 data on transaction and user base


# Approach
*	Clone the data from the phonepse_pulse Github repository to the local device.
*	Converted the unstructured data to a structured pandas data frame through python programming.
*	Uploaded the data frames to the mysql server with the help of pymysql.
*	Creating an app with the help of streamlit.
*	Use plotly for the charts and maps.
*	For each data I have crated a query to get data from database.
*	Took latitude and longitude data from the web and done basic data formatting and cleaning.
*	Then plot the geospatial data with the help of plotly.
 
 
