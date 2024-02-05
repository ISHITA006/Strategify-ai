import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from components import data_converter, chart_maker

if 'vertical_selected' not in st.session_state:
    st.session_state.vertical_selected = None
if 'vertical_options' not in st.session_state:
    st.session_state.vertical_options = None 
if 'division_data' not in st.session_state:
    st.session_state.division_data = None
if 'radar_chart_dict' not in st.session_state:
    st.session_state.radar_chart_dict = None 
if 'compare_rating' not in st.session_state:
    st.session_state.compare_rating = False

st.title('Division Insights Dashboard 🏭')
st.subheader('View Customer Insights across Departments, Divisions or Classes')

if st.session_state.email is None:
    st.warning('Please login to access the Division Insights')
else:
    if st.session_state.internal_data is not None:

        st.session_state.vertical_selected = st.selectbox('Select a Vertical:', ['Division Name', 'Department Name', 'Class Name'])
        st.session_state.vertical_options = st.selectbox('Select a '+ st.session_state.vertical_selected+' :', st.session_state.internal_data[st.session_state.vertical_selected].unique())
        st.session_state.division_data = data_converter.create_sub_dataframe(st.session_state.internal_data, st.session_state.vertical_selected, st.session_state.vertical_options) 

        col1, col2 = st.columns([0.5, 0.5], gap='large')

        with col1:
            st.subheader('Recommended Percentage 🗣️')
            chart_maker.create_pie_chart(st.session_state.division_data, 'Recommended IND')

        with col2:
            st.subheader('Rating Percentage by Age 🌟')
            st.session_state.radar_chart_dict = data_converter.create_radar_chart_dict(st.session_state.division_data)
            chart_maker.create_animated_radar_chart(st.session_state.radar_chart_dict)

        with col1:
            st.subheader('Ratings Information📊')
            st.session_state.compare_rating = st.checkbox('Compare with Average for '+ st.session_state.vertical_selected, key='compare_with_average_rating')
            chart_maker.create_score_barchart_comparison(st.session_state.division_data, st.session_state.internal_data, st.session_state.vertical_selected, st.session_state.vertical_options, st.session_state.compare_rating)

        with col2:
            st.subheader('Ratings by Age Group📊')
            st.write(" ")
            st.write(" ")
            chart_maker.create_stacked_bar_chart(st.session_state.internal_data, st.session_state.vertical_selected, st.session_state.vertical_options)
            
    else:
        st.warning('Please upload a dataset to view division based insights!')