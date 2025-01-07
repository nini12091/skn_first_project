import streamlit as st

def run():
    st.title("🚗 친환경 자동차 현황 및 데이터 통합 플랫폼")
    st.markdown("""
    국내 전기차 및 하이브리드 자동차 관련 정보를 한눈에 제공합니다.  
    왼쪽 사이드바에서 원하는 페이지를 선택하세요!  
    """)

    st.markdown("### 주요 기능")
    st.write("1️⃣ **친환경 자동차 등록 현황 페이지**: 친환경 자동차의 지역 및 차종별 등록 현황 확인 📊")
    st.write("2️⃣ **국내 주요 5사 자동차 분석 페이지**: 국내 자동차 주요 5사 친환경 자동차의 수요 데이터 분석📈")
    st.write("3️⃣ **FAQ 페이지**: 자주 묻는 질문 모음 ❓")