import os
import sys
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

import pandas as pd
import streamlit as st
from database.database_read import load_data_from_database
#
# def filter_hev_ev(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.", month_end: str = "Dec."):
#     data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")
#     filtered_data = data_fixed[data_fixed[model_column].str.contains("HEV|EV", na=False, case=False)]
#     model_list = filtered_data[model_column].tolist()
#
#     monthly_data = filtered_data.loc[:, month_start:month_end].apply(pd.to_numeric, errors='coerce')
#     monthly_data.index = filtered_data[model_column]
#
#     return model_list, monthly_data

def make_dataframe():
    data = load_data_from_database()
    print(data)
    # df = pd.DataFrame(data, columns=['id', 'brand', 'category', 'question', 'answer'])
    # print(df)
    # df['Question'] = df['Question'].str.replace(r"\[.*?\]\\n", "", regex=True)
    # df['Question'] = df['Question'].str.replace(r"\\n", " ", regex=True)
    # df['Answer'] = df['Answer'].str.replace(r"\\n", "\n", regex=True)

    # return df

make_dataframe()