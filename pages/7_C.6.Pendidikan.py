import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Sumber Daya Manusia",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Menampilkan judul aplikasi di tengah
st.markdown("""
    <h2 style="text-align: center;">📊Survey Evaluasi Kepuasan Mahasiswa Terhadap Proses Pembelajaran</h2>
""", unsafe_allow_html=True)

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Fungsi untuk menambahkan kolom kategori berdasarkan skor
def assign_category(score):
    if score < 1.0:
        return "Sangat Kurang"
    elif score < 2.0:
        return "Kurang"
    elif score < 3.0:
        return "Cukup"
    elif score < 4.0:
        return "Baik"
    else:
        return "Sangat Baik"

# Load data
data = load_data("C.6-kepuasan-pembelajaran-TS-prep.csv")

# Inisialisasi session_state untuk semua filter jika belum ada
if 'selected_tahun' not in st.session_state:
    st.session_state['selected_tahun'] = 'All'
if 'selected_dosen' not in st.session_state:
    st.session_state['selected_dosen'] = 'All'
if 'selected_matakuliah' not in st.session_state:
    st.session_state['selected_matakuliah'] = 'All'
if 'selected_pertanyaan' not in st.session_state:
    st.session_state['selected_pertanyaan'] = 'All'

# FILTER 1: Tahun Akademik
tahun_akademik_list = ['All'] + sorted(data['Tahun Akademik'].unique())
selected_tahun = st.selectbox(
    'Pilih Tahun Akademik',
    options=tahun_akademik_list,
    index=tahun_akademik_list.index(st.session_state['selected_tahun']) if st.session_state['selected_tahun'] in tahun_akademik_list else 0
    )
st.session_state['selected_tahun'] = selected_tahun

# Filter data berdasarkan Tahun Akademik
filtered_data = data if selected_tahun == 'All' else data[data['Tahun Akademik'] == selected_tahun]

# FILTER 2: Nama Dosen
dosen_list = ['All'] + sorted(filtered_data['Dosen Pengampuh'].unique())
selected_dosen = st.selectbox(
    'Pilih Nama Dosen',
    options=dosen_list,
    index=dosen_list.index(st.session_state['selected_dosen']) if st.session_state['selected_dosen'] in dosen_list else 0
    )
st.session_state['selected_dosen'] = selected_dosen

# Filter data berdasarkan Nama Dosen
filtered_data = filtered_data if selected_dosen == 'All' else filtered_data[filtered_data['Dosen Pengampuh'] == selected_dosen]

# FILTER 3: Mata Kuliah
matakuliah_list = ['All'] + sorted(filtered_data['Mata Kuliah'].unique())
selected_matakuliah = st.selectbox(
    'Pilih Mata Kuliah',
    options=matakuliah_list,
    index=matakuliah_list.index(st.session_state['selected_matakuliah']) if st.session_state['selected_matakuliah'] in matakuliah_list else 0
    )
st.session_state['selected_matakuliah'] = selected_matakuliah

# Filter data berdasarkan Mata Kuliah
filtered_data = filtered_data if selected_matakuliah == 'All' else filtered_data[filtered_data['Mata Kuliah'] == selected_matakuliah]

# FILTER 4: Pertanyaan
pertanyaan_list = ['All'] + sorted(filtered_data['Pertanyaan'].unique())
selected_pertanyaan = st.selectbox(
    'Pilih Pertanyaan',
    options=pertanyaan_list,
    index=pertanyaan_list.index(st.session_state['selected_pertanyaan']) if st.session_state['selected_pertanyaan'] in pertanyaan_list else 0
    )
st.session_state['selected_pertanyaan'] = selected_pertanyaan

# Filter data berdasarkan Pertanyaan
filtered_data = filtered_data if selected_pertanyaan == 'All' else filtered_data[filtered_data['Pertanyaan'] == selected_pertanyaan]

# Validasi data kosong
if filtered_data.empty:
    st.warning("Tidak ada data yang sesuai dengan filter.")
else:
    # Menghitung rata-rata skor untuk setiap pertanyaan
    avg_scores = filtered_data.groupby('Pertanyaan')['Jawaban'].mean().reset_index()
    avg_scores.rename(columns={'Jawaban': 'Rata-rata Skor'}, inplace=True)

    # Menambahkan kolom kategori berdasarkan rata-rata skor
    avg_scores['Kategori'] = avg_scores['Rata-rata Skor'].apply(assign_category)

    
    # Menambahkan kolom inisial untuk pertanyaan
    avg_scores['Inisial Pertanyaan'] = [chr(97 + i) for i in range(len(avg_scores))]  # Menghasilkan a, b, c, ...

                        # Membuat barchart berdasarkan rata-rata skor dengan color continuous scale
    barchart = px.bar(
            avg_scores,
            x='Inisial Pertanyaan',
            y='Rata-rata Skor',
            color='Rata-rata Skor',  # Menggunakan rata-rata skor untuk color continuous scale
            title='Rata-rata Nilai Jawaban per Pertanyaan',
            color_continuous_scale='sunset',  # Skema warna kontinu
                labels={
                    'Rata-rata Skor': 'Rata-rata Skor',
                    'Inisial Pertanyaan': 'Pertanyaan'
                },
                height=480,
                orientation='v'  # Orientasi vertikal
            )

            # Menambahkan teks tooltip untuk menampilkan detail lengkap pertanyaan
    barchart.update_traces(
                hovertemplate="<b>Pertanyaan:</b> %{customdata[0]}<br>" +
                            "<b>Rata-rata Skor:</b> %{y:.2f}<br>",
                customdata=avg_scores[['Pertanyaan']].values  # Tooltip tetap menampilkan pertanyaan lengkap
            )

            # Menampilkan grafik
    st.plotly_chart(barchart)

    # Menampilkan tabel rata-rata skor dengan kategori
st.data_editor(
    avg_scores,
    column_config={
        "Rata-rata Skor": st.column_config.ProgressColumn(
                    "Rata-rata Skor",
                    help="Menampilkan nilai rata-rata jawaban",
                    min_value=0,
                    max_value=5,  # Asumsikan skala 1-5
                    format="%.2f",  # Format nilai
                    ),
                "Kategori": st.column_config.TextColumn(
                "Kategori",
                help="Kategori berdasarkan skor"
                )
                },
                hide_index=True,
                use_container_width=True
            )
