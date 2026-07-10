import streamlit as st

st.title("🚀 My First Cloud App")
st.write("Hello World! This app is successfully running.")
user_input = st.text_input("Type your name here:")
if user_input:
    st.write(f"Welcome to the cloud, {user_input}!")