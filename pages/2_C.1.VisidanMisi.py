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
st.title("📊 Dashboard Survei Visi dan Misi STT Wastukancana & Teknik Informatika")

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Fungsi untuk membersihkan data
def clean_data(data, start_col=1):
    for col in data.columns[start_col:]:
        data[col] = data[col].astype(str).str.extract(r'(\d+)').astype(float)
    return data

# Tampilkan deskripsi survei dan grafik
tab1, tab2 = st.tabs(["👨‍🏫 Survey Pemahaman Visi & Misi STT Wastukancana", "🎓 Survey Pemahaman Visi & Misi Teknik Informatika"])

with tab1:
    # Load data
    data1 = load_data("C.1.SurveyPemahamanVisiMisiSTTWastukancana.csv")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pilih Status
        status_filter = st.selectbox("🔍 Pilih Status:", ["All"] + list(data1['1. Status Bpk/Ibu/Saudara/i:'].unique()))

        # Filter data berdasarkan status
        if status_filter == "All":
            filtered_data1 = data1
        else:
            filtered_data1 = data1[data1['1. Status Bpk/Ibu/Saudara/i:'] == status_filter]

    with col2:
        # Pilih Pertanyaan (berdasarkan kolom-kolom pertanyaan yang ada di filtered data)
        pertanyaan_list = filtered_data1.columns[1:]  # Asumsi pertanyaan ada di kolom 1 hingga kolom terakhir sebelum kolom status
        pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", pertanyaan_list)

    # Filter data berdasarkan pertanyaan yang dipilih
    filtered_data2 = filtered_data1[['1. Status Bpk/Ibu/Saudara/i:', pertanyaan_filter]]

    # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
    avg_scores1 = filtered_data1.iloc[:, 1:].mean().reset_index()
    avg_scores1.columns = ['Indikator', 'Rata-Rata Skor']

    # Menyiapkan huruf untuk sumbu X (a, b, c, ...)
    letters = [chr(i) for i in range(97, 97 + len(avg_scores1))]  # Menghasilkan list ['a', 'b', 'c', ...]
    avg_scores1['Indikator'] = letters  # Menggunakan huruf untuk sumbu X

     # Visualisasi Bar Chart untuk Rata-Rata Skor
    fig_bar = px.bar(
        avg_scores1,
        x='Indikator',
        y='Rata-Rata Skor',
        labels={'Indikator': 'Indikator', 'Rata-Rata Skor': 'Rata-Rata Skor'},
        title=f"Rata-Rata Skor untuk Status: {status_filter}",
        color='Rata-Rata Skor',
        color_continuous_scale='Blues',
        height=700
    )
        # Mengatur posisi judul agar berada di tengah
    fig_bar.update_layout(
        title_x=0.3  # Menempatkan judul di tengah (0.5 artinya di tengah dari grafik)
    )

    # Tambahkan garis rata-rata sebagai referensi
    avg_line = avg_scores1['Rata-Rata Skor'].mean()
    fig_bar.add_hline(y=avg_line, line_dash="dash", line_color="red", 
                    annotation_text=f"Rata-rata {avg_line:.2f}", annotation_position="top left")

    

    # Membuat layout kolom
    col = st.columns((2, 4 ,2), gap='medium')

    with col[1]:
        # Tampilkan Bar Chart
        st.plotly_chart(fig_bar, use_container_width=True, use_container_high=True)

with tab2:
     # Load data
    data1 = load_data("C.1.SurveyPemahamanVisiMisiTIF.csv")
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pilih Status
        status_filter = st.selectbox("🔍 Pilih Status:", ["All"] + list(data1['1. Status Bpk/Ibu/Saudara/i:'].unique()))

        # Filter data berdasarkan status
        if status_filter == "All":
            filtered_data1 = data1
        else:
            filtered_data1 = data1[data1['1. Status Bpk/Ibu/Saudara/i:'] == status_filter]

    with col2:
        # Pilih Pertanyaan (berdasarkan kolom-kolom pertanyaan yang ada di filtered data)
        pertanyaan_list = filtered_data1.columns[1:]  # Asumsi pertanyaan ada di kolom 1 hingga kolom terakhir sebelum kolom status
        pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", pertanyaan_list)

    # Filter data berdasarkan pertanyaan yang dipilih
    filtered_data2 = filtered_data1[['1. Status Bpk/Ibu/Saudara/i:', pertanyaan_filter]]

    # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
    avg_scores1 = filtered_data1.iloc[:, 1:].mean().reset_index()
    avg_scores1.columns = ['Indikator', 'Rata-Rata Skor']

    # Menyiapkan huruf untuk sumbu X (a, b, c, ...)
    letters = [chr(i) for i in range(97, 97 + len(avg_scores1))]  # Menghasilkan list ['a', 'b', 'c', ...]
    avg_scores1['Indikator'] = letters  # Menggunakan huruf untuk sumbu X

     # Visualisasi Bar Chart untuk Rata-Rata Skor
    fig_bar = px.bar(
        avg_scores1,
        x='Indikator',
        y='Rata-Rata Skor',
        labels={'Indikator': 'Indikator', 'Rata-Rata Skor': 'Rata-Rata Skor'},
        title=f"Rata-Rata Skor untuk Status: {status_filter}",
        color='Rata-Rata Skor',
        color_continuous_scale='Blues',
        height=700
    )
        # Mengatur posisi judul agar berada di tengah
    fig_bar.update_layout(
        title_x=0.3  # Menempatkan judul di tengah (0.5 artinya di tengah dari grafik)
    )

    # Tambahkan garis rata-rata sebagai referensi
    avg_line = avg_scores1['Rata-Rata Skor'].mean()
    fig_bar.add_hline(y=avg_line, line_dash="dash", line_color="red", 
                    annotation_text=f"Rata-rata {avg_line:.2f}", annotation_position="top left")

    

    # Membuat layout kolom
    col = st.columns((2, 4 ,2), gap='medium')

    with col[1]:
        # Tampilkan Bar Chart
        st.plotly_chart(fig_bar, use_container_width=True, use_container_high=True)
