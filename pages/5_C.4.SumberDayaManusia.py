import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Sumber Daya Manusia",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Judul aplikasi
st.title("Sumber Daya Manusia")

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

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
    # Menampilkan metrik untuk setiap kompetensi
    kompetensi_list = ['Pedagogik', 'Profesional', 'Kepribadian', 'Sosial']

    for kompetensi in kompetensi_list:
        kompetensi_data = filtered_data[filtered_data['Kompetensi'] == kompetensi]
        avg_value = kompetensi_data['Rata-rata per Kompetensi'].mean()

        # Menampilkan metrik untuk kompetensi tertentu
        st.radial(
            label=f"Rata-rata Nilai {kompetensi}",
            value=f"{avg_value:.2f}",
            delta=None,  # Nilai perubahan, kosongkan jika tidak perlu
            help=f"Rata-rata nilai untuk kompetensi {kompetensi}"
        )

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

    # Plot grafik barchart dengan plotly.express
    st.subheader('Rata-rata Nilai Kompetensi per Tahun Akademik')
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
        height=600
    )
    st.plotly_chart(barchart)

    # Menambahkan hole untuk membuatnya donut chart dan memilih warna
    piechart = px.pie(
        filtered_data,
        names='Kompetensi',                # Kolom Kompetensi
        values='Rata-rata per Kompetensi', # Kolom Rata-rata per Kompetensi
        title='Persentase Rata-rata Nilai per Kompetensi',
        labels={'Rata-rata per Kompetensi': 'Rata-rata Nilai'},
        hole=0.3,                          # Membuat hole (donut chart)
        color_discrete_sequence=px.colors.sequential.turbid
    )

    # Menampilkan pie chart
    st.plotly_chart(piechart)

