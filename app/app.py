import streamlit as st
from top5_car import get_top_5_cars, parse_car_data
import pandas as pd

st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        color: #2E86C1;
        font-weight: bold;
    }
    .subheader {
        font-size: 24px;
        color: #117A65;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_URL = "http://127.0.0.1:8000/api"

st.markdown('<div class="title">🚗 국내 자동차 현황</div>', unsafe_allow_html=True)

menu = st.sidebar.selectbox(
    "📋 메뉴를 선택하세요",
    ["국내 자동차 수요", "사고 추이 분석", "자동차 Top 5 정보"],
    index=0
)

if menu == "국내 자동차 수요":
    st.markdown('<div class="subheader">📊 국내 자동차 수요 분석</div>', unsafe_allow_html=True)
    st.write("국내 자동차 수요에 대한 트렌드 분석")

elif menu == "사고 추이 분석":
    st.markdown('<div class="subheader">🚦 자동차 사고 추이</div>', unsafe_allow_html=True)
    st.write("자동차 수요 증가에 따른 사고 발생 현황 분석")

elif menu == "자동차 Top 5 정보":
    st.markdown('<div class="title">🏆 국내 자동차 Top 5 정보</div>', unsafe_allow_html=True)
    raw_data = get_top_5_cars()

    if "🚨" not in raw_data:
        car_data = parse_car_data(raw_data)

        # 데이터를 브랜드별로 그룹화
        grouped_data = {}
        for entry in car_data:
            brand = entry["브랜드"]
            if brand not in grouped_data:
                grouped_data[brand] = []
            grouped_data[brand].append({"정보": entry["정보"], "내용": entry["내용"]})

        # 브랜드별로 테이블 출력
        for brand, details in grouped_data.items():
            st.markdown(f"### {brand}")
            df = pd.DataFrame(details)
            st.table(df)

        st.success("브랜드별 테이블을 성공적으로 생성했습니다!")
    else:
        st.error("데이터를 가져오는 데 실패했습니다.")