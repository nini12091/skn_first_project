import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from view.utils.file_loader import load_excel
from view.utils.data_cleaning import filter_hev_ev
import streamlit as st
from view.components.chart import plot_monthly_trends

def process_hyundai_data(sheet_name="Unit Sales by Model"):
    try:
        # 현대 자동차 데이터 로드
        data = load_excel(sheet_name=sheet_name, file_name="hyundai_demand.xlsx", header=2)
        # 데이터 필터링
        model_list, monthly_sales = filter_hev_ev(data, model_column="Unnamed: 2", month_start="Jan.", month_end="Dec.")
        return model_list, monthly_sales
    except FileNotFoundError:
        return [], None

def render_hyundai_analysis(image_base64):
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="data:image/png;base64,{image_base64}" alt="Hyundai Logo" style="width: 50px;">
            <h2 style="margin: 0;">현대 자동차</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_list, monthly_sales = process_hyundai_data(sheet_name="Unit Sales by Model")
    if model_list and monthly_sales is not None:
        col1, col2 = st.columns([1, 2])

        # 모델 리스트
        with col1:
            st.markdown("#### 현대 친환경 자동차 리스트")
            st.markdown(
                """
                <style>
                .scrollable-container {
                    overflow-y: auto;
                    height: 400px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                }
                .card {
                    padding: 10px;
                    margin-bottom: 10px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    font-size: 14px;
                    font-weight: bold;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            styled_cards = "<div class='scrollable-container'>"
            for model in model_list:
                styled_cards += f"<div class='card'>🚗 {model}</div>"
            styled_cards += "</div>"
            st.markdown(styled_cards, unsafe_allow_html=True)

        # 월별 수요 데이터 시각화
        with col2:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
                    <h4 style="text-align: center;">2023년 월별 친환경 자동차 수요</h4>
                    <div>
                """,
                unsafe_allow_html=True,
            )
            st.pyplot(plot_monthly_trends(monthly_sales, title="Hyundai Monthly Trends"))
            st.markdown("</div></div>", unsafe_allow_html=True)