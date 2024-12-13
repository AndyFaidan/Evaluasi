import streamlit as st
import pandas as pd
from streamlit_apexjs import st_apexcharts

# Set page configuration
st.set_page_config(
    page_title="Beranda",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Fungsi pembantu untuk memuat data survei
@st.cache_data
def load_survey_data(file_path):
    survey_data = pd.read_csv(file_path)  # Mengambil data dari file CSV
    # Mengonversi timestamp ke format datetime dengan infer_format=True
    survey_data['Timestamp'] = pd.to_datetime(survey_data['Timestamp'], errors='coerce', infer_datetime_format=True)
    return survey_data

# Memuat data survei untuk dua file yang berbeda
survey_df_1 = load_survey_data("C.1.HasilSurveyPemahamanVMTSPS2024.csv")  # File pertama
survey_df_2 = load_survey_data("C.1.HasilSurveyPemahamanVMTSUPPS2024.csv")  # File kedua

# Fungsi untuk mengonversi kolom menjadi numerik dan menangani nilai yang hilang
def convert_to_numeric(df, columns):
    for col in columns:
        # Mengonversi menjadi numerik dan meng-coerce nilai yang tidak valid menjadi NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')  
    return df

# Mengonversi kolom pertanyaan 5 hingga 9 menjadi numerik pada kedua file
survey_df_1 = convert_to_numeric(survey_df_1, survey_df_1.columns[5:10])
survey_df_2 = convert_to_numeric(survey_df_2, survey_df_2.columns[5:10])

# Menghitung rata-rata untuk masing-masing dataset pada pertanyaan 5 hingga 9 untuk kedua file
rata_rata_pertanyaan_1 = survey_df_1.iloc[:, 5:10].mean()
rata_rata_pertanyaan_2 = survey_df_2.iloc[:, 5:10].mean()

# Menyiapkan opsi donut chart dan seri untuk rata-rata penilaian
options = {
    "chart": {
        "id": "donut_chart",
        "toolbar": {
            "show": False
        }
    },
    "legend": {
        "show": True,
        "position": "bottom",
    },
    "plotOptions": {
        "pie": {
            "donut": {
                "size": "70%"
            }
        }
    },
    "labels": ["Mengerti", "Tidak Mengerti"],  # Menambahkan label untuk bagian-bagian
    "colors": ["#ADD8E6", "#00008B"]  # Biru muda untuk "Mengerti", Biru tua untuk "Tidak Mengerti"
}

# Membuat donut chart berdasarkan rata-rata penilaian untuk File 1
series_1 = [rata_rata_pertanyaan_1.mean(), 5 - rata_rata_pertanyaan_1.mean()]  # Menghitung rata-rata total untuk file pertama
st_apexcharts(options, series_1, 'donut', '100%', 'Rata-Rata Pemahaman Visi dan Misi Program Studi Teknik Informatika')

# Membuat donut chart berdasarkan rata-rata penilaian untuk File 2
series_2 = [rata_rata_pertanyaan_2.mean(), 5 - rata_rata_pertanyaan_2.mean()]  # Menghitung rata-rata total untuk file kedua
st_apexcharts(options, series_2, 'donut', '100%', 'Rata-Rata Pemahaman Visi dan Misi STT Wastukancana')
