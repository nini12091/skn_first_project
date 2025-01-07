import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

import os
import pandas as pd
import streamlit as st
import mysql.connector

def load_excel(sheet_name: str, file_name: str = "hyundai_demand.xlsx", header: int = 2):

    file_path = os.path.join(project_root, "data", "raw", file_name)
    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name, header=header)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found in '{file_path}'")

@st.cache_data
def load_data_from_csv(csv_path):
    if not os.path.exists(csv_path):
        st.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        return pd.DataFrame()
    data = pd.read_csv(csv_path, encoding="utf-8")

    data['Question'] = data['Question'].str.replace(r"\[.*?\]\\n", "", regex=True)
    data['Question'] = data['Question'].str.replace(r"\\n", " ", regex=True)

    data['Answer'] = data['Answer'].str.replace(r"\\n", "\n", regex=True)
    return data