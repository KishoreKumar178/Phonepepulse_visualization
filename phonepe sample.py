import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pymysql
#connecting Databse
con = pymysql.connect(host = "localhost",
                      user = "root",
                      password = "kishore123",
                      db = "phonepe_data")
cursor = con.cursor()


states =('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
          'bihar', 'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 
          'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 
          'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 
          'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry',
           'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 
           'uttarakhand', 'west-bengal'
           )
modes= ('Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services', 'Others')

#creating webpage
st.set_page_config(layout="wide")
st.title(":blue[Phonpe visualization]")
st.write("This visualization helps to get insights about phonepe data")
st.header(":green[Trend on phonepe]")
parameter = st.radio("Select the parameter",("Transactions","Users"))
if parameter == "Transactions":
    st.write ("Transactions on the way")
elif parameter == "Users":
    st.write("Users on the way")

col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("Select the year", (2018,2019,2020,2021,2022))
with col2:
    quarter = st.selectbox("Select the quarter",(1,2,3,4))

df = pd.read_csv("D:\Git\Phonepepulse_visualization\Phonepepulse_visualization\Data\Trans_lat_lan.csv")

fig = px.choropleth(
    df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='ST_NM',
    color='transaction_count',
    color_continuous_scale='Viridis'
)

fig.update_geos(fitbounds="locations", visible=False)


st.plotly_chart(fig)
#########################################Transaction data######################################################################
st.header(":red[Transactions]")
tab1, tab2, tab3= st.tabs(["Overall", "State", "District"])

with tab1:
   st.header("Overall")
   mode = st.selectbox("Select the Mode", modes)
   df = cursor.execute("SELECT * FROM india_transaction_data where Name = '{}'".format(mode))
   output = cursor.fetchall()
   df = pd.DataFrame(output)
   title = [i[0] for i in cursor.description]
   df.columns = title
   df["new_year"] = df["year"] + "Q"+ df["quarter"]
   #st.dataframe(df)
   col1, col2 = st.columns(2)
   with col1:
       fig = px.bar(df, x= "new_year", y= "count",labels= {"new_year":"Year", "count":"Transaction count"},
                    title= "Transaction count VS Year", color="count",color_continuous_scale="Viridis")
       st.plotly_chart(fig)
     
   with col2:
       fig = px.bar(df, x= "new_year", y= "amount", labels= {"new_year":"Year", "amount":"Transaction value"},
                    title= "Transaction Value VS Year", color="amount", color_continuous_scale="purp")
       st.plotly_chart(fig)
   col1, col2 = st.columns(2)
   with col1:
       year = st.selectbox("Select the year", (2018,2019,2020,2021,2022),key=1)
       df = cursor.execute("SELECT * FROM india_transaction_data where year = {} and quarter = {}".format(year,quarter))
       output = cursor.fetchall()
       df = pd.DataFrame(output)
       title = [i[0] for i in cursor.description]
       df.columns = title
       df["new_year"] = df["year"] + "Q"+ df["quarter"]
       value = df["count"]
       lable = df["Name"]
       fig1 = go.Figure(data=[go.Pie(labels=lable, values=value, hole=.5, title= "Transaction Count")])
       fig1.update_traces(textposition='outside', textinfo='percent+label')
       fig1.update_layout(legend=dict(x=0,y=1))
       st.plotly_chart(fig1)
   with col2:
       quarter = st.selectbox("Select the quarter",(1,2,3,4),key=2)
       value = df["count"]
       lable = df["Name"]
       fig1 = go.Figure(data=[go.Pie(labels=lable, values=value, hole=.5, title= "Transaction Value")])
       fig1.update_traces(textposition='outside', textinfo='percent+label')
       st.plotly_chart(fig1)
   df = cursor.execute("SELECT * FROM india_transaction_data")
   output = cursor.fetchall()
   df = pd.DataFrame(output)
   title = [i[0] for i in cursor.description]
   df.columns = title
   df["new_year"] = df["year"] + "Q"+ df["quarter"]
   fig= px.bar(df, x="Name", y="amount", color="Name",
       animation_frame="new_year", animation_group="Name", range_y=[0,700000000000], labels={"Name": "Transaction Mode","amount":"Transaction Value","new_year":"Year"},
       title= "Transaction mode vs Transaction value over time")
   st.plotly_chart(fig)

   

with tab2:
   st.header("State wise")
   col1, col2 = st.columns(2)
   with col1:
        t_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 3)
        t_mode = st.selectbox("Select the Mode", modes,key = 4)
   with col2:
        t_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 5)
   df = cursor.execute("SELECT * FROM transaction_data WHERE year={} and quarter = {} and Name =  '{}' ".format(t_year, t_quarter, t_mode))
   output = cursor.fetchall()
   df = pd.DataFrame(output)
   title = [i[0] for i in cursor.description]
   df.columns = title
   #st.dataframe(df)
   fig = px.bar(df, x= "state", y = "count", color= "state",labels={"state":"State","count":"Transaction Count"},
                title= "Statewise {} transaction count".format(t_mode),
                width=1200, height=800)
   fig.update_layout(xaxis_tickangle=-45)
   fig.update_layout(uniformtext_minsize=10)
   st.plotly_chart(fig)
   fig1 = px.bar(df, x= "state", y = "amount", color= "state",labels={"state":"State","amount":"Transaction Value"},
                title= "Statewise {} transaction value".format(t_mode),
                width=1200, height=800)
   fig1.update_layout(xaxis_tickangle=-45)
   fig1.update_layout(uniformtext_minsize=10)
   st.plotly_chart(fig1)
   
   

with tab3:
     st.header("District")
     col1, col2,col3 = st.columns(3)
     with col1:
         t_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 6)
     with col2:
         t_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 7)
     with col3:
         t_state = st.selectbox("Select the state",states,key = 8)

     df = cursor.execute("SELECT * FROM transaction_data WHERE year={} and quarter = {} and state =  '{}' ".format(t_year, t_quarter,t_state))
     output = cursor.fetchall()
     df = pd.DataFrame(output)
     title = [i[0] for i in cursor.description]
     df.columns = title
     #st.dataframe(df)
     fig = px.bar(df,x="Name",y="count",color= "Name", labels={"Name":"Transaction mode", "count":"Transaction count"}, title= "Transaction Count VS Transaction Mode")
     st.plotly_chart(fig)
     df = cursor.execute("SELECT * FROM map_transactions_district WHERE year={} and quarter = {} and state =  '{}' ".format(t_year, t_quarter,t_state))
     output = cursor.fetchall()
     df = pd.DataFrame(output)
     title = [i[0] for i in cursor.description]
     df.columns = title
     #st.dataframe(df)
     fig = px.bar(df, x = "district", y= "transaction_count", color="district",color_continuous_scale="viridis",width=1000, height=800,
                  labels={"district":"District", "transaction_count":"Transaction Count"}, title= "Districtwise Transaction count")
     st.plotly_chart(fig)
    

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@USER DATA@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
st.header("User")
tab1, tab2, tab3 = st.tabs(["Overall","State","District"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        df = cursor.execute("SELECT * FROM india_user_data")
        output = cursor.fetchall()
        df = pd.DataFrame(output)
        title = [i[0] for i in cursor.description]
        df.columns = title
        df["new_year"] = df["year"] + "Q"+ df["quarter"]
        fig = px.line(df,x="new_year", y ="RegisterdUsers", markers=True, labels={"new_year":"Year","RegisterdUsers": "Registered Users"},
                      title= "Growth of transactions" )
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_layout(uniformtext_minsize=10)
        st.plotly_chart(fig)
    with col2:
        fig = px.line(df,x="new_year", y = "appOpens", markers= True,labels={"new_year":"Year","appOpens": "App usage"},
                      title= "Growth of app usage")
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_layout(uniformtext_minsize=10)
        st.plotly_chart(fig)
    col1, col2 = st.columns(2)
    with col1:
        u_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 9)
    with col2:
        u_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 10)
    df = cursor.execute("SELECT * FROM india_users_brand_data where year= {} and quarter= {} ".format(u_year,u_quarter))
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    title = [i[0] for i in cursor.description]
    df.columns = title
    value = df["count"]
    lable = df["Brand"]
    fig1 = go.Figure(data=[go.Pie(labels=lable, values=value, hole=.5, title= "Transaction Count")])
    fig1.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(fig1)
    df = cursor.execute("SELECT * FROM user_data where year= {} and quarter= {}".format(u_year,u_quarter))
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    title = [i[0] for i in cursor.description]
    df.columns = title
    fig = px.bar(df, x = "state", y="RegisterdUsers", color="state",width=1000, height=800 ,
                 labels={"state":"State","RegisterdUsers":"Registered Users"}, title= "Statewise Registered Users", hover_data=['appOpens'])
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_layout(uniformtext_minsize=10)
    st.plotly_chart(fig)

with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        u_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 11)
    with col2:
        u_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 12)
    with col3:
        u_state = st.selectbox("Select the state",states,key = 13)
    df = cursor.execute("SELECT * FROM user_brand_data where year= {} and quarter= {} and state = '{}'".format(u_year,u_quarter,u_state))
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    title = [i[0] for i in cursor.description]
    df.columns = title
    col1, col2 = st.columns(2)
    value = df["count"]
    lable = df["Brand"]
    fig1 = go.Figure(data=[go.Pie(labels=lable, values=value, hole=.5, title= "Transaction Count")])
    fig1.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(fig1)
    df = cursor.execute("SELECT * FROM user_data where state = '{}'".format(u_state))
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    title = [i[0] for i in cursor.description]
    df.columns = title
    df["new_year"] = df["year"] + "Q"+ df["quarter"]
    fig = px.bar(df, x="new_year",y=["RegisterdUsers","appOpens"], barmode="group", labels=dict(new_year= "Year", RegisterdUsers= "Registered Users",appOpens = "Appopens") , title= "Registered Users & appopens")
    st.plotly_chart(fig)
    
with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        u_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 14)
    with col2:
        u_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 15)
    with col3:
        u_state = st.selectbox("Select the state",states,key = 16)
    df = cursor.execute("SELECT * FROM map_users_data_districts where year= {} and quarter= {} and state = '{}'".format(u_year,u_quarter,u_state))
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    title = [i[0] for i in cursor.description]
    df.columns = title
    col1, col2 = st.columns(2)
    fig1 = px.bar(df, x = "district", y = "registered_users", color="district", width=1000, labels={"district":"Districts", "registered_users":"Registered Users"},
                  title="Districtwise Registered Users")
    fig1.update_layout(xaxis_tickangle=-45)
    fig1.update_layout(uniformtext_minsize=10)
    st.plotly_chart(fig1)

    df = cursor.execute("SELECT * FROM map_users_data_districts where state = '{}'".format(u_state))
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    title = [i[0] for i in cursor.description]
    df.columns = title

    df["new_year"] = df["year"] + "Q"+ df["quarter"]
    fig= px.bar(df, x="district", y="appopens", color="district",width= 1000,
       animation_frame="new_year", animation_group="district", range_y=[0,100000000], labels={"district":"Districts", "new_year": "year", "appopens": "Appopens"},title="Districtwise appopening trend")
    st.plotly_chart(fig)
   
    
    
st.header("Top 10 Data")
tab1, tab2= st.tabs(["overall","State"])
with tab1:
     col1, col2 = st.columns(2)
     with col1:
         T_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 17)
     with col2:
         T_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 18)
     df = cursor.execute("SELECT state, count ,amount FROM top_10_states where year = {} and quarter = {}".format(T_year,T_quarter))
     output = cursor.fetchall()
     df = pd.DataFrame(output)     
     title = ["State", "Transactions_count", "Transactions_value"]
     rank = [i for i in range (1,11)]
     df.columns = title
     df.insert(0, "Rank", rank , True)
     hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
     st.markdown(hide_table_row_index, unsafe_allow_html=True)
     st.header("Transactions")
     col1, col2, col3 = st.columns(3)
     with col1:
         st.header("Top 10 States")
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         df["Transactions_value"] = df["Transactions_value"].div(1000000000)
         df["Transactions_value"]= df["Transactions_value"].round(2)
         df["Transactions_value"] = df["Transactions_value"].map(str) + "B"
         df["Transactions_count"] = df["Transactions_count"].div(1000000)
         df["Transactions_count"]= df["Transactions_count"].round(2)
         df["Transactions_count"] = df["Transactions_count"].map(str) + "M"
         st.table(df)
     with col2:
         st.header("Top 10 Districts")
         df = cursor.execute("SELECT districts, count ,amount FROM top_10_districts where year = {} and quarter = {}".format(T_year,T_quarter))
         output = cursor.fetchall()
         df = pd.DataFrame(output)     
         title = ["State", "Transactions_count", "Transactions_value"]
         rank = [i for i in range (1,11)]
         df.columns = title
         df.insert(0, "Rank", rank , True)
         df["Transactions_value"] = df["Transactions_value"].div(1000000000)
         df["Transactions_value"]= df["Transactions_value"].round(2)
         df["Transactions_value"] = df["Transactions_value"].map(str) + "B"
         df["Transactions_count"] = df["Transactions_count"].div(1000000)
         df["Transactions_count"]= df["Transactions_count"].round(2)
         df["Transactions_count"] = df["Transactions_count"].map(str) + "M"
         
         hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
     with col3:
         st.header("Top 10 Pincodes")
         df = cursor.execute("SELECT pincodes, count ,amount FROM top_10_pincodes where year = {} and quarter = {}".format(T_year,T_quarter))
         output = cursor.fetchall()
         df = pd.DataFrame(output)     
         title = ["State", "Transactions_count", "Transactions_value"]
         rank = [i for i in range (1,11)]
         df.columns = title
         df.insert(0, "Rank", rank , True)
         df["Transactions_value"] = df["Transactions_value"].div(1000000000)
         df["Transactions_value"]= df["Transactions_value"].round(2)
         df["Transactions_value"] = df["Transactions_value"].map(str) + "B"
         df["Transactions_count"] = df["Transactions_count"].div(1000000)
         df["Transactions_count"]= df["Transactions_count"].round(2)
         df["Transactions_count"] = df["Transactions_count"].map(str) + "M"
         
         hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
     st.header("Top 10 User Data")
     df = cursor.execute("SELECT state, Registeredusers FROM top_10_states_user where year = {} and quarter = {}".format(T_year,T_quarter))
     output = cursor.fetchall()
     df = pd.DataFrame(output)     
     title = ["State", "Registered Users"]
     rank = [i for i in range (1,11)]
     df.columns = title
     df.insert(0, "Rank", rank , True)
     hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
     st.markdown(hide_table_row_index, unsafe_allow_html=True)
     col1, col2, col3 = st.columns(3)
     with col1:
         st.header("Top 10 States")
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
     with col2:
         st.header("Top 10 Districts")
         df = cursor.execute("SELECT districts, Registeredusers FROM top_10_districts_user where year = {} and quarter = {}".format(T_year,T_quarter))
         output = cursor.fetchall()
         df = pd.DataFrame(output)     
         title = ["State", "Registered Users"]
         rank = [i for i in range (1,11)]
         df.columns = title
         df.insert(0, "Rank", rank , True)         
         hide_table_row_index = """
              <style>
             thead tr th:first-child {display:none}
             tbody th {display:none}
             </style>
             """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
     with col3:
         st.header("Top 10 Pincodes")
         df = cursor.execute("SELECT pincodes, Registeredusers FROM top_10_pincodes_user where year = {} and quarter = {}".format(T_year,T_quarter))
         output = cursor.fetchall()
         df = pd.DataFrame(output)     
         title = ["State", "Registered Users"]
         rank = [i for i in range (1,11)]
         df.columns = title
         df.insert(0, "Rank", rank , True)         
         hide_table_row_index = """
             <style>
             thead tr th:first-child {display:none}
             tbody th {display:none}
             </style>
             """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
with tab2:
     col1, col2, col3 = st.columns(3)
     with col1:
         T_year = st.selectbox("Select the year", (2018,2019,2020,2021,2022), key= 19)
     with col2:
         T_quarter = st.selectbox("Select the quarter",(1,2,3,4),key = 20)
     with col3:
         T_state = st.selectbox("Select the state",states,key = 21)
     df = cursor.execute("SELECT district, count ,amount FROM topstates_transaction where year = {} and quarter = {} and state = '{}' limit 3".format(T_year,T_quarter,T_state))
     output = cursor.fetchall()
     df = pd.DataFrame(output)     
     title = ["Districts","Transactions_count", "Transactions_value"]
     rank = [i for i in range (1,4)]
     df.columns = title
     df.insert(0, "Rank", rank , True)
     hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
     st.markdown(hide_table_row_index, unsafe_allow_html=True)
     st.header("Transactions")
     col1, col2 = st.columns(2)
     with col1:
         st.header("Top 3 Districts")
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         df["Transactions_value"] = df["Transactions_value"].div(10000000)
         df["Transactions_value"]= df["Transactions_value"].round(2)
         df["Transactions_value"] = df["Transactions_value"].map(str) + "Cr"
         df["Transactions_count"] = df["Transactions_count"].div(100000)
         df["Transactions_count"]= df["Transactions_count"].round(2)
         df["Transactions_count"] = df["Transactions_count"].map(str) + "L"
         st.table(df)
     with col2:
         st.header("Top 3 Pincodes")
         df = cursor.execute("SELECT pincodes, count, amount FROM toppincodes_transaction where year = {} and quarter = {} and state = '{}' limit 3".format(T_year,T_quarter,T_state))
         output = cursor.fetchall()
         df = pd.DataFrame(output)     
         title = ["Pincodes", "Transactions_count", "Transactions_value"]
         rank = [i for i in range (1,4)]
         df.columns = title
         df.insert(0, "Rank", rank , True)
         df["Transactions_value"] = df["Transactions_value"].div(10000000)
         df["Transactions_value"]= df["Transactions_value"].round(2)
         df["Transactions_value"] = df["Transactions_value"].map(str) + "Cr"
         df["Transactions_count"] = df["Transactions_count"].div(100000)
         df["Transactions_count"]= df["Transactions_count"].round(2)
         df["Transactions_count"] = df["Transactions_count"].map(str) + "L"
         
         hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
     st.header("Top 10 User Data")
     df = cursor.execute("SELECT state, Registeredusers FROM topstates_user where year = {} and quarter = {} and state = '{}' limit 3".format(T_year,T_quarter, T_state))
     output = cursor.fetchall()
     df = pd.DataFrame(output)     
     title = ["State", "Registered Users"]
     rank = [i for i in range (1,4)]
     df.columns = title
     df.insert(0, "Rank", rank , True)
     hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
     st.markdown(hide_table_row_index, unsafe_allow_html=True)
     col1, col2 = st.columns(2)
     with col1:
         st.header("Top 10 Disricts")
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
     with col2:
         st.header("Top 10 Pincodes")
         df = cursor.execute("SELECT district, Registeredusers FROM topstates_user where year = {} and quarter = {} and state = '{}' limit 3".format(T_year,T_quarter,T_state))
         output = cursor.fetchall()
         df = pd.DataFrame(output)     
         title = ["State", "Registered Users"]
         rank = [i for i in range (1,4)]
         df.columns = title
         df.insert(0, "Rank", rank , True)         
         hide_table_row_index = """
              <style>
             thead tr th:first-child {display:none}
             tbody th {display:none}
             </style>
             """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)



con.close()