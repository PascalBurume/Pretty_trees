"""
This script creates a Streamlit app to analyze trees in San Francisco using a dataset provided by SF DPW.
The app allows filtering the trees by their owner and displays histograms of tree width and age, as well as a map of tree locations.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
    page_title="SF Trees",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Display app title and description
st.title("SF Trees")
st.write(
    """
    This app analyses trees in San Francisco using
    a dataset kindly provided by SF DPW. The dataset
    is filtered by the owner of the tree as selected
    in the sidebar!
    """
)

# Read the trees dataset
trees_df = pd.read_csv("trees.csv")
today = pd.to_datetime("today")

# Calculate tree age based on the current date
trees_df["date"] = pd.to_datetime(trees_df["date"])
trees_df["age"] = (today - trees_df["date"]).dt.days

# Get unique caretakers (tree owners)
unique_caretakers = trees_df["caretaker"].unique()

# Allow filtering trees by owner in the sidebar
owners = st.sidebar.multiselect("Tree Owner Filter", unique_caretakers)

#Pick colors for the graph 
graph_colors = st.sidebar.color_picker("Pick a color for the graph")

# Apply owner filter if selected
if owners:
    trees_df = trees_df[trees_df["caretaker"].isin(owners)]
    df_dbh_grouped = pd.DataFrame(trees_df.groupby(["dbh"]).count()["tree_id"])
    df_dbh_grouped.columns = ["tree_count"]

# Create two columns for displaying histograms
col1, col2 = st.columns(2)

# Display histogram of tree width in the first column
with col1:
    fig = px.histogram(trees_df, x=trees_df["dbh"], title="Tree Width", color_discrete_sequence=[graph_colors])
    st.plotly_chart(fig)

# Display histogram of tree age in the second column
with col2:
    fig = px.histogram(
        trees_df, x=trees_df["age"], title="Tree Age", color_discrete_sequence=[graph_colors])
    st.plotly_chart(fig)


