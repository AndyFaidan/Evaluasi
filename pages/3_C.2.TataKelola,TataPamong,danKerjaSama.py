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
st.title("Dashboard Survei Visi dan Misi STT Wastukancana")

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Tampilkan deskripsi survey dan grafik
tab1, tab2 = st.tabs(["SARANA DOSEN", "SARANA MAHASISWA"])

# Tab SARANA DOSEN
with tab1:
    # Load dataset
    data1 = load_data("C2.tatakeloladosendantendik-prep.csv")

    # Periksa struktur data
    st.write("Preview Data:", data1.head())

    # Ekstraksi angka dari kolom yang relevan
    for col in data1.columns[1:-1]:  # Hindari kolom pertama (deskripsi) dan terakhir (status)
        data1[col] = data1[col].astype(str).str.extract(r'(\d+)').astype(float)

    # Filter berdasarkan Status
    status_filter = st.selectbox("Pilih Status:", data1['Status Bpk/Ibu/Saudara/i.'].unique())
    filtered_data1 = data1[data1['Status Bpk/Ibu/Saudara/i.'] == status_filter]

    # Hitung rata-rata skor untuk setiap kolom
    avg_scores1 = filtered_data1.iloc[:, 1:-1].mean()

    # Visualisasi data
    fig1 = px.bar(
        avg_scores1,
        x=avg_scores1.index,
        y=avg_scores1.values,
        labels={'x': 'Indikator', 'y': 'Rata-Rata Skor'},
        title=f"Rata-Rata Skor untuk Status {status_filter}"
    )
    st.plotly_chart(fig1)

with tab2:
    # Membaca data untuk tab SARANA MAHASISWA dari file yang sesuai
    data2 = load_data("C2.tatakelolamhs-preprossesing.csv")

    # Periksa struktur data
    st.write("Preview Data:", data2.head())

    # Ekstraksi angka dari kolom yang relevan (semua kolom selain kolom pertama yang berisi pertanyaan)
    for col in data2.columns[1:]:  # Mulai dari kolom kedua yang berisi skor
        data2[col] = data2[col].astype(str).str.extract(r'(\d+)').astype(float)

    # Hitung rata-rata skor untuk setiap kolom (pertanyaan)
    avg_scores2 = data2.iloc[:, 1:].mean()  # Mengambil skor untuk setiap pertanyaan

    # Visualisasi data
    fig2 = px.bar(
        avg_scores2,
        x=avg_scores2.index,
        y=avg_scores2.values,
        labels={'x': 'Indikator', 'y': 'Rata-Rata Skor'},
        title="Rata-Rata Skor untuk Setiap Pertanyaan (SARANA MAHASISWA)"
    )
    st.plotly_chart(fig2)

