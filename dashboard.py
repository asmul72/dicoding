# bike_sharing_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config FIRST
st.set_page_config(page_title="Bike Sharing Analytics", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('day.csv', parse_dates=['dteday'])

df = load_data()

# Set up dashboard
st.title("🚴♂️ Bike Sharing System Dashboard")
st.markdown("Analyzing rental patterns and operational metrics")

# Sidebar filters
st.sidebar.header("Filters")
year_filter = st.sidebar.multiselect('Select Years:', options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")

# Preprocess filtered data
if year_filter:
    df_filtered = df[df['yr'].isin(year_filter)]
else:
    df_filtered = df.copy()

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Rentals", f"{df_filtered['cnt'].sum():,}")
with col2:
    st.metric("Avg Daily Rentals", f"{df_filtered['cnt'].mean():.0f}")
with col3:
    st.metric("Peak Daily Rentals", df_filtered['cnt'].max())
with col4:
    st.metric("Registered Users Ratio", f"{(df_filtered['registered'].sum()/df_filtered['cnt'].sum())*100:.1f}%")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🌦 Weather Impact", "👥 User Analysis", "📊 Data"])

with tab1:
    # Temporal trends
    st.subheader("Temporal Patterns")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df_filtered, x='dteday', y='cnt', ax=ax)
    ax.set_title("Daily Rentals Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)
    
    # Monthly patterns
    df_filtered['month'] = df_filtered['dteday'].dt.month_name()
    monthly_data = df_filtered.groupby(['yr', 'month'])['cnt'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=monthly_data, x='month', y='cnt', hue='yr', ax=ax,
                order=['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'])
    ax.set_title("Monthly Rental Patterns")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with tab2:
    # Weather impact
    st.subheader("Weather Impact Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df_filtered, x='weathersit', y='cnt', ax=ax)
        ax.set_title("Rentals by Weather Condition")
        ax.set_xlabel("Weather Situation (1:Best, 3:Worst)")
        ax.set_ylabel("Daily Rentals")
        st.pyplot(fig)
    
    with col2:
        # Correlation matrix
        corr = df_filtered[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(corr[['cnt']].sort_values(by='cnt', ascending=False), 
                    annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Feature Correlation with Rentals")
        st.pyplot(fig)

with tab3:
    # User analysis
    st.subheader("User Behavior Patterns")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df_filtered, x='dteday', y='registered', label='Registered', ax=ax)
    sns.lineplot(data=df_filtered, x='dteday', y='casual', label='Casual', ax=ax)
    ax.set_title("User Type Trends Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Users")
    st.pyplot(fig)
    
    # Special days comparison
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.barplot(data=df_filtered, x='holiday', y='cnt', ax=ax[0])
    ax[0].set_title("Holiday vs Regular Days")
    ax[0].set_xticklabels(['Regular', 'Holiday'])
    
    sns.barplot(data=df_filtered, x='workingday', y='cnt', ax=ax[1])
    ax[1].set_title("Working Day vs Non-Working")
    ax[1].set_xticklabels(['Non-Working', 'Working'])
    st.pyplot(fig)

with tab4:
    # Raw data
    st.subheader("Dataset Preview")
    st.dataframe(df_filtered.head(100))
    
    # Data summary
    if st.checkbox("Show Data Summary"):
        st.write(df_filtered.describe())
    
    # Download button
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_bike_data.csv",
        mime="text/csv"
    )

# Recommendations section
st.markdown("---")
st.subheader("Operational Recommendations")
st.markdown("""
1. **Inventory Management**: Increase bike availability during fall months (Sep-Oct)
2. **Weather Preparedness**: Implement surge pricing during optimal weather days
3. **User Engagement**: Target registered users with loyalty programs in winter
4. **Maintenance Scheduling**: Plan maintenance during low-rental periods (Jan-Feb)
5. **Staff Allocation**: Increase staff during working days and peak seasons
""")
