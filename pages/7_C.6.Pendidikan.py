import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Set page configuration
st.set_page_config(
    page_title="Visi dan Misi",
    layout="wide",
    initial_sidebar_state="collapsed",
)

file_url = 'https://drive.google.com/uc?id=1e2DIdPTY2TE7LcHP0FC-E868FjGy0kZ5'
file_path = 'k__jawaban.csv'

try:
    gdown.download(file_url, file_path, quiet=False)
    df = pd.read_csv(file_path)
    print("File berhasil diunduh dan dibaca!")
except Exception as e:
    print(f"Gagal mengunduh file: {e}")

# Membaca data dari file CSV
df = pd.read_csv(file_path)

# Pastikan kolom 'Tahun Akademik' bertipe numerik
df['Tahun Akademik'] = pd.to_numeric(df['Tahun Akademik'], errors='coerce')

# Menghapus baris dengan nilai 'Tahun Akademik' yang tidak valid (NaN)
df = df.dropna(subset=['Tahun Akademik'])

# Judul aplikasi
st.title("Analisis Kepuasan Mahasiswa terhadap Dosen")

# Bagian menu di body utama
st.header("Filter Data")

# Membuat range slider untuk filter Tahun Akademik
min_tahun = int(df['Tahun Akademik'].min())
max_tahun = int(df['Tahun Akademik'].max())
tahun_akademik_range = st.slider(
    "Pilih Rentang Tahun Akademik",
    min_value=min_tahun,
    max_value=max_tahun,
    value=(min_tahun, max_tahun)
)

# Filter untuk memilih Dosen Pengampuh
dosen_options = ['All'] + list(df['Dosen Pengampuh'].unique())
dosen_selected = st.selectbox("Pilih Dosen Pengampuh", options=dosen_options)

# Filter untuk memilih Pertanyaan
pertanyaan_options = ['All'] + list(df['Pertanyaan'].unique())
pertanyaan_selected = st.selectbox("Pilih Pertanyaan", options=pertanyaan_options)

# Menyaring data berdasarkan pilihan filter
df_filtered = df[
    (df['Tahun Akademik'].between(tahun_akademik_range[0], tahun_akademik_range[1]))
]

if dosen_selected != 'All':
    df_filtered = df_filtered[df_filtered['Dosen Pengampuh'] == dosen_selected]

if pertanyaan_selected != 'All':
    df_filtered = df_filtered[df_filtered['Pertanyaan'] == pertanyaan_selected]

# Menampilkan data yang sudah difilter
if df_filtered.empty:
    st.warning("Tidak ada data yang ditemukan dengan filter yang dipilih.")
else:
    st.subheader(f"Data yang Dimasukkan untuk Dosen: {dosen_selected}, Pertanyaan: {pertanyaan_selected}, Rentang Tahun Akademik: {tahun_akademik_range}")
    st.dataframe(df_filtered)

    # Menghitung rata-rata jawaban untuk setiap dosen dan tahun akademik yang difilter
    kepuasan_dosen = df_filtered.groupby(["Tahun Akademik", "Dosen Pengampuh"])['Jawaban'].mean().reset_index()

    # Membuat visualisasi Line Chart menggunakan Plotly
    fig_line = px.line(
        kepuasan_dosen,
        x="Tahun Akademik",
        y="Jawaban",
        color="Dosen Pengampuh",
        title="Rata-rata Kepuasan Mahasiswa Terhadap Dosen per Tahun Akademik",
        labels={"Jawaban": "Rata-rata Kepuasan", "Tahun Akademik": "Tahun Akademik", "Dosen Pengampuh": "Dosen"}
    )

    # Menampilkan grafik Line Chart
    st.plotly_chart(fig_line)

    # Menghitung distribusi jawaban untuk Donut Chart
    distribusi_jawaban = df_filtered['Jawaban'].value_counts(normalize=True).reset_index()
    distribusi_jawaban.columns = ['Jawaban', 'Persentase']

    # Membuat visualisasi Donut Chart menggunakan Plotly
    fig_donut = px.pie(
        distribusi_jawaban,
        values='Persentase',
        names='Jawaban',
        title="Distribusi Kepuasan Mahasiswa",
        hole=0.4,
        labels={"Jawaban": "Skor Kepuasan", "Persentase": "Persentase"}
    )

    # Menampilkan grafik Donut Chart
    st.plotly_chart(fig_donut)
