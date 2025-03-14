import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca dataset
day_df = pd.read_csv('dashboard/day.csv')
hour_df = pd.read_csv('dashboard/hour.csv')

# Mapping Musim dan Situasi Cuaca
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
weather_mapping = {
    1: 'Clear',
    2: 'Mist',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Snow'
}

day_df['season_label'] = day_df['season'].map(season_mapping)
day_df['weather_label'] = day_df['weathersit'].map(weather_mapping)
hour_df['season_label'] = hour_df['season'].map(season_mapping)
hour_df['weather_label'] = hour_df['weathersit'].map(weather_mapping)

# Header Dashboard
st.title("Dashboard Analisis Penggunaan Sepeda")
st.sidebar.title("Filter Data")

# Sidebar Filters
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim", 
    options=day_df['season_label'].unique(), 
    default=day_df['season_label'].unique()
)

selected_weather = st.sidebar.multiselect(
    "Pilih Situasi Cuaca", 
    options=day_df['weather_label'].unique(), 
    default=day_df['weather_label'].unique()
)

# Filter Data
filtered_day_df = day_df[
    (day_df['season_label'].isin(selected_seasons)) &
    (day_df['weather_label'].isin(selected_weather))
]

# Visualisasi 1: Clustered Bar Chart
st.subheader("Pengaruh Musim dan Situasi Cuaca terhadap Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x='season_label',
    y='cnt',
    hue='weather_label',
    data=filtered_day_df,
    palette='coolwarm',
    ax=ax
)
ax.set_title("Penggunaan Sepeda Berdasarkan Musim dan Situasi Cuaca")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penggunaan Sepeda")
st.pyplot(fig)

# Visualisasi 2: Histogram Distribusi Kecepatan Angin
st.subheader("Distribusi Kecepatan Angin")
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(day_df['windspeed'], bins=20, color='skyblue', edgecolor='black')
ax.set_title("Distribusi Kecepatan Angin")
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Visualisasi 3: Scatter Plot Windspeed vs Penggunaan Sepeda
st.subheader("Hubungan Kecepatan Angin dengan Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x='windspeed', y='cnt', data=day_df, alpha=0.6, ax=ax)
ax.set_title("Kecepatan Angin vs Penggunaan Sepeda")
ax.set_xlabel("Kecepatan Angin (windspeed)")
ax.set_ylabel("Jumlah Penggunaan Sepeda")
st.pyplot(fig)

# Visualisasi 4: Scatter Plot dengan Garis Tren
st.subheader("Tren Hubungan Kecepatan Angin dengan Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(x='windspeed', y='cnt', data=day_df, scatter_kws={'alpha':0.6}, line_kws={'color':'red'}, ax=ax)
ax.set_title("Scatter Plot dengan Tren Garis")
ax.set_xlabel("Kecepatan Angin (windspeed)")
ax.set_ylabel("Jumlah Penggunaan Sepeda")
st.pyplot(fig)

# Visualisasi 5: Boxplot Kecepatan Angin
st.subheader("Pengaruh Kategori Kecepatan Angin terhadap Penggunaan Sepeda")
bins = [0, 10, 20, 30]
labels = ['Low', 'Medium', 'High']
day_df['windspeed_category'] = pd.cut(day_df['windspeed'], bins=bins, labels=labels)

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='windspeed_category', y='cnt', data=day_df, palette='pastel', ax=ax)
ax.set_title("Pengaruh Kecepatan Angin pada Penggunaan Sepeda")
ax.set_xlabel("Kategori Kecepatan Angin")
ax.set_ylabel("Jumlah Penggunaan Sepeda")
st.pyplot(fig)
