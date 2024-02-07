import pandas as pd
import streamlit as st
import numpy as np
import pymongo
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from PIL import Image


# Page Configuration
icon = Image.open("icon.jpg")
st.set_page_config(page_title= "Airbnb Data Analysis & Dashboard",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """### This dashboard is brought to you by S.Pavitran Kartick
                                        The necessary data has been sampled from mongo Atlas."""}
                  )

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Highlights","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "2px", "--hover-color": "#FF8F8F"},
                                   "nav-link-selected": {"background-color": "#993030"}}
                          )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://pavitrankarticks:Zurajanai1@guvi.spcpzfu.mongodb.net/")
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    # Title Image
    st.image("Title.png")
    col1,col2 = st.columns([4,1],gap='small')
    col1.markdown("## :red[Domain] : Travel Industry, Property Management and Tourism")
    col1.markdown("## :red[Tools Utilized] : Python, Pandas, Streamlit, MongoDB, PowerBI")
    col1.markdown("## :red[Synopsis] : This project aims  to provide an overview of the procured Airbnb data using Streamlit. With the help of this web application and dashboard, Users can gain insights into pricing variations, availability patterns, and location-based trends of hotels/apartments. The project has been imbued with creative visualizations and plots for better understanding of hotel pricing and availability.")
    col2.image("home.webp")
    
# Highlights PAGE
if selected == "Highlights":
    tab1,tab2 = st.tabs([" $ \huge 📊  ExtractedData $", " $ \huge 🔎  TopTrends $"])
    
    # RAW DATA TAB
    with tab1:
        #extracted dataframe
        with st.expander("Click to view Dataframe"):
            st.write(df)
        #raw data
        with st.expander("Click to view Raw data"):
            st.write(col.find_one())
       
       
    # Top Trends 
    with tab2:
        # GETTING USER INPUTS
        country = st.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
        
        
            
        # TOP 10 PROPERTY TYPES BAR CHART
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                        title='Top 10 Property Types',
                        x='Listings',
                        y='Property_type',
                        orientation='h',
                        color='Property_type',
                        color_continuous_scale=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig,use_container_width=True) 
    
        

        # TOP 10 HOSTS BAR CHART
        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df2,
                        title='Top 10 Hosts with Highest number of Listings',
                        x='Listings',
                        y='Host_name',
                        orientation='h',
                        color='Host_name',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        
        st.divider()
            
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1,
                        title='Total Listings in each Room_types',
                        names='Room_type',
                        values='counts',
                        color_discrete_sequence=px.colors.sequential.Agsunset
                    )
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)

        st.divider()

        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='Country',
                            locationmode='country names',
                            color='Total_Listings',
                            color_continuous_scale=px.colors.sequential.Plasma
                            )
        st.plotly_chart(fig,use_container_width=True)

        st.divider()
        
# EXPLORE PAGE
if selected == "Explore":
    st.markdown("# Explore the varying trends of Airbnb listings")
    
    # GETTING USER INPUTS
    country = st.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
        
    # AVG PRICE BY ROOM TYPE BARCHART
    pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
    fig = px.bar(data_frame=pr_df,
                    x='Room_type',
                    y='Price',
                    color='Price',
                    title='Avg Price in each Room type'
                )
    st.plotly_chart(fig,use_container_width=True)

    st.divider()
    
    # HEADING 2
    st.markdown("## Availability Analysis")
    
    # AVAILABILITY BY ROOM TYPE BOX PLOT
    fig = px.box(data_frame=df.query(query),
                    x='Room_type',
                    y='Availability_365',
                    color='Room_type',
                    title='Availability by Room_type'
                )
    st.plotly_chart(fig,use_container_width=True)

    st.divider()
        
    # AVG PRICE IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
    fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color= 'Price', 
                                    hover_data=['Price'],
                                    locationmode='country names',
                                    size='Price',
                                    title= 'Avg Price in each Country',
                                    color_continuous_scale='agsunset'
                        )
    st.plotly_chart(fig,use_container_width=True)

    st.divider()
    
    # BLANK SPACE
    st.markdown("#   ")
    st.markdown("#   ")
    
    # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
    country_df.Availability_365 = country_df.Availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color= 'Availability_365', 
                                    hover_data=['Availability_365'],
                                    locationmode='country names',
                                    size='Availability_365',
                                    title= 'Avg Availability in each Country',
                                    color_continuous_scale='agsunset'
                        )
    st.plotly_chart(fig,use_container_width=True)

    st.divider()