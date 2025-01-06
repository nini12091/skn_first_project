import streamlit as st
import web_page.registration as registration
import web_page.demand as demand
import web_page.faq as faq
import web_page.home as home

# 페이지 기본 설정
st.set_page_config(
    page_title="친환경 자동차 현황",
    page_icon="🚗",
    layout="wide"
)

# 사이드바 메뉴
st.sidebar.title("📂 MENU")
menu = st.sidebar.radio(
    "페이지를 선택하세요:",
    ["🏠 Home", "📊 친환경 자동차 등록 현황", "📈 국내 주요 5사 자동차 분석", "❓ FAQ"],
    key="main_menu"
)

# 각 메뉴에 따라 페이지 로드
if menu == "🏠 Home":
    home.run()
elif menu == "📊 친환경 자동차 등록 현황":
    registration.run()
elif menu == "📈 국내 주요 5사 자동차 분석":
    demand.run()
elif menu == "❓ FAQ":
    faq.run()