import pandas as pd
import numpy as np
import streamlit as st

def load_csv(file_name):
    df = pd.read_csv(r'C:\Users\nihal\OneDrive - Nanyang Technological University\Market_Assist\Streamlit\data\\'+file_name+'.csv')
    return df

def convert_json_to_df(data):
    age = []
    rating = []
    recommend = []
    division_name = []
    department_name = []
    class_name = []
    for i in data:
        st.write(i)
        st.write(data[0]['reviewer_age'])
        for j in range(len(data[str(i)]['reviewer_age'])): 
            st.write(j)
            age.append(data[i]['reviewer_age'][j])
            rating.append(data[i]['ratings'][j])
            recommend.append(data[i]['recommend'][j])
            names = data[i]['product_category'].split('/')
            department_name.append(names[0])
            division_name.append(names[1])
            class_name.append(names[2])
    df = pd.DataFrame({'Age': age, 'Rating': rating, 'Recommended IND': recommend, 'Department Name': department_name, 'Division Name': division_name, 'Class Name': class_name})
    return df