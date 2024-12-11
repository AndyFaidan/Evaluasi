import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Dashboard Pengabdian pada Masyarakat",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Judul aplikasi
st.title("Dashboard Survei Pengabdian pada Masyarakat STT Wastukancana")

# Load the data
@st.cache
def load_data():
    # Replace 'pengabdian-prep.csv' with the actual path to your CSV file
    data = pd.read_csv('pengabdian-prep.csv', header=None)
    return data

# Load data
data_pengabdian = load_data()

# Assign column names
data_pengabdian.columns = [
    "Distribusi informasi oleh Pusat PPM tentang jenis hibah untuk pengabdian pada masyarakat telah terakses oleh civitas akademika.",
    "Prosedur kegiatan pengabdian pada masyarakat internal sesuai dengan SOP yang telah ditetapkan.",
    "Prosedur kegiatan hibah pengabdian pada masyarakat eksternal sesuai dengan SOP yang telah ditetapkan."
]

# Tampilkan deskripsi survey dan grafik
st.subheader("Survey Pengabdian pada Masyarakat")
st.write("""
Survey ini bertujuan untuk mengetahui sejauh mana civitas akademika memahami prosedur dan distribusi informasi mengenai pengabdian pada masyarakat di STT Wastukancana.
""")

# Show the data in the app
st.write("Data Pengabdian:")
st.dataframe(data_pengabdian)

# Visualisasi Distribusi Skala
st.subheader("Distribusi Skala Pengabdian pada Masyarakat")

# Display histograms for each question
for col in data_pengabdian.columns:
    st.write(f"**Distribusi {col}:**")
    fig = px.histogram(data_pengabdian, x=col, nbins=5, labels={col: "Skala"}, title=f"Distribusi {col}")
    st.plotly_chart(fig, use_container_width=True)

