import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Visi dan Misi",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Judul aplikasi
st.title("Dashboard Survei Layanan Mahasiswa")

# Muat data dari CSV
data = pd.read_csv("C3. layanan mahasiswa-prep.csv")

# Tampilkan deskripsi survey
st.write("Deskripsi Survey Layanan Mahasiswa:")
st.write(data.describe())

# Buat grafik bar untuk menampilkan rata-rata nilai dari setiap pertanyaan
fig = px.bar(data.mean(), title="Rata-Rata Nilai Layanan Mahasiswa")
st.plotly_chart(fig, use_container_width=True)

# Buat grafik histogram untuk menampilkan distribusi nilai
fig_hist = px.histogram(data, title="Distribusi Nilai Layanan Mahasiswa")
st.plotly_chart(fig_hist, use_container_width=True)

# Buat grafik boxplot untuk menampilkan nilai-nilai ekstrem
fig_box = px.box(data, title="Nilai-Nilai Ekstrem Layanan Mahasiswa")
st.plotly_chart(fig_box, use_container_width=True)

# Buat grafik scatterplot untuk menampilkan hubungan antara pertanyaan
fig_scatter = px.scatter(data, x="Dosen menyediakan waktu bagi mahasiswa yang ingin berkonsultasi", y="Dosen membantu mahasiswa yang mengalami kesulitan dalam perkuliahan", title="Hubungan Antara Pertanyaan")
st.plotly_chart(fig_scatter, use_container_width=True)
