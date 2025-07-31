import streamlit as st
import requests

st.title("AlgoTrade MVP")
if st.button("Ping Backend"):
    r = requests.get("http://localhost:8000/ping")
    st.write(r.json())
