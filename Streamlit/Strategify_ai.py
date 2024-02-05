from components import request_maker
import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import ast
import time
from streamlit_lottie import st_lottie
from components import data_loader, data_converter

st.set_page_config(
    page_title="Strategify.ai",
    page_icon="📈",
    layout="wide"
)

if 'product_id' not in st.session_state:
    st.session_state.product_id = None
if 'internal_data' not in st.session_state:
    st.session_state.internal_data = None
if 'email' not in st.session_state:
    st.session_state.email = None 
if 'login_button' not in st.session_state:
    st.session_state.login_button = None
if 'dataset_exists' not in st.session_state:
    st.session_state.dataset_exists = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'username' not in st.session_state:
    st.session_state.username = None


col1, col2, col3 = st.columns([0.7, 0.1, 0.2], gap = 'large')

with col3:
    if st.session_state.email is None:
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        text_input = st.text_input("Please enter Email 📧", placeholder="Email")
        password_input = st.text_input("Please enter Password👇", placeholder="Password", type="password")
    else:
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        text_input = st.text_input("Please enter Email 📧", placeholder=st.session_state.email)
        password_input = st.text_input("Please enter Password👇", type="password")
    col4, col5 = st.columns([0.5, 0.5], gap = 'large')
    with col4:
        if st.button("Login"):
            st.session_state.login_button = 'login attempted'
            st.experimental_rerun()
    with col5:
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()
    
    if text_input and password_input and st.session_state.login_button is not None:
        if st.session_state.login_button is not None and request_maker.validate_user(text_input, password_input) == 'username':
            st.warning('Sorry we did not find that username, please register on our registration page')
            time.sleep(5)
        elif st.session_state.login_button is not None and request_maker.validate_user(text_input, password_input) == 'password':
            st.warning('Invalid password, please try again 🙁')
        else:
            st.session_state.email, st.session_state.username = text_input, request_maker.validate_user(text_input, password_input)[1]
        st.session_state.login_button = None
        st.experimental_rerun()

with col1:
    st.title('Welcome to Strategify.ai! 📈')
    if st.session_state.email is None:
        st.warning('Please login to access Strategify.ai 😟')
    else:
        st.success('Welcome '+ st.session_state.username + ' 🎉')
        with st.spinner('Checking for any previously uploaded data...'):
            temp = request_maker.check_data_exists(st.session_state.username)
        if temp == 'error':
            st.warning('Please upload a dataset to view insights 🙁')
            st.session_state.uploaded_file = st.file_uploader('Upload a dataset', type=['csv'])
            with st.spinner('Uploading...'):
                if st.session_state.uploaded_file is not None:
                    st.session_state.internal_data = pd.read_csv(st.session_state.uploaded_file)
                    st.session_state.internal_data.sort_values(by='Clothing ID', inplace=True)
                    if st.session_state.internal_data is not None:
                        st.session_state.dataset_exists = 'yes'
                    my_json = data_converter.to_json(st.session_state.internal_data)
                    if request_maker.upload_data(my_json, st.session_state.username) == 'success':
                        st.success('Dataset uploaded successfully! 🎉')
                        st.write('You can now move on to our insights dashboard to get insights on the product! ')
                        st.write('You can also view our AI powered market generator to supercharge your marketing strategy! 🚀')
                    else:
                        st.warning('There was an error uploading the dataset, please try again')
        else:
            st.success('You have already uploaded a dataset. If you want to modify you can reupload a new dataset')
            st.session_state.dataset_exists = 'yes'
            with st.spinner("Retrieving your dataset..."):
                st.session_state.internal_data = data_converter.from_json(request_maker.download_dataset(st.session_state.username))
            st.session_state.internal_data.sort_values(by='Clothing ID', inplace=True)
            if st.session_state.internal_data is not None:
                st.session_state.dataset_exists = 'yes'
            st.session_state.uploaded_file = st.file_uploader('Modify your dataset', type=['csv'])
            if st.session_state.uploaded_file is None:
                st.write('You can now move on to our insights dashboard to get insights on the product! ')
                st.write('You can also view our AI powered market generator to supercharge your marketing strategy! 🚀')
            with st.spinner('Uploading...'):
                if st.session_state.uploaded_file is not None:
                    st.session_state.internal_data = pd.read_csv(st.session_state.uploaded_file)
                    st.session_state.internal_data.sort_values(by='Clothing ID', inplace=True)
                    if st.session_state.internal_data is not None:
                        st.session_state.dataset_exists = 'yes'
                    my_json = data_converter.to_json(st.session_state.internal_data)
                    if request_maker.reupload_dataset(my_json, st.session_state.username) == 'success':
                        st.success('Dataset uploaded successfully! 🎉')
                        st.write('You can now move on to our insights dashboard to get insights on the product! ')
                        st.write('You can also view our AI powered market generator to supercharge your marketing strategy! 🚀') 
                    else:
                        st.warning('There was an error uploading the dataset, please try again')
            



        
        
        



