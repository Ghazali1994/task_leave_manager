import streamlit as st
from db import SessionLocal, User

def login():
    session = SessionLocal()
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            st.session_state.user = user.username
            st.success("Logged in as " + user.username)
        else:
            st.error("Invalid credentials")
    session.close()

def signup():
    session = SessionLocal()
    st.sidebar.subheader("Sign Up")
    username = st.sidebar.text_input("New Username")
    password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Create Account"):
        if session.query(User).filter_by(username=username).first():
            st.error("Username already exists")
        else:
            session.add(User(username=username, password=password))
            session.commit()
            st.success("Account created!")
    session.close()
