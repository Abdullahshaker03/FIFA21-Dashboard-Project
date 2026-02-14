import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FIFA 21 Dashboard", layout="wide")
st.title("⚽ FIFA 21 Data Analysis Dashboard")
st.markdown("Created by Abdullah Shaker")

#Load Data 
@st.cache_data
def load_data():
    df = pd.read_csv('mid_project.csv')
    df.columns = df.columns.str.strip() 
    return df

df1 = load_data()

#Sidebar for filtering
st.sidebar.header("Filter Options")
all_clubs = df1['Club'].dropna().unique()
selected_clubs = st.sidebar.multiselect("Select Clubs to Compare:", 
                                        options=all_clubs, 
                                        default=['Liverpool', 'Real Madrid', 'FC Barcelona'])

#Display Key Metrics
col_a, col_b, col_c = st.columns(3)
col_a.metric("Total Players", len(df1))
col_b.metric("Avg Overall Rating", round(df1['↓OVA'].mean(), 1))
col_c.metric("Total Market Value", f"€{df1['Value(€)'].sum() / 1e9:.1f}B")

#Data Dictionary
st.divider()   
with st.expander(" Click to see Columns Description (Data Dictionary)"):
    st.markdown("""
    | Column Name | Description |
    |:---|:---|
    | **LongName** | Full name of the player |
    | **Nationality** | Country the player represents |
    | **Age** | Player’s age (in years) |
    | **Club** | Club the player is currently playing for |
    | **Preferred Foot** | Player’s preferred foot (Left or Right) |
    | **↓OVA** | Overall rating of the player (current ability) |
    | **POT** | Maximum potential rating the player can reach |
    | **Value(€)** | Estimated market value of the player |
    | **Wage(€)** | Weekly wage of the player |
    | **Release Clause(€)** | Minimum amount required to buy the player from the club |
    | **PAC** | Pace (Speed) attribute of the player |
    | **SHO** | Shooting attribute of the player |
    | **PAS** | Passing attribute of the player |
    | **DRI** | Dribbling attribute of the player |
    | **DEF** | Defending attribute of the player |
    | **PHY** | Physical attribute of the player |
    | **Hits** | Number of times the player's profile has been viewed |
    """)
st.divider()

# Age and Nationality Distribution (Row 1)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Player Age Distribution")
    fig1 = px.histogram(df1, x='Age', nbins=20,text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Top 10 Nationalities")
    top10_nat = df1['Nationality'].value_counts().head(10).reset_index()
    fig2 = px.bar(top10_nat, x='Nationality', y='count', text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# Club Comparison Analysis
st.divider()
if selected_clubs:
    filtered_df = df1[df1['Club'].isin(selected_clubs)]
    st.header(f"📊 Detailed Comparison for Selected Clubs")

    st.subheader("Physicality (PHY) Comparison")

    fig3 = px.box(filtered_df, 
                 x='Club', 
                 y='PHY') 

    fig3.update_layout(height=600) 

    st.plotly_chart(fig3, use_container_width=True) 


# Trending Players (Hits)
st.divider()
st.header("Top 10 Most Trending Players (Hits)")
top_hits = df1.nlargest(10, 'Hits')
fig4 = px.bar(top_hits, x='LongName', y='Hits', 
             text_auto=True)
st.plotly_chart(fig4, use_container_width=True)


st.divider()
st.header("📈 Market Intelligence: Rating vs. Value")

fig_scatter = px.scatter(data_frame=df1, 
                         x='↓OVA', 
                         y='Value(€)', 
                         title='Overall Rating vs Market Value', 
                         labels={'↓OVA' : 'Overall Rating', 'Value(€)': 'Market Value (€)'})

fig_scatter.update_layout(height=600)
st.plotly_chart(fig_scatter, use_container_width=True)
