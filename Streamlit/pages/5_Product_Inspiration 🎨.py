import streamlit as st
import pandas as pd
from components import request_maker, data_converter

st.title('Product Inspiration🎨')
st.subheader('Improve Product Design Based on Customer Sentiments')
st.write('These product inspirations are curated by leveraging on the current product strengths and to improve the product weaknesses based on customer feedback. ')

if st.session_state.email is None:
    st.warning('Please login to access Product Inspirations')
else:
    if st.session_state.internal_data is None:
        st.warning('Please upload a dataset to view insights!')
    else: 
        st.session_state.product_id = st.selectbox('Select a product id for product-wise insights:', st.session_state.internal_data['Clothing ID'].unique())
        st.success("Showing marketing insights for product id : "+ str(st.session_state.product_id)+ ' 🎉')

        with st.spinner('Generating AI Powered Product Inspirations...'):
            st.session_state.product_insights = request_maker.get_product_insights(st.session_state.username, st.session_state.product_id)
            image_links = request_maker.generate_image(st.session_state.product_insights, data_converter.get_class_name(st.session_state.internal_data, st.session_state.product_id))
            if image_links == 'All API keys failed, unable to generate images':
                st.warning('All API keys failed, unable to generate images')
            else:
                cnt = 1
                col1, col2 = st.columns([0.5, 0.5])
                for i in image_links:
                    if cnt%2 == 0:
                        with col1:
                            st.image(i, use_column_width=True)
                    else:
                        with col2:
                            st.image(i, use_column_width=True) 
                    cnt+=1   
                    
