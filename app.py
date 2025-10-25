import streamlit as st
import pandas as pd

# -------------------------
# 1️⃣ 데이터 불러오기
# -------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
    df = pd.read_csv(url)
    df = df.dropna(subset=["horsepower", "weight", "mpg"])
    df["horsepower"] = df["horsepower"].astype(float)
    return df

df = load_data()

# -------------------------
# 2️⃣ 제목
# -------------------------
st.title("🚗 자동차 성능 비교 웹앱")
st.markdown("데이터 출처: [Seaborn MPG Dataset](https://github.com/mwaskom/seaborn-data)")

# -------------------------
# 3️⃣ 자동차 선택
# -------------------------
car_names = sorted(df['name'].unique())

col1, col2 = st.columns(2)
with col1:
    car1 = st.selectbox("비교할 자동차 1️⃣", car_names, index=0)
with col2:
    car2 = st.selectbox("비교할 자동차 2️⃣", car_names, index=1)

# -------------------------
# 4️⃣ 선택한 자동차 정보 표시
# -------------------------
data1 = df[df["name"] == car1].iloc[0]
data2 = df[df["name"] == car2].iloc[0]

st.subheader("📊 자동차 스펙 비교")

comparison = pd.DataFrame({
    "항목": ["연비 (mpg)", "마력 (horsepower)", "무게 (weight)", "모델 연도 (model year)"],
    car1: [data1["mpg"], data1["horsepower"], data1["weight"], data1["model_year"]],
    car2: [data2["mpg"], data2["horsepower"], data2["weight"], data2["model_year"]],
})

st.dataframe(comparison, use_container_width=True)

# -------------------------
# 5️⃣ 시각화
# -------------------------
st.subheader("📈 성능 비교 그래프")

numeric_cols = ["mpg", "horsepower", "weight"]
chart_df = pd.DataFrame({
    "항목": numeric_cols,
    car1: [data1[col] for col in numeric_cols],
    car2: [data2[col] for col in numeric_cols]
}).set_index("항목")

st.bar_chart(chart_df)

# -------------------------
# 6️⃣ 간단한 분석
# -------------------------
st.subheader("🧠 요약 비교 분석")

def compare_value(a, b, higher_is_better=True):
    if a == b:
        return "⚖️ 두 차량은 동일합니다."
    elif (a > b and higher_is_better) or (a < b and not higher_is_better):
        return f"✅ **{car1}** 이 더 우수합니다."
    else:
        return f"✅ **{car2}** 이 더 우수합니다."

st.markdown(f"**연비:** {compare_value(data1['mpg'], data2['mpg'])}")
st.markdown(f"**마력:** {compare_value(data1['horsepower'], data2['horsepower'])}")
st.markdown(f"**무게:** {compare_value(data1['weight'], data2['weight'], higher_is_better=False)}")

st.info("💡 Streamlit 앱은 GitHub 저장 후 `streamlit run car_compare_app.py` 명령어로 실행할 수 있습니다.")
