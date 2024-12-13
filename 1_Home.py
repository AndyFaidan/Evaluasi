import streamlit as st
import pandas as pd
from streamlit_apexjs import st_apexcharts
import altair as alt
import plotly.express as px


# Set page configuration
st.set_page_config(
    page_title="Beranda",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Fungsi pembantu untuk memuat data survei
@st.cache_data
# Load dataset function (if it's not defined elsewhere)
def load_data(file_path):
    return pd.read_csv(file_path)

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
                "size": "65%"
            }
        }
    },
    "labels": ["Mengerti", "Tidak Mengerti"],  # Menambahkan label untuk bagian-bagian
    "colors": ["#ADD8E6", "#00008B"]  # Biru muda untuk "Mengerti", Biru tua untuk "Tidak Mengerti"
}

a, b, c = st.columns(3)

a.metric("Temperature", "30°F", "-9°F", border=True)
b.metric("Wind", "4 mph", "2 mph", border=True)
c.metric("Humidity", "77%", "5%", border=True)

# Membuat layout kolom
col = st.columns((2, 7), gap='medium')

with col[0]:
    # Bar chart pertama (Donut Chart untuk rata-rata dari file pertama)
    series_1 = [rata_rata_pertanyaan_1.mean(), 5 - rata_rata_pertanyaan_1.mean()]  # Menghitung rata-rata total untuk file pertama
    st_apexcharts(options, series_1, 'donut', '100%', 'Visi dan Misi Teknik Informatika')

    # Bar chart kedua (Donut Chart untuk rata-rata dari file kedua)
    series_2 = [rata_rata_pertanyaan_2.mean(), 5 - rata_rata_pertanyaan_2.mean()]  # Menghitung rata-rata total untuk file kedua
    st_apexcharts(options, series_2, 'donut', '100%', 'Visi dan Misi STT Wastukancana')

with col[1]:
    
    # Load dataset
    data1 = load_data("C2.tatakeloladosendantendik-prep.csv")


    # Ekstraksi angka dari kolom yang relevan
    for col in data1.columns[1:-1]:  # Hindari kolom pertama (deskripsi) dan terakhir (status)
        data1[col] = data1[col].astype(str).str.extract(r'(\d+)').astype(float)

    # Remove question text from indicator names (before the question mark or text after it)
    cleaned_columns = data1.columns[1:-1].str.replace(r"\?.*", "", regex=True)

    # Assign cleaned column names back to the DataFrame
    data1.columns = ['Deskripsi'] + cleaned_columns.tolist() + ['Status Bpk/Ibu/Saudara/i.']

    # Creating a mapping of letters (a, b, c, etc.) to each indicator
    indicator_mapping = {col: chr(97 + idx) for idx, col in enumerate(data1.columns[1:-1])}

    # Map the indicator names to letters (a, b, c, etc.)
    mapped_indicators = data1.columns[1:-1].map(indicator_mapping)

    # Hitung rata-rata skor untuk setiap kolom di seluruh data
    avg_scores_all = data1.iloc[:, 1:-1].mean()

    # Convert the average scores to a DataFrame for easier plotting
    avg_scores_all_df = pd.DataFrame({
        'Indikator': mapped_indicators,
        'Rata-Rata Skor': avg_scores_all.values,
        'Full Question': data1.columns[1:-1]
    })

    # Create Altair bar chart with tooltips
    chart = alt.Chart(avg_scores_all_df).mark_bar().encode(
        x=alt.X('Indikator:N', title='Indikator'),  # Nominal scale for the indicators
        y=alt.Y('Rata-Rata Skor:Q', title='Rata-Rata Skor'),  # Quantitative scale for the average scores
        color=alt.Color('Indikator:N', scale=alt.Scale(scheme='category20')),  # Use 'category20' for colors
        tooltip=['Rata-Rata Skor:Q', 'Full Question:N']  # Only show the score and full question in tooltip
    ).properties(
        title="Tata Kelola Dosen & Tenaga Pendidik",
        width=400,
        height=300
    ).configure_title(
        anchor='middle'  # This centers the title
    )

    # Show the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

    data2 = load_data("C2.tatakelolamhs-preprossesing.csv")

    # Ekstraksi angka dari kolom yang relevan (skor)
    # Menghapus kolom pertama (Deskripsi) dan memproses skor dari kolom kedua dan seterusnya
    for col in data2.columns[1:]:  # Mulai dari kolom kedua yang berisi skor
        data2[col] = data2[col].apply(lambda x: pd.to_numeric(x, errors='coerce'))

    # Hitung rata-rata skor untuk setiap kolom (pertanyaan)
    avg_scores2 = data2.iloc[:, 1:].mean()

    # Membuat DataFrame dengan rata-rata skor dan nama indikator
    avg_scores2_df = pd.DataFrame({
        'Indikator': data2.columns[1:],  # Nama kolom sebagai indikator
        'Rata-Rata Skor': avg_scores2.values
    })

    #Membuat peta (mapping) untuk mengganti nama indikator dengan a, b, c, d, ...
    indicator_mapping = {col: chr(97 + idx) for idx, col in enumerate(data2.columns[1:])}

    # Ganti nama indikator dengan huruf (a, b, c, d, ...)
    avg_scores2_df['Indikator'] = avg_scores2_df['Indikator'].map(indicator_mapping)

    # Membuat Plotly Express Line Chart interaktif
    fig = px.line(avg_scores2_df, x='Indikator', y='Rata-Rata Skor',
                labels={'Rata-Rata Skor': 'Rata-Rata Skor', 'Indikator': 'Indikator'},
                markers=True)

    # Menyesuaikan layout untuk memusatkan title
    fig.update_layout(
        title="Tata Kelola Mahasiswa",
        title_x=0.5,  # Memusatkan title
        title_y=1,    # Posisi title di atas grafik
        title_xanchor='center',  # Memastikan title di pusat secara horizontal
    )

    # Menampilkan chart di Streamlit
    st.plotly_chart(fig, use_container_width=True)
