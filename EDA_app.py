import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Market Sales Analysis - Client ABC", layout="wide")

# =======================
# LOAD & CLEAN DATA
# =======================
@st.cache_data
def load_data():
    df = pd.read_excel("DS Internship - EDA - Data.xlsx")
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    df['Store_Open'] = pd.to_datetime(df['Store_Open'])
    df['Store_Close'] = df['Store_Close'].astype(str)
    df['Store_Modification'] = df['Store_Modification'].astype(str)
    return df

df = load_data()

st.title("📊 Market Sales Analysis for Client ABC")
st.markdown("This dashboard presents exploratory insights from ABC's retail store data across the U.S. from **2015 to 2020**.")

st.markdown("""
**Submitted by:** [Tusha Rahul](https://tusharahul.netlify.app)  
**Assignment:** *EDA Project for Tiger Analytics Internship*
""")

# =======================
# UTILITY FUNCTION
# =======================
def question_block(question, answer_fn, code_str):
    st.markdown(f"### 📌 {question}")
    answer_fn()
    with st.expander("🔍 Show Code"):
        st.code(code_str, language='python')
    st.markdown("---")


# =======================
# QUESTION 1 - Total Sales by Year
# =======================
def q1():
    result = df.groupby('Year')['Sales'].sum()
    st.bar_chart(result)

q1_code = """result = df.groupby('Year')['Sales'].sum()
st.bar_chart(result)"""

question_block("1. Total Sales by Year", q1, q1_code)


# =======================
# QUESTION 2 - Stores Opened in 1991
# =======================
def q2():
    stores_1991 = df[df['Store_Open'].dt.year == 1991]['Store'].nunique()
    st.metric("Stores opened in 1991", stores_1991)

q2_code = """stores_1991 = df[df['Store_Open'].dt.year == 1991]['Store'].nunique()
st.metric("Stores opened in 1991", stores_1991)"""

question_block("2. Number of Stores Opened in 1991", q2, q2_code)


# =======================
# QUESTION 3 - Remodeled Stores
# =======================
def q3():
    remodeled = df[df['Store_Modification'].str.lower().notna()]['Store'].nunique()
    st.metric("Remodeled Stores", remodeled)

q3_code = """remodeled = df[df['Store_Modification'].str.lower().notna()]['Store'].nunique()
st.metric("Remodeled Stores", remodeled)"""

question_block("3. Number of Stores Remodeled", q3, q3_code)


# =======================
# QUESTION 4 - Sales vs Sq. Ft.
# =======================
def q4():
    store_avg = df.groupby('Store')[['Sales', 'Total_Sq_Ft']].mean()
    fig, ax = plt.subplots()
    sns.scatterplot(data=store_avg, x='Total_Sq_Ft', y='Sales', ax=ax)
    st.pyplot(fig)
    corr = store_avg['Sales'].corr(store_avg['Total_Sq_Ft'])
    st.success(f"Correlation between Sales and Total Sq. Ft.: {corr:.2f}")

q4_code = """store_avg = df.groupby('Store')[['Sales', 'Total_Sq_Ft']].mean()
fig, ax = plt.subplots()
sns.scatterplot(data=store_avg, x='Total_Sq_Ft', y='Sales', ax=ax)
st.pyplot(fig)
corr = store_avg['Sales'].corr(store_avg['Total_Sq_Ft'])
st.success(f"Correlation: {corr:.2f}")"""

question_block("4. Direct Relationship Between Sales and Total Sq. Ft.", q4, q4_code)


# =======================
# QUESTION 5 - Most Profitable Super Division
# =======================
def q5():
    result = df.groupby('Super_Division')['Sales'].sum().sort_values(ascending=False).reset_index()
    result.columns = ['Super Division', 'Total Sales']
    st.dataframe(result.style.format({"Total Sales": "${:,.2f}"}))


q5_code = """result = df.groupby('Super_Division')['Sales'].sum().sort_values(ascending=False).reset_index()
result.columns = ['Super Division', 'Total Sales']
st.dataframe(result.style.format({"Total Sales": "${:,.2f}"}))"""


question_block("5. Most Profitable Super Division", q5, q5_code)


# =======================
# QUESTION 6 - Active Stores
# =======================
def q6():
    active = df[df['Store_Close'] == 'No Close date']['Store'].nunique()
    st.metric("Active Stores as of Today", active)

q6_code = """active = df[df['Store_Close'] == 'No Close date']['Store'].nunique()
st.metric("Active Stores", active)"""

question_block("6. Number of Active Stores", q6, q6_code)


# =======================
# QUESTION 7 - Super Division with Max Avg Sq Ft
# =======================
def q7():
    result = df.groupby('Super_Division')['Total_Sq_Ft'].mean().sort_values(ascending=False).reset_index()
    result.columns = ['Super Division', 'Avg Sq. Ft.']
    st.dataframe(result.style.format({"Avg Sq. Ft.": "{:,.2f}"}))

q7_code = """result = df.groupby('Super_Division')['Total_Sq_Ft'].mean().sort_values(ascending=False).reset_index()
result.columns = ['Super Division', 'Avg Sq. Ft.']
st.dataframe(result.style.format({"Avg Sq. Ft.": "{:,.2f}"}))"""


question_block("7. Super Division with Highest Average Sq. Ft.", q7, q7_code)


# =======================
# QUESTION 8 - Top 3 Candidate States
# =======================
def q8():
    state_sales = df.groupby('State').agg({'Sales': 'mean', 'Total_Sq_Ft': 'mean'}).sort_values('Sales', ascending=False)
    st.dataframe(state_sales.head(3).style.format({"Sales": "${:,.2f}", "Total_Sq_Ft": "{:,.2f}"}))

q8_code = """state_sales = df.groupby('State').agg({'Sales': 'mean', 'Total_Sq_Ft': 'mean'}).sort_values('Sales', ascending=False)
st.dataframe(state_sales.head(3))"""

question_block("8. Top 3 Potential Candidate States for Expansion", q8, q8_code)


# =======================
# QUESTION 9 - Best Time to Open a Store
# =======================
def q9():
    result = df.groupby('Month')['Sales'].mean().sort_values(ascending=False)
    st.line_chart(result)

q9_code = """result = df.groupby('Month')['Sales'].mean().sort_values(ascending=False)
st.line_chart(result)"""

question_block("9. Best Time of the Year to Open a Store", q9, q9_code)


# =======================
# QUESTION 10 - Outlet-Type and Closures
# =======================
def q10():
    df_temp = df.copy()
    df_temp['Closed'] = df_temp['Store_Close'] != 'No Close date'
    result = df_temp.groupby('Outlet_Type')['Closed'].mean().sort_values(ascending=False)
    st.dataframe(result.map(lambda x: f"{x:.2%}").rename("Closure Rate"))

q10_code = """df_temp = df.copy()
df_temp['Closed'] = df_temp['Store_Close'] != 'No Close date'
result = df_temp.groupby('Outlet_Type')['Closed'].mean().sort_values(ascending=False)
st.dataframe(result.map(lambda x: f"{x:.2%}"))"""

question_block("10. Outlet-Type Effect on Store Closures", q10, q10_code)


st.markdown("---")
st.markdown(
    "📄 Created by [Tusha Rahul](https://tusharahul.netlify.app) for **Tiger Analytics** Internship Assignment"
)
