import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Dashboard Penelitian dan Pengabdian Masyarakat",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Judul aplikasi
st.title("Dashboard Survei Penelitian dan Pengabdian Masyarakat STT Wastukancana")

# Load the data
@st.cache
def load_data():
    # Replace 'penelitian-prep.csv' with the actual path to your CSV file
    data = pd.read_csv('penelitian-prep.csv', header=None)
    return data

# Load data
data_penelitian = load_data()

# Assign column names
data_penelitian.columns = [
    "Ketersediaan akses terhadap jurnal online",
    "Distribusi informasi oleh Pusat PPM (Penelitian dan Pengabdian Masyarakat) tentang jenis hibah untuk penelitian telah dapat terakses dengan baik oleh dosen.",
    "Prosedur penelitian internal sesuai dengan SOP.",
    "Penelitian hibah eksternal difasilitasi dengan baik oleh Pusat PPM.",
    "Institusi memfasilitasi pembiayaan publikasi artikel di jurnal nasional terakreditasi.",
    "Institusi memfasilitasi pembiayaan publikasi artikel di jurnal internasional.",
    "Institusi memfasilitasi pembiayaan call for paper di tingkat nasional.",
    "Institusi memfasilitasi pembiayaan call for paper di tingkat internasional.",
    "Institusi memfasilitasi pengurusan dan pembiayaan HAKI (hak cipta kekayaan intelektual)."
]

# Tampilkan deskripsi survey dan grafik
st.subheader("Survey Penelitian dan Pengabdian pada Masyarakat")
st.write("""
Survey ini bertujuan untuk mengetahui sejauh mana civitas akademika memahami berbagai aspek terkait penelitian dan pengabdian pada masyarakat di STT Wastukancana.
""")

# Show the data in the app
st.write("Data Penelitian:")
st.dataframe(data_penelitian)

# Visualisasi Distribusi Skala
st.subheader("Distribusi Skala Penelitian dan Pengabdian pada Masyarakat")

# Display histograms for each question
for col in data_penelitian.columns:
    st.write(f"**Distribusi {col}:**")
    fig = px.histogram(data_penelitian, x=col, nbins=5, labels={col: "Skala"}, title=f"Distribusi {col}")
    st.plotly_chart(fig, use_container_width=True)

