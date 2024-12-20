import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Survey Kepuasan Dosen Terhadap Pengelolaan Kegiatan PKM",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Menampilkan judul aplikasi di tengah
st.markdown("""
    <h2 style="text-align: center;">📊Survey Kepuasan Dosen Terhadap Pengelolaan Kegiatan PKM</h2>
""", unsafe_allow_html=True)

st.divider()
# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Fungsi untuk membersihkan data
def clean_data(data, start_col=1):
    for col in data.columns[start_col:]:
        data[col] = data[col].astype(str).str.extract(r'(\d+)').astype(float)
    return data

# Menambahkan kolom kategori berdasarkan nilai skor
def determine_category(score):
    if score < 1.0:
        return "Sangat Kurang"
    elif score < 2.0:
        return "Kurang"
    elif score < 3.0:
        return "Netral"
    elif score < 4.0:
        return "Baik"
    else:
        return "Sangat Baik"


# Load data
data1 = load_data("pengabdian-prep.csv")

# Calculate average scores for each question
avg_scores = data1.mean()

# Prepare the indicator names (letters for X-axis)
questions = data1.columns.tolist()  # Assuming questions are column names
letters = [chr(i) for i in range(97, 97 + len(avg_scores))]  # ['a', 'b', 'c', ...]



# Create a DataFrame with letters as 'Indikator', average scores, and questions
avg_scores_df = pd.DataFrame({
    'Indikator': letters,
    'Pertanyaan': questions,
    'Rata-Rata Skor': avg_scores.values
})

# Terapkan fungsi kategori ke setiap nilai skor rata-rata
avg_scores_df['Kategori'] = avg_scores_df['Rata-Rata Skor'].apply(determine_category)


# Calculate metrics for 'Rata-Rata Skor' column in avg_scores_df
min_score = avg_scores_df['Rata-Rata Skor'].min()
max_score = avg_scores_df['Rata-Rata Skor'].max()
mean_score = avg_scores_df['Rata-Rata Skor'].mean()

# Calculate percentage for each metric based on the maximum possible score (5)
min_percentage = (min_score / 5) * 100
max_percentage = (max_score / 5) * 100
mean_percentage = (mean_score / 5) * 100

# Kolom untuk nilai Min, Mean, dan Max
col1, col2, col3 = st.columns(3)

with col1:
        
        st.markdown(f"""
            <div style="border: px solid; padding: 10px; border-radius: 15px; text-align: center;
                        background: linear-gradient(to right, #9b59b6, #f06292); 
                        border-image: linear-gradient(to right, #9b59b6, #f06292) 1;">
                <p style="font-size: 15px; margin: 0; color: black;">Rata-Rata Skor</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold; color: black;">{mean_score:.2f}</p>
                <p style="font-size: 16px; ">{mean_percentage:.2f}%</p>
                <!-- Progress Bar with White and Gray Colors -->
                <div style="height: 10px; background-color: #d3d3d3; border-radius: 10px;">
                    <div style="width: {mean_percentage}%; height: 100%; background-color: white; 
                            border-radius: 10px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with col2:
        # Display Min Score with Progress Bar
        color = 'green' if min_percentage > 60 else 'red'
        st.markdown(f"""
            <div style="border: px solid; padding: 10px; border-radius: 15px; text-align: center;
                        background: linear-gradient(to right, #ff5733, #ff8c00);
                        border-image: linear-gradient(to right, #ff5733, #ff8c00) 1;">
                <p style="font-size: 15px; margin: 0; color: black;">Minimal Skor</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold; color: black;">{min_score:.2f}</p>
                <p style="font-size: 16px;">{min_percentage:.2f}%</p>
                <!-- Progress Bar with White and Gray Colors -->
                <div style="height: 10px; background-color: #d3d3d3; border-radius: 10px;">
                    <div style="width: {min_percentage}%; height: 100%; background-color: white; 
                            border-radius: 10px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with col3:
        # Display Max Score with Progress Bar
        color = 'green' if max_percentage > 60 else 'red'
        st.markdown(f"""
            <div style="border: 0px solid; padding: 10px; border-radius: 15px; text-align: center;
                        background: linear-gradient(to right, #00b0ff, #04c778); 
                        border-image: linear-gradient(to right, #00b0ff, #04c778) 1;">
                <p style="font-size: 15px; margin: 0; color: black;">Maksimal Skor</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold; color: black;">{max_score:.2f}</p>
                <p style="font-size: 16px; color: ">{max_percentage:.2f}%</p>
                <!-- Progress Bar with White and Gray Colors -->
                <div style="height: 10px; background-color: #d3d3d3; border-radius: 10px;">
                    <div style="width: {max_percentage}%; height: 100%; background-color: white; 
                            border-radius: 10px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# Tambahkan opsi "All" di awal daftar pertanyaan
all_questions = ["All"] + questions

# Perbarui selectbox untuk menyertakan opsi "All"
selected_question_index = st.selectbox(
    "Pilih Pertanyaan",
    range(len(all_questions)),
    format_func=lambda x: all_questions[x]
)

# Jika "All" dipilih, hitung data gabungan, jika tidak, ambil pertanyaan spesifik
if selected_question_index == 0:  # "All" dipilih
    selected_question_avg_score = avg_scores_df['Rata-Rata Skor'].mean()
    fulfilled_percentage = (selected_question_avg_score / 5) * 100
    not_fulfilled_percentage = 100 - fulfilled_percentage
else:
    selected_question_avg_score = avg_scores_df['Rata-Rata Skor'].iloc[selected_question_index - 1]
    fulfilled_percentage = (selected_question_avg_score / 5) * 100
    not_fulfilled_percentage = 100 - fulfilled_percentage

# Persiapkan data untuk donut chart
fulfillment_data = pd.DataFrame({
    'Status': ['Terpenuhi', 'Tidak Terpenuhi'],
    'Persentase': [fulfilled_percentage, not_fulfilled_percentage]
})


col1, col2, col3 = st.columns(3)


with col1:
    with st.container(border=True):
        # Create the donut chart
        fig_donut = px.pie(
            fulfillment_data,
            values='Persentase',
            names='Status',
            hole=0.4,
            title=f"Persentase Terpenuhi dan Tidak Terpenuhi untuk Pertanyaan",
            color_discrete_sequence=px.colors.sequential.Purpor
        )
        # Update layout to center the title and position the legend at the bottom
        fig_donut.update_layout(
            legend_title="Indikator",  # Title for the legend
            legend_orientation="h",  # Horizontal legend
            legend_yanchor="middle",  # Aligns legend at the bottom
        )
        # Display the donut chart
        st.plotly_chart(fig_donut, use_container_width=True)
    

with col2:
    with st.container(border=True):
        # Plot a bar chart for average scores
        fig_bar = px.bar(
            avg_scores_df,
            x='Indikator',
            y='Rata-Rata Skor',
            labels={'Indikator': 'Indikator', 'Rata-Rata Skor': 'Rata-Rata Skor'},
            title="Rata-Rata Skor untuk Setiap Indikator",
            color='Rata-Rata Skor',
            color_continuous_scale='Purpor',
            height=450,
            hover_data=["Rata-Rata Skor"]  # Include only non-conflicting fields
        )
        # Update layout untuk menyesuaikan tampilan
        fig_donut.update_layout(
            title_x=0.2,  # Centers the title
            )

        # Display the bar chart
        st.plotly_chart(fig_bar, use_container_width=True)

with col3:
    with st.container(border=True):
        # Filter data tanpa netral (skor == 3 dianggap netral)
        non_neutral_data = data1[data1.apply(lambda row: ~row.isin([3]), axis=1)]

        # Hitung jumlah kategori
        categories_count = {
            "Sangat Kurang": (non_neutral_data == 1).sum().sum(),
            "Kurang": (non_neutral_data == 2).sum().sum(),
            "Baik": (non_neutral_data == 4).sum().sum(),
            "Sangat Baik": (non_neutral_data == 5).sum().sum(),
        }

        # Hitung total jawaban yang relevan
        total_non_neutral = sum(categories_count.values())

        # Hitung persentase untuk setiap kategori
        fulfillment_data = pd.DataFrame({
            'Kategori': categories_count.keys(),
            'Jumlah': categories_count.values(),
            'Persentase': [count / total_non_neutral * 100 for count in categories_count.values()]
        })

        # Buat diagram pie dengan persentase
        fig_donut = px.pie(
            fulfillment_data,
            values='Persentase',
            names='Kategori',
            hole=0.4,
            title="Distribusi Kategori Jawaban (Tanpa Netral)",
            color_discrete_sequence=px.colors.sequential.Purpor
        )

        # Update layout untuk menyesuaikan tampilan
        fig_donut.update_layout(
            title_x=0.2,  # Centers the title
            legend_title="Kategori",  # Title for the legend
            legend_orientation="h",  # Horizontal legend
            legend_yanchor="bottom",  # Aligns legend at the bottom
            legend_y=-0.2,  # Moves the legend below the chart
            legend_x=0.5,  # Centers the legend horizontally
            legend_xanchor="center"  # Ensures that the legend is anchored in the center
        )

        # Tampilkan diagram pie
        st.plotly_chart(fig_donut, use_container_width=True)


# Tampilkan data editor dengan kolom kategori
st.data_editor(
    avg_scores_df,
    column_config={
        "Rata-Rata Skor": st.column_config.ProgressColumn(
            "Rata-rata Skor",
            help="Menampilkan nilai rata-rata jawaban",
            min_value=0,
            max_value=5,  # Asumsikan skala 1-5
            format="%.2f",  # Format nilai dengan dua desimal
        ),
        "Kategori": st.column_config.TextColumn(
            "Kategori",
            help="Kategori berdasarkan skor"
        )
    },
    hide_index=True,  # Menyembunyikan indeks
    use_container_width=True  # Menggunakan lebar penuh tabel
)

