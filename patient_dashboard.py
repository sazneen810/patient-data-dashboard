import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# --- Load & clean data ---
df = pd.read_excel("Patient Dataset.xlsx", sheet_name='Table 1')
df['Blast Cell %'] = df['Blast Cell %'].str.rstrip('%').astype(float)

# --- Normalize numeric values ---
scaler = MinMaxScaler()
numeric_cols = ['Age (years)', 'Hemoglobin Level (g/dL)', 'WBC Count (10^3/µL)', 'Blast Cell %', 'Survival Time (months)']
df_scaled = df.copy()
df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# --- Sidebar Filters ---
st.sidebar.header("Filter Patients")

gender = st.sidebar.selectbox("Select Gender", options=["All"] + list(df["Gender"].unique()))
age_range = st.sidebar.slider("Age Range", int(df["Age (years)"].min()), int(df["Age (years)"].max()), (20, 70))

# --- Filter Data ---
df_filtered = df.copy()
if gender != "All":
    df_filtered = df_filtered[df_filtered["Gender"] == gender]
df_filtered = df_filtered[(df_filtered["Age (years)"] >= age_range[0]) & (df_filtered["Age (years)"] <= age_range[1])]

# --- Main Dashboard ---
st.title("🩺 Patient Data Dashboard")
st.write("Explore trends and correlations in clinical indicators of 10 patients.")

# 1. Histogram
st.subheader("Hemoglobin Distribution")
st.plotly_chart(px.histogram(df_filtered, x="Hemoglobin Level (g/dL)", nbins=10))

# 2. Scatter Plot
st.subheader("WBC Count vs Blast Cell %")
st.plotly_chart(px.scatter(df_filtered, x="WBC Count (10^3/µL)", y="Blast Cell %", color="Gender"))

# 3. 3D Scatter Plot
st.subheader("3D Scatter: Age, Hemoglobin, Survival Time")
st.plotly_chart(px.scatter_3d(df_filtered,
    x="Age (years)", y="Hemoglobin Level (g/dL)", z="Survival Time (months)", color="Gender"))

# 4. Parallel Coordinates
st.subheader("Multivariate: Parallel Coordinates Plot")
st.plotly_chart(px.parallel_coordinates(df_filtered,
    dimensions=numeric_cols, color="Survival Time (months)"))

# 5. Correlation Heatmap
st.subheader("Correlation Heatmap")
st.plotly_chart(px.imshow(df_filtered[numeric_cols].corr(), text_auto=True, color_continuous_scale="RdBu_r"))

# 6. Survival Time per Patient
st.subheader("Survival Time by Patient")
st.plotly_chart(px.bar(df_filtered, x="Patient ID", y="Survival Time (months)", color="Gender"))

# --- Data Table ---
st.subheader("Filtered Data Table")
st.dataframe(df_filtered)
