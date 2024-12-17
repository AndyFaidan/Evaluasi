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
    <h2 style="text-align: center;">📊Dashboard Sumber Daya Manusia</h2>
""", unsafe_allow_html=True)

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Tampilkan deskripsi survei dan grafik
tab1, tab2 = st.tabs(["👨‍🏫 Survey Kepuasan Dosen", "🎓 Survey Kepuasan Tenaga Pendidik"])

with tab1:

    # Load data
    data = load_data("C.4.Kepuasandosen-prep.csv")

    # Inisialisasi session_state untuk semua filter jika belum ada
    if 'selected_tahun' not in st.session_state:
        st.session_state['selected_tahun'] = 'All'
    if 'selected_dosen' not in st.session_state:
        st.session_state['selected_dosen'] = 'All'
    if 'selected_matakuliah' not in st.session_state:
        st.session_state['selected_matakuliah'] = 'All'

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
    dosen_list = ['All'] + sorted(filtered_data['Nama Dosen'].unique())
    selected_dosen = st.selectbox(
        'Pilih Nama Dosen',
        options=dosen_list,
        index=dosen_list.index(st.session_state['selected_dosen']) if st.session_state['selected_dosen'] in dosen_list else 0
    )
    st.session_state['selected_dosen'] = selected_dosen

    # Filter data berdasarkan Nama Dosen
    filtered_data = filtered_data if selected_dosen == 'All' else filtered_data[filtered_data['Nama Dosen'] == selected_dosen]

    # FILTER 3: Mata Kuliah
    matakuliah_list = ['All'] + sorted(filtered_data['Matakuliah'].unique())
    selected_matakuliah = st.selectbox(
        'Pilih Mata Kuliah',
        options=matakuliah_list,
        index=matakuliah_list.index(st.session_state['selected_matakuliah']) if st.session_state['selected_matakuliah'] in matakuliah_list else 0
    )
    st.session_state['selected_matakuliah'] = selected_matakuliah

    # Filter data berdasarkan Mata Kuliah
    filtered_data = filtered_data if selected_matakuliah == 'All' else filtered_data[filtered_data['Matakuliah'] == selected_matakuliah]

    # Validasi data kosong
    if filtered_data.empty:
        st.warning("Tidak ada data yang sesuai dengan filter.")
    else:
        # Menampilkan metrik untuk setiap kompetensi dalam 4 kolom
        kompetensi_list = ['Pedagogik', 'Profesional', 'Kepribadian', 'Sosial']

        # Membuat layout dengan 4 kolom
        cols = st.columns(4)

        for idx, kompetensi in enumerate(kompetensi_list):
            kompetensi_data = filtered_data[filtered_data['Kompetensi'] == kompetensi]
            avg_value = kompetensi_data['Rata-rata per Kompetensi'].mean()

            with cols[idx]:
                # Menampilkan metrik dengan styling tambahan menggunakan HTML dan CSS
                st.markdown("""
                <style>
                    .metric-container {
                        display: flex;
                        flex-direction: column;  /* Mengubah arah flex menjadi kolom */
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                        background-color: #f5bf4a;
                        border-radius: 10px;
                        border: 2px solid #ddd;
                        margin-bottom: 10px;
                    }
                    .metric-label {
                        font-size: 1rem;
                        color: black;
                        margin-bottom: 10px;  /* Memberikan jarak antara label dan nilai */
                    }
                    .metric-text {
                        font-size: 2rem;
                        color: black;
                    }
                </style>
                """, unsafe_allow_html=True)

                # Tampilan menggunakan flexbox dengan arah kolom untuk menampilkan label di atas nilai
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Rata-rata Nilai {kompetensi}</div>
                    <div class="metric-text">{avg_value:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Tampilkan tabel dengan kolom Progress (Rata-rata per Kompetensi)
            st.data_editor(
                filtered_data[['Tahun Akademik', 'Nama Dosen', 'Matakuliah', 'Kompetensi', 'Rata-rata per Kompetensi', 'Kategori per Kompetensi']],
                column_config={
                    "Rata-rata per Kompetensi": st.column_config.ProgressColumn(
                        "Rata-rata per Kompetensi",
                        help="Menampilkan nilai rata-rata kompetensi",
                        min_value=0,
                        max_value=5,  # Sesuaikan dengan rentang nilai kompetensi
                        format="%.2f",  # Format nilai
                    ),
                },
                hide_index=True,
            )

        with col2:
            
            barchart = px.bar(
                filtered_data,
                x='Rata-rata per Kompetensi',
                y='Tahun Akademik',
                color='Kompetensi',
                barmode='group',
                title='Rata-rata Nilai Kompetensi per Tahun Akademik',
                labels={
                    'Rata-rata per Kompetensi': 'Rata-rata Nilai',
                    'Tahun Akademik': 'Tahun Akademik',
                    'Kompetensi': 'Kompetensi'
                },
                height=480
            )
            st.plotly_chart(barchart)


