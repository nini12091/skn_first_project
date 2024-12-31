import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000/api"

st.title("FastAPI & Streamlit Integration")

st.header("GET Request Example")
item_id = st.text_input("Enter Item ID", "1")
if st.button("Fetch Item"):
    response = requests.get(f"{BASE_URL}/items/{item_id}", params={"q": "test_query"})
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")

# POST 요청 예제
st.header("POST Request Example")
name = st.text_input("Item Name")
description = st.text_area("Description")
price = st.number_input("Price", min_value=0.0, step=0.01)
tax = st.number_input("Tax", min_value=0.0, step=0.01)

if st.button("Create Item"):
    payload = {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax,
    }
    response = requests.post(f"{BASE_URL}/items/", json=payload)
    if response.status_code == 200:
        st.success("Item Created Successfully!")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")