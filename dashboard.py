import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# function
def create_perhour_df(df):
    perhour_df = df.groupby(by="hour").agg({'count': ['count', 'mean']}).reset_index()
    return perhour_df
def create_perday_df(df):
    perday_df = df.groupby(by="weekday").agg(count=("count", "mean")).reset_index()
    order = [3, 1, 5, 6, 4, 0, 2]
    perday_df = perday_df.reindex(order)
    return perday_df
def create_perweather_df(df):
    perweather_df = df.groupby(by="weather").agg(count=("count", "mean")).reset_index()
    return perweather_df
def create_perseason_df(df):
    perseason_df = df.groupby(by="season").agg(count=("count", "mean")).reset_index()
    return perseason_df
def create_peryear_df(df,the_year):
    peryear_df = df.groupby(df['datetime'].dt.month).agg({'registered': 'sum'})
    peryear_df = df[df['datetime'].dt.year == the_year]
    peryear_df['datetime'] = pd.to_datetime(peryear_df['datetime'])
    return peryear_df
def create_perregis_df(df):
    df['datetime'] = df['datetime'].dt.strftime('%B')
    perregis_df = df.groupby(by="datetime").agg(count=("registered", "sum")).reset_index()
    order = [4, 3, 7, 0, 8, 6, 5, 1, 11, 10, 9, 2]
    perregis_df = perregis_df.reindex(order)
    return perregis_df

# read data
main_df = pd.read_csv("main_data.csv")
for column in ["datetime"]: 
    main_df[column] = pd.to_datetime(main_df[column])
# create data
the_year = 2011
peryear_df_11 = create_peryear_df(main_df, the_year)
perhour_df = create_perhour_df(peryear_df_11)
perday_df = create_perday_df(peryear_df_11)
perweather_df = create_perweather_df(peryear_df_11)
perseason_df = create_perseason_df(peryear_df_11)
perregis_df = create_perregis_df(peryear_df_11)
color = ["#D3D3D3", "#D3D3D3", "#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
color1 = ["#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
color2 = ["#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


# header
st.title('Bike Sharing Dashboard 🚲')
# column
st.subheader('Year')
col1, col2 = st.columns(2)
with col1:
    if st.button('2011'):
        the_year = 2011
        peryear_df_11 = create_peryear_df(main_df, the_year)
        perhour_df = create_perhour_df(peryear_df_11)
        perday_df = create_perday_df(peryear_df_11)
        perweather_df = create_perweather_df(peryear_df_11)
        perseason_df = create_perseason_df(peryear_df_11)
        perregis_df = create_perregis_df(peryear_df_11)
        color = ["#D3D3D3", "#D3D3D3", "#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        color1 = ["#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        color2 = ["#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        total_orders = perregis_df["count"].sum()
        st.metric("Total Rented Bikes", value=total_orders)
with col2:
    if st.button('2012'):
        the_year = 2012
        peryear_df_12 = create_peryear_df(main_df, the_year)
        perhour_df = create_perhour_df(peryear_df_12)
        perday_df = create_perday_df(peryear_df_12)
        perweather_df = create_perweather_df(peryear_df_12)
        perseason_df = create_perseason_df(peryear_df_12)
        perregis_df = create_perregis_df(peryear_df_12)
        color = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#ff8819", "#D3D3D3", "#D3D3D3"]
        color1 = ["#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        color2 = ["#ff8819", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        total_orders = perregis_df["count"].sum()
        st.metric("Total Rented Bikes", value=total_orders)


with st.sidebar:
    choices = st.selectbox(
        label="Average Rented Bikes",
        options=('Select an option', '🕓 per-Hour', '📅 per-Day', '🌤️ per-Weather', '🍁 per-Season')
    )
    if choices=='🕓 per-Hour':
        max_hour = perhour_df.loc[perhour_df['count'].idxmax(), 'hour']
        st.write('The most number of Rented Bikes is at', max_hour[17])
    elif choices=='📅 per-Day':
        if the_year==2012:
            st.write('The most number of Rented Bikes is on Thursday')
        else:
            st.write('The most number of Rented Bikes is on Tuesday')
    elif choices=='🌤️ per-Weather':
        max_weather = perweather_df.loc[perweather_df['count'].idxmax(), 'weather']
        st.write('The most number of Rented Bikes is during', max_weather, 'weather')
    elif choices=='🍁 per-Season':
        max_season = perseason_df.loc[perseason_df['count'].idxmax(), 'season']
        st.write('The most number of Rented Bikes is during', max_season, 'season')


st.header('Average Rented Bikes')
st.subheader('🕓 per-Hour')
fig, ax = plt.subplots(figsize=(30, 12))
ax.plot(    
    perhour_df["hour"],
    perhour_df["count"]["mean"],
    marker='o', 
    linewidth=3,
    color="#ff8819"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader('📅 per-Day')
fig, ax = plt.subplots(figsize=(25, 10))
sns.barplot(
    y="count", 
    x="weekday",
    data=perday_df,
    palette=color,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader('🌤️ per-Weather')
fig, ax = plt.subplots(figsize=(25, 10))
sns.barplot(
    y="count", 
    x="weather",
    data=perweather_df,
    palette=color1,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader('🍁 per-Season')
fig, ax = plt.subplots(figsize=(25, 10))
sns.barplot(
    y="count", 
    x="season",
    data=perseason_df,
    palette=color2,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.header('Growth of Rented Bikes')
st.subheader('📝 per-Registered User')
fig, ax = plt.subplots(figsize=(25, 10))
ax.plot(
    perregis_df["datetime"],
    perregis_df["count"],
    marker='o', 
    linewidth=2,
    color="#ff8819"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.caption('Made with ❤️ | © 2024 by Nabila')