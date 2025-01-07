import os
import streamlit as st
from view.utils.file_loader import load_data_from_csv

# FAQ 페이지 함수
def run():
    st.title("❓ 자주 묻는 질문 FAQ")

    # CSS 스타일 추가
    st.markdown(
        """
        <style>
        .pagination-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
        }
        .pagination-button {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            color: #333;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .pagination-button:hover {
            background-color: #e0e0e0;
        }
        .pagination-button:disabled {
            background-color: #f2f2f2;
            color: #aaa;
            cursor: not-allowed;
        }
        .page-info {
            text-align: center;
            font-size: 14px;
        }
        .gray-box {
            background-color: #f2f2f2;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # CSV 파일 경로
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "hyundai_faq.csv")

    # 데이터 로드
    faq_data = load_data_from_csv(csv_path)

    if faq_data.empty:
        st.warning("FAQ 데이터를 로드하지 못했습니다.")
        return

    # 브랜드 선택
    st.subheader("브랜드 선택")
    brands = ["전체"] + list(faq_data["Brand"].unique())
    selected_brand = st.selectbox("브랜드를 선택하세요:", brands)

    # 브랜드 필터링
    if selected_brand != "전체":
        faq_data = faq_data[faq_data["Brand"] == selected_brand]

    # 검색어 입력
    search_query = st.text_input("궁금하신 키워드를 검색하세요:")

    # 카테고리 선택 (라디오 버튼)
    st.subheader("카테고리 선택")
    categories = ["전체"] + list(faq_data["Category"].unique())
    selected_category = st.radio("카테고리를 선택하세요:", categories, horizontal=True)

    # 세션 상태 초기화 (필터 변경 시)
    if (
        "previous_category" not in st.session_state
        or st.session_state.previous_category != selected_category
        or st.session_state.previous_brand != selected_brand
        or st.session_state.previous_query != search_query
    ):
        st.session_state.current_page = 1
        st.session_state.previous_category = selected_category
        st.session_state.previous_brand = selected_brand
        st.session_state.previous_query = search_query

    # 카테고리 필터링
    if selected_category != "전체":
        faq_data = faq_data[faq_data["Category"] == selected_category]

    # 검색어 필터링
    if search_query:
        faq_data = faq_data[
            faq_data["Question"].str.contains(search_query, case=False, na=False) |
            faq_data["Answer"].str.contains(search_query, case=False, na=False)
        ]

    # 페이지네이션 처리
    st.subheader(f"질문 목록 ({len(faq_data)}개)")
    if not faq_data.empty:
        # 페이지당 항목 수
        items_per_page = 10

        # 총 페이지 수 계산
        total_pages = (len(faq_data) - 1) // items_per_page + 1

        # 현재 페이지 데이터 추출
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_data = faq_data.iloc[start_idx:end_idx]

        # 현재 페이지 데이터 출력
        for index, row in current_data.iterrows():
            with st.expander(f"❓ {row['Question']}"):
                st.markdown(
                    f'<div class="gray-box">{row["Answer"]}</div>',
                    unsafe_allow_html=True,
                )

        # 버튼을 FAQ 끝과 맞추기 위한 레이아웃
        col1, col2, col3 = st.columns([1, 8, 1])

        with col1:
            if st.button("이전", key="prev", disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page -= 1

        with col3:
            if st.button("다음", key="next", disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page += 1

        # 페이지 정보 표시
        with col2:
            st.markdown(
                f"<div class='page-info'>페이지 {st.session_state.current_page} / {total_pages}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("검색 결과가 없습니다.")
