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
def load_survey_data():
    survey_data = pd.read_csv("C.1.HasilSurveyPemahamanVMTSPS2024.csv")
    # Mengonversi timestamp ke format datetime untuk pemrosesan yang lebih baik
    survey_data['Timestamp'] = pd.to_datetime(survey_data['Timestamp'])
    return survey_data

# Memuat data survei
survey_df = load_survey_data()

# Menghitung rata-rata respons untuk pertanyaan 5 hingga 9
# Kolom-kolom ini sesuai dengan penilaian dari survei
rata_rata_semua_pertanyaan = survey_df.iloc[:, 5:10].mean().mean()  # Menghitung rata-rata keseluruhan

# Menampilkan rata-rata keseluruhan
st.subheader("Rata-Rata Pemahaman Visi dan Misi")
st.write(f"Rata-rata pemahaman keseluruhan adalah: {rata_rata_semua_pertanyaan:.2f} dari 5")

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

# Membuat seri untuk donut chart (menampilkan rata-rata penilaian dan bagian yang tersisa)
series = [rata_rata_semua_pertanyaan, 5 - rata_rata_semua_pertanyaan]  # Mengasumsikan penilaian adalah dari 5

# Menyusun layout dengan dua kolom
col1, col2 = st.columns([1, 2])  # Kolom pertama lebih kecil untuk chart, kolom kedua untuk penjelasan

# Container untuk donut chart di kiri layar (kolom 1)
with col1:
    st_apexcharts(options, series, 'donut', '100%', 'Rata-Rata Pemahaman Visi dan Misi')

# Container untuk penjelasan di sebelah kanan (kolom 2)
with col2:
    st.subheader("Penjelasan:")
    st.write(
        "1. **Mengerti**: Bagian chart ini mewakili responden yang memahami visi dan misi Program Studi Teknik Informatika."
    )
    st.write(
        "2. **Tidak Mengerti**: Bagian ini mewakili responden yang tidak memahami visi dan misi."
    )
