# importing libraries
import pandas as pd
import os
from sqlalchemy import create_engine
import plotly.express as px
import pathlib as path
import pymysql
import warnings
warnings.filterwarnings("ignore")
#path for the data
u_p = r"D:\Git\pulse\data\aggregated\user\country\india\state"
t_p = r"D:\Git\pulse\data\aggregated\transaction\country\india\state"
map_t_p = r"D:\Git\pulse\data\map\transaction\hover\country\india"
map_u_p = r"D:\Git\pulse\data\map\user\hover\country\india"

#creating dataframes
transactions_data = pd.DataFrame({})
india_transactions_data = pd.DataFrame({})
india_users_data = pd.DataFrame({})
Users_data = pd.DataFrame({})
Users_brand_data = pd.DataFrame({})
top_10_states = pd.DataFrame({})
top_10_districts = pd.DataFrame({})
top_10_pincodes = pd.DataFrame({})
top_10_states_user = pd.DataFrame({})
top_10_districts_user=pd.DataFrame({})
top_10_pincodes_user = pd.DataFrame({})
map_transactions_state = pd.DataFrame({})
map_transactions_district = pd.DataFrame({})
map_users_data_state = pd.DataFrame({})
map_users_data_district = pd.DataFrame({})
india_users_brand_data = pd.DataFrame({})
topstates_transaction = pd.DataFrame({})
toppincodes_transaction = pd.DataFrame({})
topstates_user = pd.DataFrame({})
toppincodes_user = pd.DataFrame({})

# Define the function to store data in pandas DF
a = os.listdir(t_p)
country = os.listdir(u_p)
def transaction_data (state, year, quarter, path):
    global transactions_data
    data = pd.read_json(path)
    for value in data.data.transactionData:
        row_data = {"Name":value["name"], "count": value["paymentInstruments"][0]["count"], 
                "amount":value["paymentInstruments"][0]["amount"], "state": state, "year": year, "quarter":quarter}
        transactions_data = transactions_data.append(row_data, ignore_index = True)

def india_transaction_data (year, quarter):
    global india_transactions_data
    data = pd.read_json(r"D:\Git\pulse\data\aggregated\transaction\country\india"+"\\"+year+"\\"+quarter+".json")
    for value in data.data.transactionData:
        row_data = {"Name":value["name"], "count": value["paymentInstruments"][0]["count"], 
                "amount":value["paymentInstruments"][0]["amount"], "year": year, "quarter":quarter}
        india_transactions_data = india_transactions_data.append(row_data, ignore_index = True)

# To call the function
for i in a:
    b = os.listdir(t_p+"\\"+i)
    for j in b:
        c = os.listdir(t_p+"\\"+i+"\\"+j)
        for k in c:
            T_path = t_p+"\\"+i+"\\"+j+"\\"+k
            l = path.Path(T_path).stem
            transaction_data (i,j,l,T_path)

def User_Data (state,year,quarter,path):
    global Users_data
    data = pd.read_json(path)
    row_data = {"RegisterdUsers":data["data"]["aggregated"]["registeredUsers"], 
                "appOpens": data["data"]["aggregated"]["appOpens"],
                "state": state, "year": year, "quarter":quarter}
    Users_data = Users_data.append(row_data, ignore_index = True)

def india_User_Data (year,quarter):
    global india_users_data
    data = pd.read_json(r"D:\Git\pulse\data\aggregated\user\country\india"+"\\"+year+"\\"+quarter+".json")
    row_data = {"RegisterdUsers":data["data"]["aggregated"]["registeredUsers"], 
                "appOpens": data["data"]["aggregated"]["appOpens"],
                 "year": year, "quarter":quarter}
    india_users_data = india_users_data.append(row_data, ignore_index = True)

def user_brand_data (state,year,quarter,path):
    global Users_brand_data
    data = pd.read_json(path)
    if data.data.usersByDevice == None:
        pass
    else:
        for i in data.data.usersByDevice:
            row_data ={"Brand": i["brand"],"count":i["count"], "Percentage":i["percentage"],
                  "state":state,"year":year,"quarter":quarter}
            Users_brand_data = Users_brand_data.append(row_data, ignore_index = True)

def india_user_brand_data (year,quarter):
    global india_users_brand_data
    data = pd.read_json(r"D:\Git\pulse\data\aggregated\user\country\india"+"\\"+year+"\\"+quarter+".json")
    if data.data.usersByDevice == None:
        pass
    else:
        for i in data.data.usersByDevice:
            row_data ={"Brand": i["brand"],"count":i["count"], "Percentage":i["percentage"],
                  "year":year,"quarter":quarter}
            india_users_brand_data = india_users_brand_data.append(row_data, ignore_index = True)

for i in country:
    print(i)
    year = os.listdir(u_p+"\\"+i)
    for j in year:
        print(j)
        quarter = os.listdir(u_p+"\\"+i+"\\"+j)
        for k in quarter:
            u_path = u_p+"\\"+i+"\\"+j+"\\"+k
            print(u_path)
            l = path.Path(u_path).stem
            User_Data (i,j,l,u_path)
            user_brand_data (i,j,l,u_path)

def Top10_states(year,quarter,path):
    global top_10_states
    df = pd.read_json(path)
    for i in df.data.states:
        row_data = {"state":i["entityName"], "count":i['metric']["count"], "amount": i['metric']["amount"],"year":year, "quarter":quarter}
        top_10_states = top_10_states.append(row_data, ignore_index = True)

def Top10_districts(year,quarter,path):
    global top_10_districts
    df = pd.read_json(path)
    for i in df.data.districts:
        row_data = {"districts":i["entityName"], "count":i['metric']["count"], "amount": i['metric']["amount"],"year":year, "quarter":quarter}
        top_10_districts = top_10_districts.append(row_data, ignore_index = True)

def Top10_pincodes(year,quarter,path):
    global top_10_pincodes
    df = pd.read_json(path)
    for i in df.data.pincodes:
        row_data = {"pincodes":i["entityName"], "count":i['metric']["count"], "amount": i['metric']["amount"],"year":year, "quarter":quarter}
        top_10_pincodes = top_10_pincodes.append(row_data, ignore_index = True) 

def Topstates_trans(state,year,quarter,path):
    global topstates_transaction
    global toppincodes_transaction
    df = pd.read_json(path)
    for i in df.data.districts:
        row_data = {"state": state,"district":i["entityName"], "count":i['metric']["count"], 
                    "amount": i['metric']["amount"],"year":year, "quarter":quarter}
        topstates_transaction = topstates_transaction.append(row_data, ignore_index = True)
    for j in df.data.pincodes:
        row_data = {"state": state,"pincodes":j["entityName"], "count":j['metric']["count"], 
                    "amount": i['metric']["amount"],"year":year, "quarter":quarter}
        toppincodes_transaction = toppincodes_transaction.append(row_data, ignore_index = True)  

def Top10_states_user(year,quarter,path):
    global top_10_states_user
    df = pd.read_json(path)
    for i in df.data.states:
        row_data = {"state":i["name"], "Registeredusers":i["registeredUsers"],"year":year, "quarter":quarter}
        top_10_states_user = top_10_states_user.append(row_data, ignore_index = True)

def Top10_districts_user(year,quarter,path):
    global top_10_districts_user
    df = pd.read_json(path)
    for i in df.data.districts:
        row_data = {"districts":i["name"], "Registeredusers":i["registeredUsers"],"year":year, "quarter":quarter}
        top_10_districts_user = top_10_districts_user.append(row_data, ignore_index = True)

def Top10_pincodes_user(year,quarter,path):
    global top_10_pincodes_user
    df = pd.read_json(path)
    for i in df.data.pincodes:
        row_data = {"pincodes":i["name"], "Registeredusers":i["registeredUsers"],"year":year, "quarter":quarter}
        top_10_pincodes_user = top_10_pincodes_user.append(row_data, ignore_index = True)  

def Topstates_user(state,year,quarter,path):
    global topstates_user
    global toppincodes_user
    df = pd.read_json(path)
    for i in df.data.districts:
        row_data = {"state":state,"district":i["name"], "Registeredusers":i["registeredUsers"],"year":year, "quarter":quarter}
        topstates_user = topstates_user.append(row_data, ignore_index = True)
    for j in df.data.pincodes:
        row_data = {"state":state,"pincodes":j["name"], "Registeredusers":j["registeredUsers"],"year":year, "quarter":quarter}
        toppincodes_user = toppincodes_user.append(row_data, ignore_index = True)

list1 = os.listdir(r"D:\Git\pulse\data\top\transaction\country\india")
for i in range(len(list1)-1):
    a = r"D:\Git\pulse\data\top\transaction\country\india"+"\\"+list1[i]
    for j in os.listdir(a):
        TS_path = r"D:\Git\pulse\data\top\transaction\country\india"+"\\"+list1[i]+"\\"+j
        US_path = r"D:\Git\pulse\data\top\user\country\india"+"\\"+list1[i]+"\\"+j
        l = path.Path(TS_path).stem
        Top10_states(list1[i],l,TS_path)
        Top10_districts(list1[i],l,TS_path)
        Top10_pincodes(list1[i],l,TS_path)
        Top10_states_user(list1[i],l,US_path)
        Top10_districts_user(list1[i],l,US_path)
        Top10_pincodes_user(list1[i],l,US_path)
        india_transaction_data(list1[i],l)
        india_User_Data (list1[i],l)
        india_user_brand_data (list1[i],l)

def map_transaction_state(year,quarter,path):
    global map_transactions_state
    data = pd.read_json(path)
    for i in data["data"]["hoverDataList"]:
        row_data = {"state":i["name"], "transaction_count":i["metric"][0]["count"], "transaction_vale": i["metric"][0]["amount"], "year": year, "quarter": quarter}
        map_transactions_state = map_transactions_state.append(row_data, ignore_index = True)
def map_transaction_district(state,year,quarter,path):
    global map_transactions_district
    data = pd.read_json(path)
    for i in data["data"]["hoverDataList"]:
        row_data = {"state":state, "district":i["name"], "transaction_count":i["metric"][0]["count"], "transaction_vale": i["metric"][0]["amount"], "year": year, "quarter": quarter}
        map_transactions_district = map_transactions_district.append(row_data, ignore_index = True)
def map_user_data_state(year,quarter,path):
    global map_users_data_state
    data = pd.read_json(path)
    for i in data["data"]["hoverData"]:
        row_data = {"state":i, "registered_users":data["data"]["hoverData"][i]['registeredUsers'], 
                    "appopens": data["data"]["hoverData"][i]["appOpens"], "year": year, "quarter": quarter}
        map_users_data_state = map_users_data_state.append(row_data, ignore_index = True)
def map_user_data_district(state,year,quarter,path):
    global map_users_data_district
    data = pd.read_json(path)
    for i in data["data"]["hoverData"]:
        row_data = {"state":state,"district":i, "registered_users":data["data"]["hoverData"][i]['registeredUsers'], 
                    "appopens": data["data"]["hoverData"][i]["appOpens"], "year": year, "quarter": quarter}
        map_users_data_district = map_users_data_district.append(row_data, ignore_index = True)
A = os.listdir(map_t_p)
for i in A:
    if i != 'state':
        b = os.listdir(map_t_p +"\\"+i)
        for j in b:
            n_path = map_t_p +"\\"+i+"\\"+j
            u_path = map_u_p +"\\"+i+"\\"+j
            l = path.Path(n_path).stem
            map_transaction_state(i,l,n_path)
            map_user_data_state(i,l,u_path)
    else:
        b = os.listdir(map_t_p +"\\"+i)
        for j in b:
            year = os.listdir(map_t_p +"\\"+i+"\\"+j)
            for k in year:
                quarter = os.listdir(map_t_p +"\\"+i+"\\"+j+"\\"+k)
                for l in quarter:
                    s_path = map_t_p +"\\"+i+"\\"+j+"\\"+k+"\\"+l
                    u_path = map_u_p +"\\"+i+"\\"+j+"\\"+k+"\\"+l
                    TT_path = (r"D:\Git\pulse\data\top\transaction\country\india") + "\\"+i+"\\"+j+"\\"+k+"\\"+l
                    UT_path = (r"D:\Git\pulse\data\top\user\country\india") + "\\"+i+"\\"+j+"\\"+k+"\\"+l
                    m = path.Path(s_path).stem
                    map_transaction_district(j,k,m,s_path)
                    map_user_data_district(j,k,m,u_path)
                    Topstates_trans(j,k,m,TT_path)
                    Topstates_user(j,k,m,UT_path)

#storing dataframes in sql database
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="root", 
                        pw="kishore123",
                        db="phonepe_data"))
transactions_data.to_sql("transaction_data", con = engine, if_exists="append", chunksize = 1000)
Users_data.to_sql("user_data", con = engine, if_exists="append", chunksize = 1000)
Users_brand_data.to_sql("user_brand_data", con = engine, if_exists="append", chunksize = 1000)
top_10_states.to_sql("top_10_states", con = engine, if_exists="append", chunksize = 1000)
top_10_districts.to_sql("top_10_districts", con = engine, if_exists="append", chunksize = 1000)
top_10_pincodes.to_sql("top_10_pincodes", con = engine, if_exists="append", chunksize = 1000)
india_transactions_data.to_sql("india_transaction_data", con = engine, if_exists="append", chunksize = 1000)
india_users_data.to_sql("india_user_data", con = engine, if_exists="append", chunksize = 1000)
map_transactions_state.to_sql("map_transactions_state", con = engine, if_exists="append", chunksize = 1000)
map_transactions_district.to_sql("map_transactions_district", con = engine, if_exists="append", chunksize = 1000)
map_users_data_state.to_sql("map_users_data_state", con = engine, if_exists="append", chunksize = 1000)
map_users_data_district.to_sql("map_users_data_districts", con = engine, if_exists="append", chunksize = 1000)
india_users_brand_data.to_sql("india_users_brand_data", con = engine, if_exists="append", chunksize = 1000)
top_10_states_user.to_sql("top_10_states_user", con = engine, if_exists="append", chunksize = 1000)
top_10_districts_user.to_sql("top_10_districts_user", con = engine, if_exists="append", chunksize = 1000)
top_10_pincodes_user.to_sql("top_10_pincodes_user", con = engine, if_exists="append", chunksize = 1000)
topstates_transaction.to_sql("topstates_transaction", con = engine, if_exists="append", chunksize = 1000)
toppincodes_transaction.to_sql("toppincodes_transaction", con = engine, if_exists="append", chunksize = 1000)
topstates_user.to_sql("topstates_user", con = engine, if_exists="append", chunksize = 1000)
toppincodes_user.to_sql("toppincodes_user", con = engine, if_exists="append", chunksize = 1000)