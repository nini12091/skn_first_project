import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

import streamlit as st

def run():
    st.title("❓ FAQ (자주 묻는 질문)")
    st.markdown("""
        ### 현대자동차 FAQ
        카테고리별로 자주 묻는 질문과 답변을 확인하세요.
        """)