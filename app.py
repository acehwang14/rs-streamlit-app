# rs-streamlit-app# 📊 종목별 상대강도(RS) 분석 Streamlit 앱 - 1차 버전

import streamlit as st
import pandas as pd

# 앱 제목
st.title("📈 종목별 상대강도(RS) 분석")

# 설명글
st.write("""
종목들의 현재가를 기준으로 상대강도(RS)를 계산하여,
기준 지수(KOSPI, S&P500 등) 대비 강한 종목을 빠르게 찾아드립니다.
""")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (종목명, 현재가)", type=["csv"])

# 또는 수동 입력
st.write("또는 직접 입력하세요:")
manual_input = st.text_area("형식: 종목명,현재가 (쉼표 구분, 한 줄에 하나)", height=150)

# 기준 지수 입력
st.header("기준 지수 설정")
index_price = st.number_input("기준 지수 현재가 입력 (예: KOSPI 2600)", min_value=0.0, format="%.2f")

# 계산 버튼
if st.button("RS 계산하기"):
    # 데이터 불러오기
    if uploaded_file is not None:
        stocks = pd.read_csv(uploaded_file)
    elif manual_input.strip() != "":
        # 수동 입력 처리
        lines = manual_input.strip().split("\n")
        data = [line.split(",") for line in lines]
        stocks = pd.DataFrame(data, columns=["종목명", "현재가"])
        stocks["현재가"] = stocks["현재가"].astype(float)
    else:
        st.warning("파일 업로드 또는 직접 입력을 해주세요.")
        st.stop()

    if index_price == 0:
        st.warning("기준 지수 현재가를 입력해주세요.")
        st.stop()

    # RS 계산
    stocks['RS'] = stocks['현재가'] / index_price

    # RS 높은 순 정렬
    stocks_sorted = stocks.sort_values(by='RS', ascending=False).reset_index(drop=True)

    # 결과 출력
    st.subheader("📋 RS 분석 결과")
    st.dataframe(stocks_sorted)

    # 다운로드 버튼
    csv = stocks_sorted.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="CSV 파일로 다운로드",
        data=csv,
        file_name='rs_result.csv',
        mime='text/csv'
    )

# 하단 노트
st.write("---")
st.caption("Made for 황팀장님 by ChatGPT 🚀")
