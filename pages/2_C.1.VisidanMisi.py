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
    <h2 style="text-align: center;">📊 Survey Pemahaman Dosen, Tendik Dan Mahasiswa Terhadap VMTS UPPS dan PS
</h2>
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

# Tampilkan deskripsi survei dan grafik
tab1, tab2 = st.tabs(["👨‍🏫 Survey Pemahaman Visi & Misi STT Wastukancana", "🎓 Survey Pemahaman Visi & Misi Teknik Informatika"])

with tab1:
    # Load data
    data = load_data("C.1.SurveyPemahamanVisiMisiSTTWastukancana.csv")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pilih Status
        status_filter = st.selectbox("🔍 Pilih Status:", ["All"] + list(data['1. Status Bpk/Ibu/Saudara/i:'].unique()))

        # Filter data berdasarkan status
        if status_filter == "All":
            filtered_data1 = data
        else:
            filtered_data1 = data[data['1. Status Bpk/Ibu/Saudara/i:'] == status_filter]

        # Calculate average scores for all questions grouped by status
        avg_scores = filtered_data1.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()
    with col2:
        # Pilih Pertanyaan (berdasarkan kolom-kolom pertanyaan yang ada di filtered data)
        pertanyaan_list = filtered_data1.columns[1:]  # Asumsi pertanyaan ada di kolom 1 hingga kolom terakhir sebelum kolom status
        pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", pertanyaan_list)

    # Filter data berdasarkan pertanyaan yang dipilih
    filtered_data2 = filtered_data1[['1. Status Bpk/Ibu/Saudara/i:', pertanyaan_filter]]

    # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
    avg_scores = filtered_data1.iloc[:, 1:].mean().reset_index()
    avg_scores.columns = ['Indikator', 'Rata-Rata Skor']

    # Menghitung rata-rata skor berdasarkan status
    avg_scoresbar = filtered_data1.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()


            # Menghitung skor rata-rata untuk pertanyaan yang dipilih
    selected_question_avg_score = filtered_data1[pertanyaan_filter].mean()

        # Hitung persentase terpenuhi dan tidak terpenuhi
    fulfilled_percentage = (selected_question_avg_score / 5) * 100
    not_fulfilled_percentage = 100 - fulfilled_percentage

        # Siapkan data untuk donut chart
    fulfillment_data = pd.DataFrame({
            'Status': ['Terpenuhi', 'Tidak Terpenuhi'],
            'Persentase': [fulfilled_percentage, not_fulfilled_percentage]
        })


    col1, col2, col3 = st.columns(3)

    # Calculate metrics
    min_score = avg_scores['Rata-Rata Skor'].min()
    max_score = avg_scores['Rata-Rata Skor'].max()
    mean_score = avg_scores['Rata-Rata Skor'].mean()

    # Display metrics with individual borders
    st.markdown("""<style>
        .metric-box {
            text-align: center;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #f9f9f9;
        }
        .metric-box h3 {
            margin: 0;
            font-size: 1.5rem;
        }
        .metric-box p {
            margin: 5px 0 0;
            font-size: 1rem;
            color: #555;
        }
        </style>""", unsafe_allow_html=True)

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

    # Mengonversi DataFrame ke format long untuk pembuatan grouped bar chart
    avg_scores_long = avg_scoresbar.melt(
        id_vars='1. Status Bpk/Ibu/Saudara/i:',  # Kolom status sebagai identifier
        var_name='Indikator',                   # Nama kolom indikator (a, b, c, ...)
        value_name='Rata-Rata Skor'             # Nama kolom nilai rata-rata skor
    )

    col1, col2 = st.columns(2)

    with col1:

        # Display the data editor with new columns
        st.data_editor(
            avg_scores_long,  # DataFrame yang ditampilkan
            column_config={
                "1. Status Bpk/Ibu/Saudara/i:": st.column_config.TextColumn(
                    "Status",
                    help="Status peserta survei"
                ),
                "Indikator": st.column_config.TextColumn(
                    "Indikator",
                    help="Huruf yang merepresentasikan pertanyaan dalam survei"
                ),
                "Pertanyaan": st.column_config.TextColumn(
                    "Pertanyaan",
                    help="Pertanyaan yang diajukan kepada peserta survei"
                ),
                "Rata-Rata Skor": st.column_config.ProgressColumn(
                    "Rata-Rata Skor",
                    help="Skor rata-rata berdasarkan indikator",
                    format="%.2f",  # Format angka menjadi 2 desimal
                    min_value=0.0,  # Skor minimal
                    max_value=5.0,  # Skor maksimal (asumsi skor 1-5)
                ),
            },
            hide_index=True,  # Menyembunyikan indeks DataFrame
            use_container_width=True  # Memanfaatkan lebar penuh kontainer
        )

    with col2:
       

        # Membuat donut chart
        fig_donut = px.pie(
            fulfillment_data,
            values='Persentase',  # Nilai persentase
            names='Status',  # Nama kategori
            hole=0.4,  # Membuat efek donut
            title=f"Persentase Terpenuhi dan Tidak Terpenuhi untuk '{pertanyaan_filter}'",  # Judul chart
            color_discrete_sequence=px.colors.sequential.Sunset  # Warna chart
        )

        # Update layout untuk judul dan posisi legenda
        fig_donut.update_layout(
            title_x=0.5,  # Memusatkan judul
            legend_title="Status",  # Menambahkan judul untuk legenda
            legend_orientation="h",  # Membuat legenda horizontal
            legend_yanchor="bottom",  # Menempatkan legenda di bawah
            legend_y=-0.3,  # Menurunkan posisi legenda
            legend_x=0.5,  # Memusatkan legenda secara horizontal
            legend_xanchor="center"  # Menjaga posisi legenda tetap di tengah
        )

        # Menampilkan donut chart di Streamlit
        st.plotly_chart(fig_donut)

    col1, col2 = st.columns(2)

    with col1:
        # Filter the data based on the selected status
        filtered_data1 = data[data['1. Status Bpk/Ibu/Saudara/i:'] == status_filter] if status_filter != "All" else data

        # Calculate the average score for each question by status
        avg_scores_line = filtered_data1.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()

        # Convert the data to long format for line chart
        avg_scores_long_line = avg_scores_line.melt(
            id_vars='1. Status Bpk/Ibu/Saudara/i:', 
            var_name='Indikator', 
            value_name='Rata-Rata Skor'
        )

        # Create the line chart using Plotly Express
        linechart = px.line(
            avg_scores_long_line,
            x="Indikator",                # X-axis: Indikator Pertanyaan (a, b, c, ...)
            y="Rata-Rata Skor",           # Y-axis: Rata-Rata Skor
            color="1. Status Bpk/Ibu/Saudara/i:",   # Color the lines based on Status
            markers=True,                 # Show markers on the line chart
            labels={
                "Indikator": "Indikator Pertanyaan",  # Label for X-axis
                "Rata-Rata Skor": "Rata-Rata Skor",   # Label for Y-axis
                "1. Status Bpk/Ibu/Saudara/i:": "Status"
            },
            title="Tren Rata-Rata Skor Berdasarkan Status dan Indikator"  # Title for the chart
        )

        # Customize the chart layout
        linechart.update_layout(
            hovermode="closest",  # Show hover data for the closest point
            xaxis_title="Indikator Pertanyaan",  # X-axis label
            yaxis_title="Rata-Rata Skor",        # Y-axis label
            legend_title="Status",               # Title for the legend
            title_x=0.5,                         # Center the title
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="black"
            ),
            margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for better spacing
            height=600,                          # Set height for the chart
            width=900                            # Set width for the chart
        )

        # Display the line chart
        st.plotly_chart(linechart, use_container_width=True)

    with col2:
         # Membuat grouped bar chart yang lebih interaktif
        barchart = px.bar(
            avg_scores_long,
            x="Indikator",                            # Sumbu X: Indikator
            y="Rata-Rata Skor",                       # Sumbu Y: Skor Rata-Rata
            color="1. Status Bpk/Ibu/Saudara/i:",     # Warna berdasarkan Status
            barmode="group",                          # Gunakan mode group saja
            text="Rata-Rata Skor",                    # Tampilkan skor pada bar
            labels={
                "Indikator": "Indikator Pertanyaan",
                "Rata-Rata Skor": "Rata-Rata Skor",
                "1. Status Bpk/Ibu/Saudara/i:": "Status"
            },
            hover_data={"Rata-Rata Skor": ":.2f"},    # Format hover dengan 2 desimal
            title="Rata-Rata Skor Berdasarkan Status dan Pertanyaan"
        )

        barchart.update_traces(
            texttemplate='%{text:.2f}',               # Format angka pada bar (2 desimal)
            textposition='outside'                   # Tampilkan teks di atas bar
        )

        barchart.update_layout(
            hovermode="closest",                      # Tooltip hanya muncul pada bar yang difokuskan
            xaxis_title="",                           # Hapus label sumbu X
            xaxis=dict(
                showticklabels=False,                 # Menyembunyikan kategori indikator di sumbu X
            ),
            yaxis_title="Rata-Rata Skor",             # Judul sumbu Y
            legend_title="Status",                    # Judul legenda
            title_x=0.5,                              # Pusatkan judul chart
            font=dict(
                family="Arial, sans-serif",           # Jenis font
                size=14,                              # Ukuran font
                color="black"                         # Warna font
            ),
            margin=dict(l=40, r=40, t=60, b=40),      # Margin kiri, kanan, atas, bawah
            height=600,                               # Tinggi chart
            width=900                                 # Lebar chart
        )


        st.plotly_chart(barchart, use_container_width=True)

with tab2:
     # Load data
    data = load_data("C.1.SurveyPemahamanVisiMisiTIF.csv")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pilih Status
        status_filter = st.selectbox("🔍 Pilih Status:", ["All"] + list(data['1. Status Bpk/Ibu/Saudara/i:'].unique()))

        # Filter data berdasarkan status
        if status_filter == "All":
            filtered_data2 = data
        else:
            filtered_data2 = data[data['1. Status Bpk/Ibu/Saudara/i:'] == status_filter]

        # Calculate average scores for all questions grouped by status
        avg_scores1 = filtered_data2.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()
    with col2:
        # Pilih Pertanyaan (berdasarkan kolom-kolom pertanyaan yang ada di filtered data)
        pertanyaan_list = filtered_data2.columns[1:]  # Asumsi pertanyaan ada di kolom 1 hingga kolom terakhir sebelum kolom status
        pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", pertanyaan_list)

    # Filter data berdasarkan pertanyaan yang dipilih
    filtered_data3 = filtered_data2[['1. Status Bpk/Ibu/Saudara/i:', pertanyaan_filter]]

    # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
    avg_scores1 = filtered_data2.iloc[:, 1:].mean().reset_index()
    avg_scores.columns = ['Indikator', 'Rata-Rata Skor']

    # Menghitung rata-rata skor berdasarkan status
    avg_scoresbar1 = filtered_data2.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()

     # Menghitung rata-rata skor berdasarkan status
    avg_scoresbar2 = filtered_data2.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()


    # Menyiapkan huruf sebagai nama indikator (a, b, c, ...)
    letters = [chr(i) for i in range(97, 97 + avg_scoresbar.shape[1] - 1)]  # ['a', 'b', 'c', ...]

    # Mengubah nama kolom pertanyaan (kecuali kolom status) menjadi huruf
    avg_scoresbar.columns = ['1. Status Bpk/Ibu/Saudara/i:'] + letters

            # Menghitung skor rata-rata untuk pertanyaan yang dipilih
    selected_question_avg_score1 = filtered_data2[pertanyaan_filter].mean()

        # Hitung persentase terpenuhi dan tidak terpenuhi
    fulfilled_percentage = (selected_question_avg_score / 5) * 100
    not_fulfilled_percentage = 100 - fulfilled_percentage

        # Siapkan data untuk donut chart
    fulfillment_data = pd.DataFrame({
            'Status': ['Terpenuhi', 'Tidak Terpenuhi'],
            'Persentase': [fulfilled_percentage, not_fulfilled_percentage]
        })


    col1, col2, col3 = st.columns(3)

    # Calculate metrics
    min_score = avg_scores['Rata-Rata Skor'].min()
    max_score = avg_scores['Rata-Rata Skor'].max()
    mean_score = avg_scores['Rata-Rata Skor'].mean()

    # Display metrics with individual borders
    st.markdown("""<style>
        .metric-box {
            text-align: center;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #f9f9f9;
        }
        .metric-box h3 {
            margin: 0;
            font-size: 1.5rem;
        }
        .metric-box p {
            margin: 5px 0 0;
            font-size: 1rem;
            color: #555;
        }
        </style>""", unsafe_allow_html=True)

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

     # Mengonversi DataFrame ke format long untuk pembuatan grouped bar chart
    avg_scores_long2 = avg_scoresbar1.melt(
        id_vars='1. Status Bpk/Ibu/Saudara/i:',  # Kolom status sebagai identifier
        var_name='Indikator',                   # Nama kolom indikator (a, b, c, ...)
        value_name='Rata-Rata Skor'             # Nama kolom nilai rata-rata skor
    )

    # Mengonversi DataFrame ke format long untuk pembuatan grouped bar chart
    avg_scores_long1 = avg_scoresbar1.melt(
        id_vars='1. Status Bpk/Ibu/Saudara/i:',  # Kolom status sebagai identifier
        var_name='Indikator',                   # Nama kolom indikator (a, b, c, ...)
        value_name='Rata-Rata Skor'             # Nama kolom nilai rata-rata skor
    )

    col1, col2 = st.columns(2)

    with col1:

        # Display the data editor with new columns
        st.data_editor(
            avg_scores_long1,  # DataFrame yang ditampilkan
            column_config={
                "1. Status Bpk/Ibu/Saudara/i:": st.column_config.TextColumn(
                    "Status",
                    help="Status peserta survei"
                ),
                "Indikator": st.column_config.TextColumn(
                    "Indikator",
                    help="Huruf yang merepresentasikan pertanyaan dalam survei"
                ),
                "Pertanyaan": st.column_config.TextColumn(
                    "Pertanyaan",
                    help="Pertanyaan yang diajukan kepada peserta survei"
                ),
                "Rata-Rata Skor": st.column_config.ProgressColumn(
                    "Rata-Rata Skor",
                    help="Skor rata-rata berdasarkan indikator",
                    format="%.2f",  # Format angka menjadi 2 desimal
                    min_value=0.0,  # Skor minimal
                    max_value=5.0,  # Skor maksimal (asumsi skor 1-5)
                ),
            },
            hide_index=True,  # Menyembunyikan indeks DataFrame
            use_container_width=True  # Memanfaatkan lebar penuh kontainer
        )

    with col2:
       

        # Membuat donut chart
        fig_donut = px.pie(
            fulfillment_data,
            values='Persentase',  # Nilai persentase
            names='Status',  # Nama kategori
            hole=0.4,  # Membuat efek donut
            title=f"Persentase Terpenuhi dan Tidak Terpenuhi untuk '{pertanyaan_filter}'",  # Judul chart
            color_discrete_sequence=px.colors.sequential.Sunset  # Warna chart
        )

        # Update layout untuk judul dan posisi legenda
        fig_donut.update_layout(
            title_x=0.5,  # Memusatkan judul
            legend_title="Status",  # Menambahkan judul untuk legenda
            legend_orientation="h",  # Membuat legenda horizontal
            legend_yanchor="bottom",  # Menempatkan legenda di bawah
            legend_y=-0.3,  # Menurunkan posisi legenda
            legend_x=0.5,  # Memusatkan legenda secara horizontal
            legend_xanchor="center"  # Menjaga posisi legenda tetap di tengah
        )

        # Menampilkan donut chart di Streamlit
        st.plotly_chart(fig_donut)

    col1, col2 = st.columns(2)

    with col1:
        # Filter the data based on the selected status
        filtered_data1 = data[data['1. Status Bpk/Ibu/Saudara/i:'] == status_filter] if status_filter != "All" else data

        # Calculate the average score for each question by status
        avg_scores_line = filtered_data1.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()

        # Generate letters as indicator names (a, b, c, d, ...)
        letters = [chr(i) for i in range(97, 97 + avg_scores_line.shape[1] - 1)]  # ['a', 'b', 'c', ...]

        # Rename columns to letters (skip the 'Status' column)
        avg_scores_line.columns = ['1. Status Bpk/Ibu/Saudara/i:'] + letters

        # Convert the data to long format for line chart
        avg_scores_long_line = avg_scores_line.melt(
            id_vars='1. Status Bpk/Ibu/Saudara/i:', 
            var_name='Indikator', 
            value_name='Rata-Rata Skor'
        )

        # Create the line chart using Plotly Express
        linechart = px.line(
            avg_scores_long_line,
            x="Indikator",                # X-axis: Indikator Pertanyaan (a, b, c, ...)
            y="Rata-Rata Skor",           # Y-axis: Rata-Rata Skor
            color="1. Status Bpk/Ibu/Saudara/i:",   # Color the lines based on Status
            markers=True,                 # Show markers on the line chart
            labels={
                "Indikator": "Indikator Pertanyaan",  # Label for X-axis
                "Rata-Rata Skor": "Rata-Rata Skor",   # Label for Y-axis
                "1. Status Bpk/Ibu/Saudara/i:": "Status"
            },
            title="Tren Rata-Rata Skor Berdasarkan Status dan Indikator"  # Title for the chart
        )

        # Customize the chart layout
        linechart.update_layout(
            hovermode="closest",  # Show hover data for the closest point
            xaxis_title="Indikator Pertanyaan",  # X-axis label
            yaxis_title="Rata-Rata Skor",        # Y-axis label
            legend_title="Status",               # Title for the legend
            title_x=0.5,                         # Center the title
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="black"
            ),
            margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for better spacing
            height=600,                          # Set height for the chart
            width=900                            # Set width for the chart
        )

        # Display the line chart
        st.plotly_chart(linechart, use_container_width=True)

    with col2:
         # Membuat grouped bar chart yang lebih interaktif
        barchart = px.bar(
            avg_scores_long2,
            x="Indikator",                            # Sumbu X: Indikator
            y="Rata-Rata Skor",                       # Sumbu Y: Skor Rata-Rata
            color="1. Status Bpk/Ibu/Saudara/i:",     # Warna berdasarkan Status
            barmode="group",                          # Gunakan mode group saja
            text="Rata-Rata Skor",                    # Tampilkan skor pada bar
            labels={
                "Indikator": "Indikator Pertanyaan",
                "Rata-Rata Skor": "Rata-Rata Skor",
                "1. Status Bpk/Ibu/Saudara/i:": "Status"
            },
            hover_data={"Rata-Rata Skor": ":.2f"},    # Format hover dengan 2 desimal
            title="Rata-Rata Skor Berdasarkan Status dan Pertanyaan"
        )

        barchart.update_traces(
            texttemplate='%{text:.2f}',               # Format angka pada bar (2 desimal)
            textposition='outside'                   # Tampilkan teks di atas bar
        )

        barchart.update_layout(
            hovermode="closest",                      # Tooltip hanya muncul pada bar yang difokuskan
            xaxis_title="",                           # Hapus label sumbu X
            xaxis=dict(
                showticklabels=False,                 # Menyembunyikan kategori indikator di sumbu X
            ),
            yaxis_title="Rata-Rata Skor",             # Judul sumbu Y
            legend_title="Status",                    # Judul legenda
            title_x=0.5,                              # Pusatkan judul chart
            font=dict(
                family="Arial, sans-serif",           # Jenis font
                size=14,                              # Ukuran font
                color="black"                         # Warna font
            ),
            margin=dict(l=40, r=40, t=60, b=40),      # Margin kiri, kanan, atas, bawah
            height=600,                               # Tinggi chart
            width=900                                 # Lebar chart
        )


        st.plotly_chart(barchart, use_container_width=True)
