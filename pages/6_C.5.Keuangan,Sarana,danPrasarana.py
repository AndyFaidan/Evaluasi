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

# Pilih file dataset
data_files = {
    "SARANA DOSEN": "C5.saranadosen-prep.csv",
    "SARANA MAHASISWA": "C5.saranamahasiswa-prep.csv",
    "SARANA TENDIK": "C5.saranatendik-prep.csv"
}

# Tampilkan deskripsi survey dan grafik
tab1, tab2, tab3 = st.tabs(["SARANA DOSEN", "SARANA MAHASISWA", "SARANA TENDIK"])

# Tab 1: SARANA DOSEN
with tab1:
    # Muat data dari CSV
    data_dosen = pd.read_csv(data_files["SARANA DOSEN"])
    
    # Tampilkan deskripsi survey
    st.write("Deskripsi Survey Sarana Dosen:")
    st.write(data_dosen.describe())
    
    # Buat grafik bar untuk menampilkan rata-rata nilai dari setiap pertanyaan
    fig_dosen = px.bar(data_dosen.mean(), title="Rata-Rata Nilai Sarana Dosen")
    st.plotly_chart(fig_dosen, use_container_width=True)
    
    # Buat grafik histogram untuk menampilkan distribusi nilai
    fig_dosen_hist = px.histogram(data_dosen, title="Distribusi Nilai Sarana Dosen")
    st.plotly_chart(fig_dosen_hist, use_container_width=True)
    
    # Buat grafik boxplot untuk menampilkan nilai-nilai ekstrem
    fig_dosen_box = px.box(data_dosen, title="Nilai-Nilai Ekstrem Sarana Dosen")
    st.plotly_chart(fig_dosen_box, use_container_width=True)

# Tab 2: SARANA MAHASISWA
with tab2:
    # Muat data dari CSV
    data_mahasiswa = pd.read_csv(data_files["SARANA MAHASISWA"])
    
    # Tampilkan deskripsi survey
    st.write("Deskripsi Survey Sarana Mahasiswa:")
    st.write(data_mahasiswa.describe())
    
    # Buat grafik bar untuk menampilkan rata-rata nilai dari setiap pertanyaan
    fig_mahasiswa = px.bar(data_mahasiswa.mean(), title="Rata-Rata Nilai Sarana Mahasiswa")
    st.plotly_chart(fig_mahasiswa, use_container_width=True)
    
    # Buat grafik histogram untuk menampilkan distribusi nilai
    fig_mahasiswa_hist = px.histogram(data_mahasiswa, title="Distribusi Nilai Sarana Mahasiswa")
    st.plotly_chart(fig_mahasiswa_hist, use_container_width=True)
    
    # Buat grafik boxplot untuk menampilkan nilai-nilai ekstrem
    fig_mahasiswa_box = px.box(data_mahasiswa, title="Nilai-Nilai Ekstrem Sarana Mahasiswa")
    st.plotly_chart(fig_mahasiswa_box, use_container_width=True)

# Tab 3: SARANA TENDIK
with tab3:
    # Muat data dari CSV
    data_tendik = pd.read_csv(data_files["SARANA TENDIK"])
    
    # Tampilkan deskripsi survey
    st.write("Deskripsi Survey Sarana Tendik:")
    st.write(data_tendik.describe())
    
    # Buat grafik bar untuk menampilkan rata-rata nilai dari setiap pertanyaan
    fig_tendik = px.bar(data_tendik.mean(), title="Rata-Rata Nilai Sarana Tendik")
    st.plotly_chart(fig_tendik, use_container_width=True)
    
    # Buat grafik histogram untuk menampilkan distribusi nilai
    fig_tendik_hist = px.histogram(data_tendik, title="Distribusi Nilai Sarana Tendik")
    st.plotly_chart(fig_tendik_hist, use_container_width=True)
    
    # Buat grafik boxplot untuk menampilkan nilai-nilai ekstrem
    fig_tendik_box = px.box(data_tendik, title="Nilai-Nilai Ekstrem Sarana Tendik")
    st.plotly_chart(fig_tendik_box, use_container_width=True)
