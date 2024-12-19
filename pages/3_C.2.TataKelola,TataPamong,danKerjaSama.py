import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Visi dan Misi",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Menampilkan judul aplikasi di tengah
st.markdown("""
    <h2 style="text-align: center;">📊 Dashboard Tata Kelola, Tata Pamong & Kerja Sama</h2>
""", unsafe_allow_html=True)

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Fungsi untuk membersihkan data
def clean_data(data, start_col=1):
    for col in data.columns[start_col:]:
        data[col] = data[col].astype(str).str.extract(r'(\d+)').astype(float)
    return data

# Fungsi untuk menambahkan kolom kategori berdasarkan skor
def assign_category(score):
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

# Tampilkan deskripsi survei dan grafik
tab1, tab2 = st.tabs(["👨‍🏫 TATA KELOLA DOSEN & TENAGA PENDIDIK", "🎓 TATA KELOLA MAHASISWA"])

with tab1:
    # Load data
    data1 = load_data("C2.tatakeloladosendantendik-prep.csv")

    col1, col2 = st.columns(2)
    with col1:
        # Pilih Status
        status_filter = st.selectbox("🔍 Pilih Status:", ["All"] + list(data1['Status Bpk/Ibu/Saudara/i.'].unique()))
        if status_filter == "All":
            filtered_data1 = data1
        else:
            filtered_data1 = data1[data1['Status Bpk/Ibu/Saudara/i.'] == status_filter]

    with col2:
        # Pilih Pertanyaan
        pertanyaan_list = filtered_data1.columns[1:-1]
        pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", ["All Pertanyaan"] + list(pertanyaan_list))

    # Hitung rata-rata skor
    avg_scores1 = filtered_data1.iloc[:, 1:-1].mean().reset_index()
    avg_scores1.columns = ['Pertanyaan', 'Rata-Rata Skor']
    avg_scores1['Indikator'] = [chr(97 + i) for i in range(len(avg_scores1))]

    # Terapkan fungsi kategori ke setiap nilai skor rata-rata
    avg_scores1['Kategori'] = avg_scores1['Rata-Rata Skor'].apply(assign_category)

    # Calculate metrics for 'Rata-Rata Skor' column in avg_scores_df
    min_score = avg_scores1['Rata-Rata Skor'].min()
    max_score = avg_scores1['Rata-Rata Skor'].max()
    mean_score = avg_scores1['Rata-Rata Skor'].mean()

    # Calculate percentage for each metric based on the maximum possible score (5)
    min_percentage = (min_score / 5) * 100
    max_percentage = (max_score / 5) * 100
    mean_percentage = (mean_score / 5) * 100

    # Kolom untuk nilai Min, Mean, dan Max
    col1, col2, col3 = st.columns(3)
    with col1:
        # Display Mean Score with Progress Bar
        color = 'green' if mean_percentage > 60 else 'red'
        st.markdown(f"""
            <div style="border: 1px solid ; padding: 10px; border-radius: 8px; text-align: center; background-color: #f5bf4a ">
                <p style="font-size: 15px; margin: 0;">Rata-Rata Skor</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold;">{mean_score:.2f}</p>
                <p style="font-size: 16px; color: {color};">{mean_percentage:.2f}%</p>
                <!-- Progress Bar -->
                <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px;">
                    <div style="width: {mean_percentage}%; height: 100%; background-color: {color}; border-radius: 5px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Display Min Score with Progress Bar
        color = 'green' if min_percentage > 60 else 'red'
        st.markdown(f"""
            <div style="border: 1px solid; padding: 10px; border-radius: 8px; text-align: center; background-color: #f5bf4a ">
                <p style="font-size: 15px; margin: 0;">Minimal Skor</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold;">{min_score:.2f}</p>
                <p style="font-size: 16px; color: {color};">{min_percentage:.2f}%</p>
                <!-- Progress Bar -->
                <div style="height: 10px; background-color: #e0e0e0; border-radius: 10px;">
                    <div style="width: {min_percentage}%; height: 100%; background-color: {color}; border-radius: 5px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        # Display Max Score with Progress Bar
        color = 'green' if max_percentage > 60 else 'red'
        st.markdown(f"""
            <div style="border: 1px solid; padding: 10px; border-radius: 8px; text-align: center; background-color: #f5bf4a ">
                <p style="font-size: 15px; margin: 0;">Maksimal Skor</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold;">{max_score:.2f}</p>
                <p style="font-size: 16px; color: {color};">{max_percentage:.2f}%</p>
                <!-- Progress Bar -->
                <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px;">
                    <div style="width: {max_percentage}%; height: 100%; background-color: {color}; border-radius: 5px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)


st.divider()
    

# Layout: Create three columns for the components
col1, col2, col3 = st.columns([2, 2, 4])

# Column 1: Donut chart and evaluation category
with col1:
    with st.container(border=True):
        # Calculate average score for all questions or specific question
        if pertanyaan_filter == "All Pertanyaan":
            avg_score = avg_scores1['Rata-Rata Skor'].mean()
        else:
            avg_score = filtered_data1[pertanyaan_filter].mean()

        # Calculate percentage and category
        percentage_score = (avg_score / 5) * 100 if avg_score > 0 else 0
        category = 'Terpenuhi' if percentage_score > 60 else 'Belum Terpenuhi'

        # Prepare data for donut chart
        donut_data = pd.DataFrame({
            "Kategori": [category, "Belum Terpenuhi" if category == "Terpenuhi" else "Terpenuhi"],
            "Persentase": [percentage_score, 100 - percentage_score]
        })

        # Create and style donut chart
        fig_donut = px.pie(
            donut_data,
            names='Kategori',
            values='Persentase',
            hole=0.5,
            color='Kategori',
            color_discrete_sequence=["#36A2EB", "#FFCE56"],
            title="Evaluasi Capaian"
        )
        fig_donut.update_layout(
            height=400,  # Reduce height,
            width=200,  # Reduce width
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5

            ),
            title_x=0.3
        )

        # Display the donut chart
        st.plotly_chart(fig_donut, use_container_width=True)

# Column 3: Pie chart showing distribution of non-neutral answers
with col2:
    with st.container(border=True):
        # Filter out "Netral" answers (score == 3)
        non_neutral_data = data1[data1.apply(lambda row: ~row.isin([3]), axis=1)]

        # Count the occurrences of each category
        categories_count = {
            "Sangat Kurang": (non_neutral_data == 1).sum().sum(),
            "Kurang": (non_neutral_data == 2).sum().sum(),
            "Baik": (non_neutral_data == 4).sum().sum(),
            "Sangat Baik": (non_neutral_data == 5).sum().sum(),
        }

        # Calculate the total number of relevant answers
        total_non_neutral = sum(categories_count.values())

        # Prepare data for the pie chart
        fulfillment_data = pd.DataFrame({
            'Kategori': categories_count.keys(),
            'Jumlah': categories_count.values(),
            'Persentase': [count / total_non_neutral * 100 for count in categories_count.values()]
        })

        # Create and style the pie chart
        fig_donut = px.pie(
            fulfillment_data,
            values='Persentase',
            names='Kategori',
            hole=0.5,
            title="Distribusi Kategori Jawaban",
            color_discrete_sequence=px.colors.sequential.Purp
        )
        
        # Update layout for the pie chart
        fig_donut.update_layout(
            title_x=0.2,
            legend_title="Kategori",
            legend_orientation="h",
            legend_yanchor="bottom",
            legend_y=-0.3,
            legend_x=0.5,
            legend_xanchor="center",
            height=400,  # Reduce height
            width=200   # Reduce width
        )

        # Display the pie chart
        st.plotly_chart(fig_donut, use_container_width=True)

# Column 2: Bar chart visualization for average scores
with col3:
    with st.container(border=True):
        # Create bar chart for average scores by indicator
        fig_bar = px.bar(
            avg_scores1,
            x='Indikator',
            y='Rata-Rata Skor',
            title="Distribusi Rata-Rata Skor Berdasarkan Indikator",
            color='Rata-Rata Skor',
            color_continuous_scale='Blues',
            hover_data={'Pertanyaan': True},
            height=400
        )
        fig_bar.update_layout(title_x=0.2)
        
        # Add a horizontal line for the average score
        fig_bar.add_hline(
            y=avg_scores1['Rata-Rata Skor'].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Rata-rata {avg_scores1['Rata-Rata Skor'].mean():.2f}",
            annotation_position="top left"
        )

        # Display the bar chart
        st.plotly_chart(fig_bar, use_container_width=True)

# Menampilkan tabel rata-rata skor dengan kategori
st.container(border=True)
st.data_editor(
            avg_scores1,
            column_config={
                "Rata-Rata Skor": st.column_config.ProgressColumn(
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

# Tab SARANA MAHASISWA
with tab2:
    # Load dataset dengan header di baris pertama dan kedua
    def load_data_with_multi_header(file_path):
        data = pd.read_csv(file_path, header=[0, 1], encoding="utf-8")  # Pastikan encoding UTF-8
        data.columns = ['_'.join(col).strip() for col in data.columns.values]
        return data

    # Load dan bersihkan data
    data2 = load_data_with_multi_header("C2.tatakelolamhs-preprossesing.csv")
    data2 = clean_data(data2)  # Jika ada fungsi clean_data, tetap digunakan

    # Hitung rata-rata skor untuk setiap pertanyaan
    avg_scores2 = data2.iloc[:, 1:].mean().reset_index()
    avg_scores2.columns = ['Pertanyaan', 'Rata-Rata Skor']

    # Menyiapkan huruf untuk sumbu X (a, b, c, ...)
    letters = [chr(i) for i in range(97, 97 + len(avg_scores2))]
    avg_scores2['Letter'] = letters

            # Calculate metrics
    min_score = avg_scores2['Rata-Rata Skor'].min()
    max_score = avg_scores2['Rata-Rata Skor'].max()
    mean_score = avg_scores2['Rata-Rata Skor'].mean()

        
        # Display metrics with individual borders
    st.markdown("""<style>
        .metric-box {
            text-align: center;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #f5bf4a ;
        }
        .metric-box h3 {
            margin: 0;
            font-size: 1.5rem;
            color: black;
        }
        .metric-box p {
            margin: 5px 0 0;
            font-size: 1rem;
            color: black ;
        }
        </style>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-box">
        <h3>{:.2f}</h3>
        <p>Minimum Skor</p>
        </div>""".format(min_score), unsafe_allow_html=True)
    with col2:       
        st.markdown("""<div class="metric-box">
        <h3>{:.2f}</h3>
        <p>Rata-Rata Skor</p>
        </div>""".format(mean_score), unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-box">
        <h3>{:.2f}</h3>
        <p>Maksimum Skor</p>
        </div>""".format(max_score), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Visualisasi Bar Chart
        fig_bar = px.bar(
            avg_scores2,
            x='Letter',
            y='Rata-Rata Skor',
            title="Rata-Rata Skor untuk Setiap Pertanyaan (SARANA MAHASISWA)",
            color='Rata-Rata Skor',
            height=500,
            hover_data={'Letter': False, 'Rata-Rata Skor': True, 'Pertanyaan': True}
        )

        # Tampilkan grafik
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        # Visualisasi Line Chart
        fig_line = px.line(
            avg_scores2,
            x='Letter',
            y='Rata-Rata Skor',
            title="Rata-Rata Skor (SARANA MAHASISWA) - Line Chart",
            markers=True,
            height=500
        )
        
        st.plotly_chart(fig_line, use_container_width=True)

    

 # Pilih pertanyaan tertentu untuk ditampilkan
    selected_question = st.selectbox("🔍 Pilih Pertanyaan untuk Melihat Detail:", avg_scores2['Pertanyaan'])
    selected_value = avg_scores2[avg_scores2['Pertanyaan'] == selected_question]['Rata-Rata Skor'].values[0]

    col1,col2 = st.columns(2)

    with col1:
        # Tampilkan tabel
        st.data_editor(
            avg_scores2,
            column_config={
                "Rata-Rata Skor": st.column_config.ProgressColumn(
                    "Rata-Rata Skor",
                    help="Skor rata-rata berdasarkan indikator",
                    min_value=0,
                    max_value=5
                ),
            },
            hide_index=True,
            use_container_width=True
        )
    
    with col2:

        col1,col2 = st.columns(2)

                # Display metrics with individual borders
        st.markdown("""<style>
            .metric-box {
                text-align: center;
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 10px;
                background-color: #f5bf4a;
            }
            .metric-box h3 {
                margin: 0;
                font-size: 1.5rem;
                color: black;
            }
            .metric-box p {
                margin: 5px 0 0;
                font-size: 1rem;
                color: black;
            }
        </style>""", unsafe_allow_html=True)

        # Tampilkan nilai terpilih dengan border
        with col1:
            st.markdown(f"""
                <div class="metric-box">
                    <p style="font-size: 24px; margin: 0;"><b>{selected_value:.2f}</b></p>
                    <p>🎯 Skor untuk {selected_question}</p>
                    <small style="color: #888;">(Persentase: {percentage_score:.1f}%)</small>
                </div>
            """, unsafe_allow_html=True)


        with col2:
            st.markdown(f"""
                <div class="metric-box">
                    <p style="font-size: 24px; margin: 0;"><b>{selected_value:.2f}</b></p>
                    <p>🎯 Skor untuk {selected_question}</p>
                    <small style="color: #888;">(Persentase: {percentage_score:.1f}%)</small>
                </div>
            """, unsafe_allow_html=True)



        # Data untuk Donut Chart
        donut_data = pd.DataFrame({
            "Kategori": ["Terpenuhi", "Belum Terpenuhi"],
            "Persentase": [percentage_score, 100 - percentage_score]
        })

        # Visualisasi Donut Chart dengan Plotly
        fig_donut = px.pie(
            donut_data,
            names='Kategori',
            values='Persentase',
            title=f"Persentase Skor untuk '{selected_question}' (Skala 1-5)",
            hole=0.5,  # Membuat tampilan menjadi donut chart
            color_discrete_sequence=["#36A2EB", "#FFCE56"]  # Warna: Biru untuk Terpenuhi, Kuning untuk Belum Terpenuhi
        )

        
        st.plotly_chart(fig_donut, use_container_width=True)

