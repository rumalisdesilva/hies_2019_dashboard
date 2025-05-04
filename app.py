import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="HIES 2019 Dashboard", layout="wide")

# Sidebar content
st.sidebar.title("📘 About This Dashboard")
st.sidebar.markdown("""
This interactive dashboard presents insights from the **Household Income and Expenditure Survey (HIES) 2019** conducted by the **Department of Census and Statistics, Sri Lanka**.

---

**Author:** Rumali De Silva  
**Student ID:** [20231677]  
**Module:** Data Science Project Lifecycle  
**Institution:** IIT

---

✅ Use the filters and visualizations to explore household expenditure patterns across Sri Lanka.
""")


# Title
st.title("🇱🇰 Sri Lanka HIES 2019 Household Expenditure Dashboard")



# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/hies_2019_expanded_expenditure_dataset.csv")
    return df

df = load_data()
# KPIs Section
st.markdown("## 📈 Key Insights")
col1, col2, col3 = st.columns(3)

with col1:
    total_expenditure = df['Expenditure_Rs'].sum()
    st.metric("💰 Total Expenditure", f"Rs. {total_expenditure:,.0f}")

with col2:
    category_count = df['Category'].nunique()
    st.metric("📦 Number of Categories", category_count)

with col3:
    record_count = df.shape[0]
    st.metric("📄 Total Records", record_count)
...


# Raw data preview
if st.checkbox("Show Raw Data"):
    st.subheader("📄 Preview of Dataset")
    st.write(df.head())

# Summary statistics
st.subheader("📊 Summary Statistics")
st.write(df.describe())

# Missing values
st.subheader("🔍 Missing Values in Each Column")
st.write(df.isnull().sum())

# Histogram of Expenditure_Rs
if 'Expenditure_Rs' in df.columns:
    st.subheader("💰 Distribution of Expenditure (Rs.)")
    fig1 = px.histogram(df, x='Expenditure_Rs', nbins=50, title="Distribution of Expenditure by Category")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Column 'Expenditure_Rs' not found in the dataset.")

# Dropdown filter: Select District
if 'District' in df.columns:
    st.subheader("🏙️ Filter by District")
    selected_district = st.selectbox("Choose a District:", df['District'].unique())

    # Filter the data by selected district
    filtered_df = df[df['District'] == selected_district]

    # Bar chart: Average Expenditure by Category (for selected District)
    st.subheader(f"📊 Average Expenditure by Category in {selected_district}")
    if 'Category' in df.columns and 'Expenditure_Rs' in df.columns:
        bar_data = (
            filtered_df.groupby('Category')['Expenditure_Rs']
            .mean()
            .reset_index()
            .sort_values(by='Expenditure_Rs', ascending=False)
        )
        fig2 = px.bar(
            bar_data,
            x='Category',
            y='Expenditure_Rs',
            title=f"Average Expenditure by Category - {selected_district}",
            labels={'Expenditure_Rs': 'Average Expenditure (Rs.)'},
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Required columns 'Category' and 'Expenditure_Rs' not found.")
else:
    st.warning("Column 'District' not found in the dataset.")

    # Download button for filtered data
st.subheader(f"⬇️ Download Filtered Data for {selected_district}")
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"expenditure_data_{selected_district}.csv",
    mime='text/csv'
)


# Box Plot: Expenditure Distribution by Category
if 'Category' in df.columns and 'Expenditure_Rs' in df.columns:
    st.subheader("📦 Expenditure Distribution by Category")
    fig3 = px.box(
        df,
        x='Category',
        y='Expenditure_Rs',
        title="Box Plot of Expenditure (Rs.) by Category",
        labels={'Expenditure_Rs': 'Expenditure (Rs.)'},
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Columns 'Category' and/or 'Expenditure_Rs' not found in the dataset.")


# Pie Chart: Share of Total Expenditure by Category
if 'Category' in df.columns and 'Expenditure_Rs' in df.columns:
    st.subheader("🥧 Share of Total Expenditure by Category")
    pie_data = (
        df.groupby('Category')['Expenditure_Rs']
        .sum()
        .reset_index()
        .sort_values(by='Expenditure_Rs', ascending=False)
    )

    fig4 = px.pie(
        pie_data,
        names='Category',
        values='Expenditure_Rs',
        title='Proportion of Total Expenditure by Category',
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("Columns 'Category' and/or 'Expenditure_Rs' not found in the dataset.")
