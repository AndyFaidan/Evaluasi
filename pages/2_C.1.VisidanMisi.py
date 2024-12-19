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
            pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", ["All"] + list(pertanyaan_list))  # Menambahkan "All" sebagai pilihan

            # Filter data berdasarkan pertanyaan yang dipilih
            if pertanyaan_filter == "All":
                # Jika "All" dipilih, tampilkan semua pertanyaan
                filtered_data2 = filtered_data1
            else:
                filtered_data2 = filtered_data1[['1. Status Bpk/Ibu/Saudara/i:', pertanyaan_filter]]

            # Filter out "Netral" answers (score == 3)
            non_neutral_data = data[data.apply(lambda row: ~row.isin([3]), axis=1)]

            # Count the occurrences of each category (Sangat Kurang, Kurang, Baik, Sangat Baik)
            categories_count = {
                "Sangat Kurang": (non_neutral_data == 1).sum().sum(),
                "Kurang": (non_neutral_data == 2).sum().sum(),
                "Baik": (non_neutral_data == 4).sum().sum(),
                "Sangat Baik": (non_neutral_data == 5).sum().sum(),
            }

            # Calculate the total number of relevant answers
            total_non_neutral = sum(categories_count.values())

            # Prepare data for the pie chart
            fulfillment_data1 = pd.DataFrame({
                'Kategori': categories_count.keys(),
                'Jumlah': categories_count.values(),
                'Persentase': [count / total_non_neutral * 100 for count in categories_count.values()]
            })

            # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
            avg_scores = filtered_data1.iloc[:, 1:].mean().reset_index()
            avg_scores.columns = ['Indikator', 'Rata-Rata Skor']

            # Menghitung rata-rata skor berdasarkan status
            avg_scoresbar = filtered_data1.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()

            # Menghitung skor rata-rata untuk pertanyaan yang dipilih
            if pertanyaan_filter != "All":
                selected_question_avg_score = filtered_data1[pertanyaan_filter].mean()
            else:
                selected_question_avg_score = filtered_data1[pertanyaan_list].mean().mean()  # Rata-rata semua pertanyaan jika "All" dipilih

            # Hitung persentase terpenuhi dan tidak terpenuhi
            fulfilled_percentage = (selected_question_avg_score / 5) * 100
            not_fulfilled_percentage = 100 - fulfilled_percentage

            # Siapkan data untuk donut chart
            fulfillment_data = pd.DataFrame({
                'Status': ['Paham', 'Tidak Paham'],
                'Persentase': [fulfilled_percentage, not_fulfilled_percentage]
            })



    
    # Mengonversi DataFrame ke format long untuk pembuatan grouped bar chart
    avg_scores_long = avg_scoresbar.melt(
        id_vars='1. Status Bpk/Ibu/Saudara/i:',  # Kolom status sebagai identifier
        var_name='Indikator',                   # Nama kolom indikator (a, b, c, ...)
        value_name='Rata-Rata Skor'             # Nama kolom nilai rata-rata skor
    )

    # Terapkan fungsi kategori ke setiap nilai skor rata-rata
    avg_scores_long['Kategori'] = avg_scores_long['Rata-Rata Skor'].apply(assign_category)

    col1, col2, col3 = st.columns(3)

    # Calculate metrics for 'Rata-Rata Skor' column in avg_scores_df
    min_score = avg_scores_long['Rata-Rata Skor'].min()
    max_score = avg_scores_long['Rata-Rata Skor'].max()
    mean_score = avg_scores_long['Rata-Rata Skor'].mean()

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
            <div style="border: 0.5px solid; padding: 10px; border-radius: 8px; text-align: center; background-color: #f5bf4a ">
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

    # Layout: Create three columns for the components
    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:
        with st.container(border=True):
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
                title_x=0.25,                              # Pusatkan judul chart
                font=dict(
                    family="Arial, sans-serif",           # Jenis font
                    size=14,                              # Ukuran font
                    color="black"                         # Warna font
                ),
                margin=dict(l=40, r=40, t=60, b=40),      # Margin kiri, kanan, atas, bawah
                height=400,                               # Tinggi chart
                width=1000                                 # Lebar chart
            )


            st.plotly_chart(barchart, use_container_width=True)

    with col2:
        with st.container(border=True):
       
            # Membuat donut chart
            fig_donut = px.pie(
                fulfillment_data,
                values='Persentase',  # Nilai persentase
                names='Status',  # Nama kategori
                hole=0.2,  # Membuat efek donut
                title=f"Persentase Pemahaman Setiap Pertanyaan",  # Judul chart
                color_discrete_sequence=px.colors.sequential.Sunset  # Warna chart
            )

            # Update layout untuk judul dan posisi legenda
            fig_donut.update_layout(
                title_x=0.0,  # Memusatkan judul
                legend_title="Status",  # Menambahkan judul untuk legenda
                legend_orientation="h",  # Membuat legenda horizontal
                legend_yanchor="bottom",  # Menempatkan legenda di bawah
                legend_y=-0.3,  # Menurunkan posisi legenda
                legend_x=0.5,  # Memusatkan legenda secara horizontal
                legend_xanchor="center",  # Menjaga posisi legenda tetap di tengah
                height=400,
                width=400  # Ensure the chart width is adequate
            )

            # Menampilkan donut chart di Streamlit
            st.plotly_chart(fig_donut)

    with col3:
        with st.container(border=True):
                # Create and style the pie chart
            fig_donut = px.pie(
                fulfillment_data1,
                values='Persentase',
                names='Kategori',
                hole=0.5,
                title="Distribusi Setiap Kategori",
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
                height=400,
                width=400,  # Ensure the chart width is adequate
            )

            # Display the pie chart
            st.plotly_chart(fig_donut, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
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
                title_x=0.2,                         # Center the title
                font=dict(
                    family="Arial, sans-serif",
                    size=14,
                    color="black"
                ),
                margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for better spacing
                height=400,                          # Set height for the chart
                width=600,                           # Set width for the chart
                xaxis=dict(
                    showticklabels=False  # Hide the labels on the X-axis (indicators)
                )
            )

            # Display the line chart
            st.plotly_chart(linechart, use_container_width=True)


    with col2:
        with st.container(border=True):
            # Create and style the bar chart (horizontal)
            fig_bar = px.bar(
                fulfillment_data1,
                x='Persentase',  # The percentage values for the bars
                y='Kategori',  # The categories for the bars
                orientation='h',  # Horizontal bar chart
                title="Distribusi Setiap Kategori",  # Title of the chart
                color='Kategori',  # Use 'Kategori' for coloring the bars
                color_discrete_sequence=px.colors.sequential.Purp  # Color sequence
            )

            # Update layout for the bar chart
            fig_bar.update_layout(
                title_x=0.4,  # Position the title
                legend_title="Kategori",  # Title of the legend
                legend_orientation="h",  # Horizontal legend
                legend_yanchor="bottom",  # Position the legend at the bottom
                legend_y=-0.3,  # Lower the legend
                legend_x=0.5,  # Center the legend horizontally
                legend_xanchor="center",  # Anchor the legend to the center
                height=400,  # Height of the chart
                width=600,  # Width of the chart
            )

            # Display the horizontal bar chart
            st.plotly_chart(fig_bar, use_container_width=True)


    # Menampilkan tabel rata-rata skor dengan kategori
    st.container(border=True)
    st.data_editor(
                avg_scores_long,
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

        

with tab2:
    # Load data
    data = load_data("C.1.SurveyPemahamanVisiMisiTIF.csv")
    

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
            pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", ["All"] + list(pertanyaan_list))  # Menambahkan "All" sebagai pilihan

            # Filter data berdasarkan pertanyaan yang dipilih
            if pertanyaan_filter == "All":
                # Jika "All" dipilih, tampilkan semua pertanyaan
                filtered_data2 = filtered_data1
            else:
                filtered_data2 = filtered_data1[['1. Status Bpk/Ibu/Saudara/i:', pertanyaan_filter]]

            # Filter out "Netral" answers (score == 3)
            non_neutral_data = data[data.apply(lambda row: ~row.isin([3]), axis=1)]

            # Count the occurrences of each category (Sangat Kurang, Kurang, Baik, Sangat Baik)
            categories_count = {
                "Sangat Kurang": (non_neutral_data == 1).sum().sum(),
                "Kurang": (non_neutral_data == 2).sum().sum(),
                "Baik": (non_neutral_data == 4).sum().sum(),
                "Sangat Baik": (non_neutral_data == 5).sum().sum(),
            }

            # Calculate the total number of relevant answers
            total_non_neutral = sum(categories_count.values())

            # Prepare data for the pie chart
            fulfillment_data1 = pd.DataFrame({
                'Kategori': categories_count.keys(),
                'Jumlah': categories_count.values(),
                'Persentase': [count / total_non_neutral * 100 for count in categories_count.values()]
            })

            # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
            avg_scores = filtered_data1.iloc[:, 1:].mean().reset_index()
            avg_scores.columns = ['Indikator', 'Rata-Rata Skor']

            # Menghitung rata-rata skor berdasarkan status
            avg_scoresbar = filtered_data1.groupby('1. Status Bpk/Ibu/Saudara/i:').mean().reset_index()

            # Menghitung skor rata-rata untuk pertanyaan yang dipilih
            if pertanyaan_filter != "All":
                selected_question_avg_score = filtered_data1[pertanyaan_filter].mean()
            else:
                selected_question_avg_score = filtered_data1[pertanyaan_list].mean().mean()  # Rata-rata semua pertanyaan jika "All" dipilih

            # Hitung persentase terpenuhi dan tidak terpenuhi
            fulfilled_percentage = (selected_question_avg_score / 5) * 100
            not_fulfilled_percentage = 100 - fulfilled_percentage

            # Siapkan data untuk donut chart
            fulfillment_data = pd.DataFrame({
                'Status': ['Paham', 'Tidak Paham'],
                'Persentase': [fulfilled_percentage, not_fulfilled_percentage]
            })



    
    # Mengonversi DataFrame ke format long untuk pembuatan grouped bar chart
    avg_scores_long = avg_scoresbar.melt(
        id_vars='1. Status Bpk/Ibu/Saudara/i:',  # Kolom status sebagai identifier
        var_name='Indikator',                   # Nama kolom indikator (a, b, c, ...)
        value_name='Rata-Rata Skor'             # Nama kolom nilai rata-rata skor
    )

    # Terapkan fungsi kategori ke setiap nilai skor rata-rata
    avg_scores_long['Kategori'] = avg_scores_long['Rata-Rata Skor'].apply(assign_category)

    col1, col2, col3 = st.columns(3)

    # Calculate metrics for 'Rata-Rata Skor' column in avg_scores_df
    min_score = avg_scores_long['Rata-Rata Skor'].min()
    max_score = avg_scores_long['Rata-Rata Skor'].max()
    mean_score = avg_scores_long['Rata-Rata Skor'].mean()

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
            <div style="border: 0.5px solid; padding: 10px; border-radius: 8px; text-align: center; background-color: #f5bf4a ">
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

    # Layout: Create three columns for the components
    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:
        with st.container(border=True):
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
                title_x=0.25,                              # Pusatkan judul chart
                font=dict(
                    family="Arial, sans-serif",           # Jenis font
                    size=14,                              # Ukuran font
                    color="black"                         # Warna font
                ),
                margin=dict(l=40, r=40, t=60, b=40),      # Margin kiri, kanan, atas, bawah
                height=400,                               # Tinggi chart
                width=1000                                 # Lebar chart
            )


            st.plotly_chart(barchart, use_container_width=True)

    with col2:
        with st.container(border=True):
       
            # Membuat donut chart
            fig_donut = px.pie(
                fulfillment_data,
                values='Persentase',  # Nilai persentase
                names='Status',  # Nama kategori
                hole=0.2,  # Membuat efek donut
                title=f"Persentase Pemahaman Setiap Pertanyaan",  # Judul chart
                color_discrete_sequence=px.colors.sequential.Sunset  # Warna chart
            )

            # Update layout untuk judul dan posisi legenda
            fig_donut.update_layout(
                title_x=0.0,  # Memusatkan judul
                legend_title="Status",  # Menambahkan judul untuk legenda
                legend_orientation="h",  # Membuat legenda horizontal
                legend_yanchor="bottom",  # Menempatkan legenda di bawah
                legend_y=-0.3,  # Menurunkan posisi legenda
                legend_x=0.5,  # Memusatkan legenda secara horizontal
                legend_xanchor="center",  # Menjaga posisi legenda tetap di tengah
                height=400,
                width=400  # Ensure the chart width is adequate
            )

            # Menampilkan donut chart di Streamlit
            st.plotly_chart(fig_donut)

    with col3:
        with st.container(border=True):
                # Create and style the pie chart
            fig_donut = px.pie(
                fulfillment_data1,
                values='Persentase',
                names='Kategori',
                hole=0.5,
                title="Distribusi Setiap Kategori",
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
                height=400,
                width=400,  # Ensure the chart width is adequate
            )

            # Display the pie chart
            st.plotly_chart(fig_donut, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
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
                title_x=0.2,                         # Center the title
                font=dict(
                    family="Arial, sans-serif",
                    size=14,
                    color="black"
                ),
                margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for better spacing
                height=400,                          # Set height for the chart
                width=600,                           # Set width for the chart
                xaxis=dict(
                    showticklabels=False  # Hide the labels on the X-axis (indicators)
                )
            )

            # Display the line chart
            st.plotly_chart(linechart, use_container_width=True)


    with col2:
        with st.container(border=True):
            # Create and style the bar chart (horizontal)
            fig_bar = px.bar(
                fulfillment_data1,
                x='Persentase',  # The percentage values for the bars
                y='Kategori',  # The categories for the bars
                orientation='h',  # Horizontal bar chart
                title="Distribusi Setiap Kategori",  # Title of the chart
                color='Kategori',  # Use 'Kategori' for coloring the bars
                color_discrete_sequence=px.colors.sequential.Purp  # Color sequence
            )

            # Update layout for the bar chart
            fig_bar.update_layout(
                title_x=0.4,  # Position the title
                legend_title="Kategori",  # Title of the legend
                legend_orientation="h",  # Horizontal legend
                legend_yanchor="bottom",  # Position the legend at the bottom
                legend_y=-0.3,  # Lower the legend
                legend_x=0.5,  # Center the legend horizontally
                legend_xanchor="center",  # Anchor the legend to the center
                height=400,  # Height of the chart
                width=600,  # Width of the chart
            )

            # Display the horizontal bar chart
            st.plotly_chart(fig_bar, use_container_width=True)


    # Menampilkan tabel rata-rata skor dengan kategori
    st.container(border=True)
    st.data_editor(
                avg_scores_long,
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

        
