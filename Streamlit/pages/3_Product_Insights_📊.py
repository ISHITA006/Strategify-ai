import streamlit as st
import pandas as pd
import numpy as np
import time
from components import request_maker, chart_maker, data_converter

if 'age_insights' not in st.session_state:
    st.session_state.age_insights = False
if 'product_insights' not in st.session_state:
    st.session_state.product_insights = None

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Product Insights Dashboard 📊')
st.subheader('View Customer Sentiment Insights for Each Product')
if st.session_state.email is None:
    st.warning('Please login to access the Product Insights')
else:
    if st.session_state.internal_data is None:
        st.warning('Please upload a dataset to view insights!')
    else:
        st.session_state.product_id = st.selectbox('Select a product id for product-wise insights:', st.session_state.internal_data['Clothing ID'].unique())
        st.success('You have selected product id : '+ str(st.session_state.product_id) + ' 🎉')
        with st.spinner('Loading Insights...'):
            st.session_state.product_insights = request_maker.get_product_insights(st.session_state.username, st.session_state.product_id)
            col1, col2 = st.columns([0.5, 0.5], gap = 'large')
            with col1:
                st.subheader('Customer Feedback')
                chart_maker.create_table(data_converter.create_sub_dataframe(st.session_state.internal_data, 'Clothing ID', st.session_state.product_id))
            with col2:
                st.subheader("Repetitive Customer Sentiments")
                recurring_keywords = data_converter.get_recurring_keywords(st.session_state.product_insights)
                st.pyplot(fig = chart_maker.generate_enriched_wordcloud(recurring_keywords), use_container_width=True)
            st.subheader('Product Insights')
            col1, col3, col2 = st.columns([0.425, 0.15, 0.425], gap = 'large')
            with col1:
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'quality', 'Quality of Product')
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'style', 'Style Rating')
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'valueForMoney', 'Value for Money')
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'ratings', 'Ratings')
            with col2:
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'fit', 'Fit of Product')
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'delivery', 'Delivery Experience')
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'customerService', 'Customer Service Rating')
                chart_maker.create_pie_chart_from_json(st.session_state.product_insights, 'recommend', 'Recommendation')

            

            
