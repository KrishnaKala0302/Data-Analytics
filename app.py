import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from setup_db import create_connection,create_user,create_user_table,authenticate_user


st.set_page_config(
    page_title='Budget Tracker'
)
st.title(':blue[Budget Tracker]')


#init session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False
if 'user_id' not in st.session_state:
    st.session_state.user_id=None
    
signup_tab,login_tab,category_tab=st.tabs(['SignUp','Login','Add and Manage Category '])

with signup_tab:
    username=st.text_input('Choose your user id',key='signup')
    password=st.text_input('Choose your password',type='password',key='password')
    signup_button=st.button('Create your Account',key='account')
    
    if signup_button:
        if username and password:
            try:
                 create_user(username,password) 
                 st.success('Account created succesfully. Go to the login page')
            except sqlite3.IntegrityError:
                st.error('Username already exists')
                
        else:
            st.warning('Please provide username and password')
            
with login_tab:
        username=st.text_input('Enter your user id',key='login')
        password=st.text_input('Enter your password',type='password',key='loginpassword')
        login_button=st.button('Login',key='loginbutton')
        
        if login_tab:
             if username and password:
                user_id=authenticate_user(username,password)
                if user_id:
                    st.session_state.logged_in=True
                    st.session_state.user_id = user_id
                    st.success(f'Welcome {username}, Let us track your budget')
                else:
                    st.error('Invalid username or password')
        else:
            st.warning('Please enter username and password')
            
if st.session_state.logged_in:
    with category_tab:
        def add_category(category_name,category_type):
            conn=create_connection()
            c=conn.cursor()
            c.execute('INSERT INTO categories_table(user_id,category_name,category_type) VALUES (?,?,?)',
                      (st.session_state.user_id[0],category_name,category_type))
            conn.commit()
            conn.close()
            
        def display_categories():
            conn=create_connection()
            c=conn.cursor()
            c.execute('SELECT category_name,category_type FROM categories_table WHERE user_id=?',(st.session_state.user_id[0],))
            categories=c.fetchall()
            conn.close()
            
            if categories:
                df=pd.DataFrame(categories,columns=['Category Name','Category Type'])
                st.subheader('Your Category Table')
                st.dataframe(df)
                data=df['Category Type'].value_counts().reset_index()
                st.subheader('Analyse your expense and income and saving source')
                fig=px.bar(data_frame=data,x='Category Type',y='count',text='count')
                st.plotly_chart(fig)
            else:
                st.write(':red[No Categories Found. Please add categories]')
                
                
        st.subheader('Add and Manage Categories')
        category_name=st.text_input('Subcategory',key='subcategory')
        category_type=st.selectbox('Category Type',options=['expense','income','savings'])
        category_button=st.button("Add Category",key='categorybutton')
        
        if category_button:
            if category_name:
                add_category(category_name,category_type)
                st.success('Category Added Succesfully')
            else:
                st.warning('Please enter Category name')
                
        display_categories()