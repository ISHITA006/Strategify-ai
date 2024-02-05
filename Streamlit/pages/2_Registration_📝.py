import streamlit as st
import pandas as pd
import numpy as np
import time
from components import request_maker

if 'email' not in st.session_state:
    st.session_state.email = None
if 'submit' not in st.session_state:
    st.session_state.submit = None
if 'done' not in st.session_state:
    st.session_state.done = None
if 'validate' not in st.session_state:
    st.session_state.validate = None

col1, col2, col3 = st.columns([2, 8, 2])

with col2:
    st.title("Welcome New User! :smile:")
    st.write("")   
    username_input = st.text_input("Enter a username 🙋‍♂️", placeholder="Username")
    st.write("")
    email_input = st.text_input("Enter your email 📧", placeholder="Email")
    st.write("")
    password_input = st.text_input("Enter a password 🔑", placeholder="Password", type="password")
    submitted = st.button("Submit")
    if submitted:
        if " " in username_input:
                st.warning("Username cannot contain spaces😱 Please enter a valid username😟")
        else:
            with st.spinner('Registering User'):
                st.session_state.validate = request_maker.register_user(username_input, email_input, password_input)
            if st.session_state.validate == 'password':
                st.warning("Password must contain at least 8 characters!😱")
            elif st.session_state.validate == 'email':
                st.warning("Email already exists!😱")
            else:
                st.session_state['email'] = email_input
                st.session_state.username = username_input
                st.session_state.dataset_exists = None
                st.session_state.internal_data = None
                st.success(f"Username '{username_input}' created successfully! :white_check_mark:")
            st.session_state['submit'] = submitted

            
