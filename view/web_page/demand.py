import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
image_path_hyundai = os.path.join(project_root, "view", "assets", "hyundai_logo.png")

from view.components.image_encoding import image_to_base64
image_base64_hyundai = image_to_base64(image_path_hyundai)

import streamlit as st
from view.service.hyundai_analysis import render_hyundai_analysis


def run():
    st.title("📈 수요 분석")
    st.markdown("""
    ### 주요 5사 수요 트렌드
    국내 주요 5대 자동차 제조사의 친환경 자동차 수요 데이터를 분석합니다.
    """)

    st.info("💡 월별 수요 데이터와 수요 비중을 확인할 수 있습니다.")

    render_hyundai_analysis(image_base64_hyundai)