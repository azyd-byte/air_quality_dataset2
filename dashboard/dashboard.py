import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set(style="dark")


def create_co_mean_all_df(df):
    co_mean_all_df = df.resample(rule='M', on='date').agg({
        "CO": "mean"
    }).reset_index()
    co_mean_all_df.rename(columns={
        "TEMP": "temperatur"
    }, inplace=True)
    return co_mean_all_df


def create_pm10_all_df(df):
    pm10_df = df.groupby(by="station").agg({
        "PM10":  "mean"
    }).sort_values(by="PM10", ascending=False).reset_index()
    pm10_df.rename(columns={
        "PM10": "pm10"
    }, inplace=True)
    return pm10_df


# Load clean data
all_df = pd.read_csv(
    'https://raw.githubusercontent.com/azyd-byte/air_quality_dataset2/main/dashboard/main_data.csv')

all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)
all_df["date"] = pd.to_datetime(all_df["date"])

# Filter data
max_date = all_df["date"].max()
min_date = all_df["date"].min()

with st.sidebar:
    # menambahkan logo
    st.image('dashboard/dashboard.jpg')

    # mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["date"] >= str(start_date))
                 & (all_df["date"] <= str(end_date))]

# st.dataframe(main_df)
co_mean_df = create_co_mean_all_df(main_df)
pm10_df = create_pm10_all_df(main_df)


st.header("Analisis Kualitas Udara di China 🌍")
st.subheader("Kadar CO di Udara Rentang Waktu Tertentu")

col1, col2, col3 = st.columns(3)
with col1:
    max_co = co_mean_df['CO'].max()
    st.metric(label="CO max: ", value=str(max_co.round(1)))
with col2:
    mean_co = co_mean_df['CO'].mean()
    st.metric(label="CO mean: ", value=str(mean_co.round(1)))
with col3:
    min_co = co_mean_df['CO'].min()
    st.metric(label="CO min: ", value=str(min_co.round(1)))
fig, ax = plt.subplots(figsize=(35, 15))
ax.plot(
    co_mean_df["date"],
    co_mean_df["CO"],
    marker='o',
    linewidth=3,
    color='#365486'
)
ax.set_xlabel('Rentang Waktu (tahun-bulan)', fontsize=35, labelpad=30)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)
st.pyplot(fig)


# Polusi PM10
st.subheader("Tingkat Polusi PM10 di China")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

color1 = ["#BF3131", "#F4F27E", "#F4F27E", "#F4F27E", "#F4F27E"]
color2 = ["#A8DF8E", "#F4F27E", "#F4F27E", "#F4F27E", "#F4F27E"]

sns.barplot(data=pm10_df.head(5), x="pm10",
            y="station", palette=color1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Polutan PM10", fontsize=35, labelpad=30)
ax[0].set_title("Kota Berpolutan PM10 Terbanyak",
                loc="center", fontsize=50, pad=30)
ax[0].tick_params(axis="x", labelsize=35)
ax[0].tick_params(axis="y", labelsize=35)
sns.barplot(data=pm10_df.sort_values(by="pm10", ascending=True).head(
    5), x="pm10", y="station", palette=color2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Polutan PM10", fontsize=35, labelpad=30)
ax[1].set_title("Kota Berpolutan PM10 Paling Sedikit",
                loc="center", fontsize=50, pad=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis="x", labelsize=40)
ax[1].tick_params(axis="y", labelsize=40)
st.pyplot(fig)

st.caption('Copyright © Zayadi 2024')
