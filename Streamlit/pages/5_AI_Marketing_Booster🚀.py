import pandas as pd
import numpy as np
import streamlit as st
from components import request_maker, data_converter
import io

if 'old_product_id' not in st.session_state:
    st.session_state.old_product_id = None
if 'campaign_plan_output' not in st.session_state:
    st.session_state.campaign_plan_output = None
if 'poster_link' not in st.session_state:
    st.session_state.poster_link = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'customizations' not in st.session_state:
    st.session_state.customizations = None

st.title('AI Marketing Booster🚀')
st.subheader('Generate AI Powered Marketing Campaigns to Boost Revenue')
if st.session_state.email is None:
    st.warning('Please login to access the AI Marketing Booster')
else:
    if st.session_state.internal_data is None:
        st.warning('Please upload a dataset to view AI Marketing Booster!')
    else: 
        st.session_state.product_id = st.selectbox('Select a product id for AI generated campaigns:', st.session_state.internal_data['Clothing ID'].unique())
        st.success("Showing marketing insights for product id : "+ str(st.session_state.product_id)+ ' 🎉')
        
        if st.session_state.old_product_id != st.session_state.product_id:
            with st.spinner('Generating AI Powered Marketing Campaign...'):
                st.session_state.product_insights = request_maker.get_product_insights(st.session_state.username, st.session_state.product_id)
                st.session_state.campaign_plan_output, st.session_state.poster_link, st.session_state.summary = request_maker.generate_marketing_campaign_and_poster(st.session_state.product_insights, data_converter.get_class_name(st.session_state.internal_data, st.session_state.product_id), st.session_state.customizations)
                st.session_state.old_product_id = st.session_state.product_id
        
        # if st.session_state.customizations is not None:
        #     with st.spinner('Generating Modified AI Powered Marketing Campaign...'):
        #         st.session_state.product_insights = request_maker.get_product_insights(st.session_state.username, st.session_state.product_id)
        #         st.session_state.campaign_plan_output, st.session_state.poster_link, st.session_state.summary = request_maker.generate_marketing_campaign_and_poster(st.session_state.product_insights, data_converter.get_class_name(st.session_state.internal_data, st.session_state.product_id), st.session_state.customizations)
        #         st.session_state.old_product_id = st.session_state.product_id
        #         st.session_state.customizations = None

        col1, col2 = st.columns([0.5, 0.5], gap = 'medium')
        with col1:
            st.subheader('Marketing Campaign Plan')
            st.write(st.session_state.campaign_plan_output)
        with col2:
            st.subheader("Marketing Poster Image")
            st.image(st.session_state.poster_link, use_column_width=True)

            buf = io.BytesIO()
            st.session_state.poster_link.save(buf, format='PNG')
            byte_im = buf.getvalue()

            st.download_button(
                label="Download Marketing Poster",
                data=byte_im,
                file_name="Product_"+str(st.session_state.product_id)+"_marketing_poster.png",
                mime="image/png"
            )

            st.subheader('Customize Marketing Poster')
            st.session_state.customizations = st.text_input('Enter your customizations here:', key='customization_input')
            customizations_button_clicked = st.button('Apply Customizations', key='apply_customizations_button')
            if customizations_button_clicked:
                with st.spinner('Applying Customizations...'):

                    st.session_state.product_insights = request_maker.get_product_insights(st.session_state.username, st.session_state.product_id)
                    temp_dump, st.session_state.poster_link, st.session_state.summary = request_maker.generate_marketing_campaign_and_poster(st.session_state.product_insights, data_converter.get_class_name(st.session_state.internal_data, st.session_state.product_id), st.session_state.customizations)
                    st.session_state.old_product_id = st.session_state.product_id
                    st.session_state.customizations = None
                    st.experimental_rerun()

        st.markdown("""---""")

        summary_button_clicked = st.button('Generate Marketing Campaign Summary', key='summary_button')
        if summary_button_clicked:
            with st.spinner('Generating Summary...'):
                summary = request_maker.generate_summary(st.session_state.campaign_plan_output, st.session_state.summary)
                st.subheader('Marketing Campaign Summary')
                st.write(summary)