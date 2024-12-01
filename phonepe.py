
    
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
import ssl
import urllib3
from PIL import Image

# Data frame creation

# sql connection

mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="8997",
                        database="phonepe_data",
                        port="5432")
cursor=mydb.cursor()

#aggregated_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1,columns=("States","Years","Quarter",
                                               "Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2,columns=("States","Years","Quarter",
                                               "Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_user_df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user = pd.DataFrame(table3,columns=("States","Years","Quarter",
                                               "Brands","Transaction_count","Percentage"))


#agmap_insurance_df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()

map_insurance = pd.DataFrame(table4,columns=("States","Years","Quarter",
                                               "Districts","Transaction_count","Transaction_amount"))

#map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5,columns=("States","Years","Quarter",
                                               "Districts","Transaction_count","Transaction_amount"))


#map_user_df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6,columns=("States","Years","Quarter",
                                               "Districts","RegisteredUsers","AppOpens"))


#top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall()

top_insurance = pd.DataFrame(table7,columns=("States","Years","Quarter",
                                               "pincodes","Transaction_count","Transaction_amount"))


#top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8,columns=("States","Years","Quarter",
                                               "pincodes","Transaction_count","Transaction_amount"))


#top_user_df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()

top_user = pd.DataFrame(table9,columns=("States","Years","Quarter",
                                               "pincodes","RegisteredUsers"))


def Transaction_amount_count_Y(df, year):
    tacy = df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} State vise Transaction_amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=450, width=400)

        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} State vise Transaction_count",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=450, width=400)

        st.plotly_chart(fig_count)
        
    col1,col2 = st.columns(2)
    
    with col1:
    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount",
                                    color_continuous_scale= "Rainbow",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name= "States",
                                    title= f"{year} TRANSACTION AMOUNT",
                                    fitbounds= "locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count",
                                    color_continuous_scale= "Rainbow",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name= "States",
                                    title= f"{year} TRANSACTION COUNT",
                                    fitbounds= "locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return tacy
    
def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=450, width=400)

        st.plotly_chart(fig_amount)
    
    with col2:

        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=450, width=400)

        st.plotly_chart(fig_count)
        
    col1,col2 = st.columns(2)
    
    with col1:
    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url,verify=False)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount",
                                    color_continuous_scale= "Rainbow",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name= "States",
                                    title= f"{tacy['Years'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT",
                                    fitbounds= "locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=True)
        st.plotly_chart(fig_india_1)
        
    with col2:
    
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count",
                                    color_continuous_scale= "Rainbow",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name= "States",
                                    title= f"{tacy['Years'].min()} Year {quarter} QUARTER TRANSACTION COUNT",
                                    fitbounds= "locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return tacy

#Tran

def Aggree_Tran_Transaction_type(df, state):

    tacy = df[df["States"] == state ]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 =st.columns(2)
    
    with col1:

        fig_pie_1 = px.pie(data_frame= tacyg, names="Transaction_type", values= "Transaction_amount",
                        width = 600, title = f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5,)

        st.plotly_chart(fig_pie_1)
    
    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names="Transaction_type", values= "Transaction_count",
                        width = 600, title = f"{state.upper()} TRANSACTION COUNT", hole= 0.5,)

        st.plotly_chart(fig_pie_2)

#Aggre_user_analysis_1

def Aggre_user_plot_1(df,year):

    aguy = df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguy, x="Brands", y="Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence = px.colors.sequential.haline,
                    hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

def Aggre_user_plot_2(df,quarter):

    aguyq = df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyq, x="Brands", y="Transaction_count", title= f"{quarter} BRANDS AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence = px.colors.sequential.haline,
                    hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq

def Aggre_user_plot_3(df, state):
    augygs = df[df["States"]== state]
    augygs.reset_index(drop=True, inplace=True)

    fig_line_1 = px.line(augygs, x="Brands", y="Transaction_count", #hover_data="Percentage",
                        title ="BRANDS , TRANSACTION COUNT, PERCENTAGE",
                        width=1000, markers=True)
    st.plotly_chart(fig_line_1)
    

#map_insurance_district

def Map_insur_Districts(df, state):

    tacy = df[df["States"] == state ]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_bar_1 = px.bar(tacyg, x="Transaction_amount", y= "Districts", orientation="h",height=600,
                        title=f"{state} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Mint_r)

        st.plotly_chart(fig_bar_1)
        
    with col2:

        fig_bar_2 = px.bar(tacyg, x="Transaction_count", y= "Districts", orientation="h",height=600,
                        title=f"{state} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)

        st.plotly_chart(fig_bar_2)
        
#map_user_plot_1
def Map_user_plot_1(df,year):

    muy = df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)


    muyg= muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg, x="States", y=["RegisteredUsers", "AppOpens"], 
                            title =f"{year} REGISTERED USER AND APPOPENS",
                            width=1000, height= 800, markers=True)
    st.plotly_chart(fig_line_1)
    
    return muy


#map_user_plot_2
def Map_user_plot_2(df,quarter):

    muyq = df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)


    muyqg= muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_2 = px.line(muyqg, x="States", y=["RegisteredUsers", "AppOpens"], 
                            title =f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER AND APPOPENS",
                            width=1000, height= 800, markers=True,
                            color_discrete_sequence = px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_2)
    
    return muyq

#map_user_plot_3
def Map_user_plot_3(df,state):

    muyqs = df[df["States"]==state]
    muyqs.reset_index(drop=True, inplace=True)
    muyqs
    
    col1,col2 = st.columns(2)
    with col1:

        fig_map_user_bar_1 = px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation="h",
                                    title= "REGISTERED USER", height= 800, color_discrete_sequence = px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)
    
    with col2:
    
        fig_map_user_bar_2 = px.bar(muyqs, x="AppOpens", y="Districts", orientation="h",
                                    title= "APPOPENS", height= 800, color_discrete_sequence = px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)
        
# Top_insurance_

def Top_insurance_plot_1(df,state):
    tiy = df[df["States"]== state]
    tiy.reset_index(drop=True, inplace=True)


    tiyg= tiy.groupby("pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_top_insur_bar1 = px.bar(tiy, x="Quarter", y="Transaction_amount",hover_data="pincodes",
                                        title= "TOP USER TRANSACTION AMOUNT", height= 650,width=600, color_discrete_sequence = px.colors.sequential.GnBu_r)

        st.plotly_chart(fig_top_insur_bar1)
        
    with col2:
    
        fig_top_insur_bar2 = px.bar(tiy, x="Quarter", y="Transaction_count",hover_data="pincodes",
                                        title= "TOP USER TRANSACTION AMOUNT", height= 650, width=600,color_discrete_sequence = px.colors.sequential.Agsunset_r)

        st.plotly_chart(fig_top_insur_bar2)
        
def Top_user_plot_1(df,year):
    tuy = df[df["Years"]== year]
    tuy.reset_index(drop=True, inplace=True)


    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1 = px.bar(tuyg, x="States", y="RegisteredUsers",color="Quarter", hover_name="States",
                            width=1000, height= 800, color_discrete_sequence = px.colors.sequential.Burgyl,
                            title=f"{year} REGISTERED USER")

    st.plotly_chart(fig_top_plot_1)
    
    return tuy

def Top_user_plot_2(df, state):
    tuys = df[df["States"]== state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2 = px.bar(tuys, x="Quarter", y="RegisteredUsers", title=f"{state} REGISTERED USERS AND PINCODES",
                            width=1000, height=800, color="RegisteredUsers", hover_data="pincodes",
                            color_continuous_scale = px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)
    

# sql connection
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="8997",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

# plot_1 

    query1 = f'''SELECT states,SUM(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount DESC
            LIMIT 10;'''
            
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount"))
    
    col1,col2 = st.columns(2)
    
    with col1:

        fig_amount_1 = px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 of State Vise Transaction_Amount ",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount_1)

#plot_2

    query2 = f'''SELECT states,SUM(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount 
            LIMIT 10;'''
            
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    
    with col2:

        fig_amount_2 = px.bar(df_2, x="states", y="transaction_amount", title="LEAST 10 of State Vise Transaction_Amount ",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)

        st.plotly_chart(fig_amount_2)

# plot_3

    query3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount '''
            
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3 = px.bar(df_3, x="transaction_amount", y="states", title="AVERAGE of State Vise Transaction_Amount ",hover_name="states",
                      orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=900, width=1000)

    st.plotly_chart(fig_amount_3)
 
 
 # sql connection
def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="8997",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

# plot_1 

    query1 = f'''SELECT states,SUM(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count DESC
            LIMIT 10;'''
            
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="states", y="transaction_count", title="TOP 10 of State Vise Transaction_Count ",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount_1)

#plot_2

    query2 = f'''SELECT states,SUM(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count 
            LIMIT 10;'''
            
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))
    with col2:
    
        fig_amount_2 = px.bar(df_2, x="states", y="transaction_count", title="LEAST 10 of State Vise Transaction_Count ",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)

        st.plotly_chart(fig_amount_2)

# plot_3

    query3 = f'''SELECT states, AVG(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count '''
            
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3 = px.bar(df_3, x="transaction_count", y="states", title="AVERAGE of State Vise Transaction_Count ",hover_name="states",
                      orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=900, width=1000)

    st.plotly_chart(fig_amount_3)
 
 
# sql connection
def top_chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="8997",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

# plot_1 

    query1 = f'''SELECT districts,SUM(registeredusers) AS registeredusers 
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY registeredusers DESC
                 LIMIT 10;'''
            
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts", "registeredusers"))
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="districts", y="registeredusers", title=" TOP 10 of District Vise Registered User",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount_1)

#plot_2

    query2 = f'''SELECT districts,SUM(registeredusers) AS registeredusers 
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY registeredusers
                 LIMIT 10;'''
            
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts", "registeredusers"))
    with col2:

        fig_amount_2 = px.bar(df_2, x="districts", y="registeredusers", title="LEAST 10 of District Vise Registered User ",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)

        st.plotly_chart(fig_amount_2)

# plot_3

    query3 = f'''SELECT districts, AVG(registeredusers) AS registeredusers 
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY registeredusers;'''
            
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts", "registeredusers"))

    fig_amount_3 = px.bar(df_3, x="registeredusers", y="districts", title="AVERAGE of District Vise Transaction_amount ",hover_name="districts",
                      orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=900, width=1000)

    st.plotly_chart(fig_amount_3)
    
# sql connection
def top_chart_appopens(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="8997",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

# plot_1 

    query1 = f'''SELECT districts,SUM(appopens) AS appopens 
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY appopens DESC
                 LIMIT 10;'''
            
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts", "appopens"))
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="districts", y="appopens", title=" TOP 10 of District Vise APPOPENS",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount_1)

#plot_2

    query2 = f'''SELECT districts,SUM(appopens) AS appopens 
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY appopens
                 LIMIT 10;'''
            
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts", "appopens"))
    with col2:

        fig_amount_2 = px.bar(df_2, x="districts", y="appopens", title="LEAST 10 of District Vise APPOPENS ",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)

        st.plotly_chart(fig_amount_2)

# plot_3

    query3 = f'''SELECT districts, AVG(appopens) AS appopens 
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY appopens;'''
            
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3 = px.bar(df_3, x="appopens", y="districts", title="AVERAGE of District Vise APPOPENS ",hover_name="districts",
                      orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=900, width=1000)

    st.plotly_chart(fig_amount_3)
    
# sql connection
def top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="8997",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

# plot_1 

    query1 = f'''SELECT states,SUM(registeredusers) AS registeredusers 
                 FROM {table_name}
                 GROUP BY states
                 ORDER BY registeredusers DESC
                 LIMIT 10;'''
            
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "registeredusers"))
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="states", y="registeredusers", title=" TOP 10 of State Vise Registered User",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount_1)

#plot_2

    query2 = f'''SELECT states,SUM(registeredusers) AS registeredusers 
                 FROM {table_name}
                 GROUP BY states
                 ORDER BY registeredusers 
                 LIMIT 10;'''
            
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "registeredusers"))
    
    with col2:

        fig_amount_2 = px.bar(df_2, x="states", y="registeredusers", title="LEAST 10 of State Vise Registered User ",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)

        st.plotly_chart(fig_amount_2)

# plot_3

    query3 = f'''SELECT states,AVG(registeredusers) AS registeredusers 
                 FROM {table_name}
                 GROUP BY states
                 ORDER BY registeredusers;'''
            
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3 = px.bar(df_3, x="registeredusers", y="states", title="AVERAGE of State Vise Transaction_amount ",hover_name="states",
                      orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=900, width=1000)

    st.plotly_chart(fig_amount_3)
 
 
 





# Streamlit part

st.set_page_config(layout="wide")




with st.sidebar:
    
    col1,col2,col3 = st.columns(3)
    
    with col2:
        path1 = "C:\GUVI PROJECTS\PHONE PE PULSE\l2.png"
        new_width = 100 # Set desired width
        new_height = 100
        image1 =Image.open(path1)
        resized = image1.resize((new_width,new_height ))
        st.image(resized)
    select = option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])
    
    
    
if select == "HOME":
    col1,col2,col3,col4 = st.columns(4)
    
        
    
    with col4:
        st.download_button(":violet[Download the App Now]", "https://www.phonepe.com/app-download/")
    
    
    st.title(":orange[PHONEPE DATA VISUALIZATION AND EXPLORATION ]")
    
    st.subheader("PhonePe is a digital payments and financial services app that allows users to perform a variety of transactions")

    col1,col2,col3 = st.columns(3)
    with col2:
     
     st.write(":green[Sending and receiving money]")
     st.write (":green[Paying bills]")
     st.write(":green[Recharging mobile phones]")
     st.write(":green[Shopping]")
     st.write(":green[Investing]")
     st.write(":green[Booking travel]")
     
     with col1:
         path1 = "C:\GUVI PROJECTS\PHONE PE PULSE\images.jpg"
         new_width = 300  # Set desired width
         new_height = 300 
         image1 =Image.open(path1)
         resized = image1.resize((new_width,new_height ))
         st.image(resized)
         
    with col3:
        path2= "C:\GUVI PROJECTS\PHONE PE PULSE\images (1).jpg"
        new_width = 300  # Set desired width
        new_height = 300 
        image1 =Image.open(path2)
        resized = image1.resize((new_width,new_height ))
        st.image(resized)
        
        
        
elif select == "DATA EXPLORATION":
    
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    
    with tab1:
        
        method = st.radio("Select the Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])
        
        if method == "Insurance Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
            
            
        
        elif method == "Transaction Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
            Agree_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State" ,Agree_tran_tac_Y["States"].unique())
            
            Aggree_Tran_Transaction_type(Agree_tran_tac_Y, states)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter", Agree_tran_tac_Y["Quarter"].min(), Agree_tran_tac_Y["Quarter"].max(), Agree_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Agree_tran_tac_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty" ,Aggre_tran_tac_Y_Q["States"].unique())
            
            Aggree_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
            
            
        
        elif method == "User Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty" ,Aggre_user_Y_Q["States"].unique())
            
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
        
    with tab2:
        
        method_2 = st.radio("Select the Method",["Map Insurance", "Map Transaction", "Map User"])
        
        if method_2 == "Map Insurance":
            
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year_Map_Insurance", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min())
            Map_insur_tac_Y = Transaction_amount_count_Y(map_insurance, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Map_Insurance" ,Map_insur_tac_Y["States"].unique())
            
            Map_insur_Districts(Map_insur_tac_Y, states)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter_Map_Insurance", Map_insur_tac_Y["Quarter"].min(), Map_insur_tac_Y["Quarter"].max(), Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Map_insur_tac_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_MI" ,Map_insur_tac_Y_Q["States"].unique())
            
            Map_insur_Districts(Map_insur_tac_Y_Q, states)
            
            
            
        
        elif method_2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year_Map_Transaction", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min())
            Map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Map_Transaction" ,Map_tran_tac_Y["States"].unique())
            
            Map_insur_Districts(Map_tran_tac_Y, states)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter_Map_Transaction", Map_tran_tac_Y["Quarter"].min(), Map_tran_tac_Y["Quarter"].max(), Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_MT" ,Map_tran_tac_Y_Q["States"].unique())
            
            Map_insur_Districts(Map_tran_tac_Y_Q, states)
        
        elif method_2 == "Map User":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year_Map_User", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min())
            Map_user_Y = Map_user_plot_1(map_user, years)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter_Map_User", Map_user_Y["Quarter"].min(), Map_user_Y["Quarter"].max(), Map_user_Y["Quarter"].min())
            Map_user_Y_Q = Map_user_plot_2(Map_user_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_MU" ,Map_user_Y_Q["States"].unique())
            
            Map_user_plot_3(Map_user_Y_Q, states)
        
        
    with tab3:
        
        method_3 = st.radio("Select the Method",["Top Insurance", "Top Transaction", "Top User"])
        
        if method_3 == "Top Insurance":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year_Top_Insurance", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min())
            Top_insur_tac_Y = Transaction_amount_count_Y(top_insurance, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_TI" ,Top_insur_tac_Y["States"].unique())
            
            Top_insurance_plot_1(Top_insur_tac_Y, states)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter_Top_Insurance", Top_insur_tac_Y["Quarter"].min(), Top_insur_tac_Y["Quarter"].max(), Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Top_insur_tac_Y, quarters)
            
            
        
        elif method_3 == "Top Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year_Top_Insurance", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min())
            Top_tran_tac_Y = Transaction_amount_count_Y(top_transaction, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_TT" ,Top_tran_tac_Y["States"].unique())
            
            Top_insurance_plot_1(Top_tran_tac_Y, states)
            
            col1,col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select The Quarter_Top_Transaction", Top_tran_tac_Y["Quarter"].min(), Top_tran_tac_Y["Quarter"].max(), Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)
        
        elif method_3 == "Top User":
            
            col1,col2 = st.columns(2)
            with col1:
               years = st.slider("Select The Year_Top_Insurance", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min())
            Top_user_Y = Top_user_plot_1(top_user, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_TU" ,Top_user_Y["States"].unique())
            
            Top_user_plot_2(Top_user_Y, states)
        
elif select == "TOP CHARTS":
    
    question = st.selectbox("Select the Questions", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                     "2. Transaction Amount and Count of Map Insurance",
                                                     "3. Transaction Amount and Count of Top Insurance",
                                                     "4. Transaction Amount and Count of Aggregated Transaction",
                                                     "5. Transaction Amount and Count of Map Transaction",
                                                     "6. Transaction Amount and Count of Top Transaction",
                                                     "7. Transaction Count of Aggregated User",
                                                     "8. Registered Users of Map User",
                                                     "9. App Opens of Map User",
                                                     "10. Registered Users of Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
        
    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
        
    elif question == "7. Transaction Count of Aggregated User":
        
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
        
    elif question == "8. Registered Users of Map User":
        
        
        st.subheader("REGISTERED USERS")
        
        states =st.selectbox("Selec the State", map_user["States"].unique())
        top_chart_registered_user("map_user", states)
        
    elif question == "9. App Opens of Map User":
        
        
        st.subheader("APP OPENS")
        
        states =st.selectbox("Selec the State", map_user["States"].unique())
        top_chart_appopens("map_user", states)
        
    elif question == "10. Registered Users of Top User":
        
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")