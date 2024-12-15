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
    <h2 style="text-align: center;">📊Dashboard Tata Kelola, Tata Pamong & Kerja Sama</h2>
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
tab1, tab2 = st.tabs(["👨‍🏫 TATA KELOLA DOSEN & TENAGA PENDIDIK", "🎓 TATA KELOLA MAHASISWA"])

# Tab SARANA DOSENS
with tab1:
    
    # Load data
    data1 = load_data("C2.tatakeloladosendantendik-prep.csv")

    col1, col2 = st.columns(2)
    with col1:
        # Pilih Status
        status_filter = st.selectbox("🔍 Pilih Status:", ["All"] + list(data1['Status Bpk/Ibu/Saudara/i.'].unique()))

        # Filter data berdasarkan status
        if status_filter == "All":
            # Jika status "All" dipilih, tampilkan seluruh data
            filtered_data1 = data1
        elif status_filter in data1['Status Bpk/Ibu/Saudara/i.'].values:
            # Jika status valid, tampilkan data sesuai status
            filtered_data1 = data1[data1['Status Bpk/Ibu/Saudara/i.'] == status_filter]
        else:
            # Jika status tidak valid, tampilkan pesan dan data kosong
            st.write("Status yang dipilih tidak valid.")
            filtered_data1 = pd.DataFrame()  # Set data kosong untuk status tidak valid
    with col2:
        # Pilih Pertanyaan (berdasarkan kolom-kolom pertanyaan yang ada di filtered data)
        pertanyaan_list = filtered_data1.columns[1:-1]  # Asumsi pertanyaan ada di kolom 1 hingga kolom terakhir sebelum kolom status
        pertanyaan_filter = st.selectbox("🔍 Pilih Pertanyaan:", pertanyaan_list)
    
    # Filter data berdasarkan pertanyaan yang dipilih
    filtered_data2 = filtered_data1[['Status Bpk/Ibu/Saudara/i.', pertanyaan_filter]]

    # Hitung rata-rata skor untuk setiap pertanyaan dalam data yang telah difilter
    avg_scores1 = filtered_data1.iloc[:, 1:-1].mean().reset_index()
    avg_scores1.columns = ['Indikator', 'Rata-Rata Skor']

    # Menyiapkan huruf untuk sumbu X (a, b, c, ...)
    letters = [chr(i) for i in range(97, 97 + len(avg_scores1))]  # Menghasilkan list ['a', 'b', 'c', ...]
    avg_scores1['Indikator'] = letters  # Menggunakan huruf untuk sumbu X

        # Tambahkan kolom 'Pertanyaan' untuk menampilkan pertanyaan di hover
    avg_scores1['Pertanyaan'] = filtered_data1.columns[1:-1]

    # Visualisasi Bar Chart untuk Rata-Rata Skor
    fig_bar = px.bar(
        avg_scores1,
        title='Distribusi Rata-Rata Skor Berdasarkan Indikator',
        x='Indikator',
        y='Rata-Rata Skor',
        labels={'Indikator': 'Indikator', 'Rata-Rata Skor': 'Rata-Rata Skor'},
        color='Rata-Rata Skor',
        color_continuous_scale='Blues',
        height=700,
        hover_data={'Indikator': True, 'Rata-Rata Skor': True, 'Pertanyaan': True}  # Menambahkan pertanyaan ke tooltip
    )
        # Mengatur posisi judul agar berada di tengah
    fig_bar.update_layout(
        title_x=0.2  # Menempatkan judul di tengah (0.5 artinya di tengah dari grafik)
    )

    # Tambahkan garis rata-rata sebagai referensi
    avg_line = avg_scores1['Rata-Rata Skor'].mean()
    fig_bar.add_hline(y=avg_line, line_dash="dash", line_color="red", 
                    annotation_text=f"Rata-rata {avg_line:.2f}", annotation_position="top left")

    

    # Membuat layout kolom
    col = st.columns((1.5, 4 ,2), gap='medium')

    with col[1]:
        # Tampilkan Bar Chart
        st.plotly_chart(fig_bar, use_container_width=True, use_container_high=True)

    with col[2]:



        st.data_editor(
            avg_scores1,
            column_config={
                "Rata-Rata Skor": st.column_config.ProgressColumn(
                    "Rata-Rata Skor",
                    help="Skor rata-rata berdasarkan indikator",
                    format="",  # Format angka
                    min_value=0,  # Skor minimal
                    max_value=5,  # Skor maksimal (asumsi skor 1-5)
                ),
            },
            hide_index=True,
            use_container_width=True  # Menggunakan lebar kontainer penuh untuk tabel
        )

        fig_pie_simple = px.pie(
            avg_scores1,
            names='Indikator',  # Kategori
            values='Rata-Rata Skor',  # Nilai kontribusi
            hole=0.5, 
            title='Distribusi Rata-Rata Skor per Indikator',
            color_discrete_sequence=px.colors.sequential.Blues,  # Warna gradasi biru
            
        )

        # Menampilkan Pie Chart
        st.plotly_chart(fig_pie_simple, use_container_width=True)



    # Hitung rata-rata skor untuk pertanyaan yang dipilih
    avg_score = filtered_data2[pertanyaan_filter].mean()

        # Cek nilai rata-rata sebelumnya dan hitung delta
    if "previous_avg_score" not in st.session_state:
        st.session_state.previous_avg_score = avg_score  # Menyimpan nilai pertama kali

    delta = avg_score - st.session_state.previous_avg_score
    delta_label = "Naik" if delta > 0 else "Turun"

    # Tentukan delta_color berdasarkan delta
    delta_color = "normal" if delta > 0 else "inverse"  # "normal" untuk kenaikan (hijau), "inverse" untuk penurunan (merah)

    # Update nilai rata-rata sebelumnya
    st.session_state.previous_avg_score = avg_score

    with col[0]:
        # Membungkus komponen metric dengan HTML untuk menambahkan border
        st.markdown(f"""
            <div style="border: 1px solid {'green' if delta > 0 else 'red'}; padding: 10px; border-radius: 8px; display: inline-block; text-align: center;">
                <p style="font-size: 15px; margin: 0;">Rata-Rata Skor untuk {pertanyaan_filter}</p>
                <p style="font-size: 30px; margin: 0; font-weight: bold;">{avg_score:.2f}</p>
                <p style="font-size: 16px; color: {'green' if delta > 0 else 'red'};">{delta:.2f} {delta_label}</p>
            </div>
        """, unsafe_allow_html=True)


            
        # Mengonversi rata-rata skor menjadi persentase
        percentage_score = (avg_score / 5) * 100  # Konversi ke persentase dari skor 1-5

        # Menentukan kategori "Terpenuhi" (skor > 60) dan "Belum Terpenuhi" (skor <= 60)
        category = 'Terpenuhi' if percentage_score > 60 else 'Belum Terpenuhi'

        # Data untuk Donut Chart
        donut_data = pd.DataFrame({
            "Kategori": [category, "Belum Terpenuhi" if category == "Terpenuhi" else "Terpenuhi"],
            "Persentase": [percentage_score, 100 - percentage_score]
        })

        
            # Visualisasi Donut Chart dengan Plotly
        fig_donut = px.pie(
            donut_data,
            names='Kategori',
            values='Persentase',
            title=f"Evaluasi Persentase Berdasarkan Rata-Rata Skor ({pertanyaan_filter})",
            hole=0.5,  # Membuat tampilan menjadi donut chart
            color='Kategori',
            color_discrete_sequence=["#36A2EB", "#FFCE56"]  # Warna: Biru untuk Terpenuhi, Kuning untuk Belum Terpenuhi
        )

        # Mengubah posisi legend (indikator warna) ke bawah
        fig_donut.update_layout(
            legend=dict(
                orientation="h",  # Horizontal
                yanchor="bottom",  # Penempatan legend di bagian bawah
                y=-0.2,  # Jarak dari grafik
                xanchor="center",  # Penempatan legend di tengah
                x=0.5  # Posisi horisontal legend
            )
        )

        
        # Tampilkan Donut Chart
        st.plotly_chart(fig_donut, use_container_width=True)

        


# Tab SARANA MAHASISWA# Tab SARANA MAHASISWA
with tab2:
    # Load dataset dengan header di baris pertama dan kedua
    def load_data_with_multi_header(file_path):
        # Membaca file dengan header di baris pertama dan kedua
        data = pd.read_csv(file_path, header=[0, 1])
        # Menyesuaikan header menjadi kolom tunggal
        data.columns = ['_'.join(col).strip() for col in data.columns.values]
        return data

    # Load dan bersihkan data
    data2 = load_data_with_multi_header("C2.tatakelolamhs-preprossesing.csv")
    data2 = clean_data(data2)  # Jika ada fungsi clean_data, tetap digunakan

    # Hitung rata-rata skor untuk setiap pertanyaan
    avg_scores2 = data2.iloc[:, 1:].mean().reset_index()  # Mengambil rata-rata untuk setiap pertanyaan
    avg_scores2.columns = ['Pertanyaan', 'Rata-Rata Skor']

    # Menyiapkan huruf untuk sumbu X (a, b, c, ...)
    letters = [chr(i) for i in range(97, 97 + len(avg_scores2))]  # Menghasilkan list ['a', 'b', 'c', ...]
    avg_scores2['Letter'] = letters

    # Visualisasi data dengan Area Chart
    fig2 = px.bar(
        avg_scores2,
        x='Letter',  # Sumbu X menggunakan huruf
        y='Rata-Rata Skor',
        title="🎓 Rata-Rata Skor untuk Setiap Pertanyaan (SARANA MAHASISWA)",
        color='Rata-Rata Skor',  # Pewarnaan berdasarkan skor
        height=500,
        hover_data={'Letter': False, 'Rata-Rata Skor': True, 'Pertanyaan': True}  # Informasi saat kursor disorot
    )

    # Tambahkan garis rata-rata sebagai referensi
    avg_line = avg_scores2['Rata-Rata Skor'].mean()
    fig2.add_hline(
        y=avg_line,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Rata-rata {avg_line:.2f}",
        annotation_position="top left"
    )

    # Tampilkan grafik
    st.plotly_chart(fig2, use_container_width=True)

    # Pilih pertanyaan tertentu untuk ditampilkan
    selected_question = st.selectbox("🔍 Pilih Pertanyaan untuk Melihat Detail:", avg_scores2['Pertanyaan'])
    selected_value = avg_scores2[avg_scores2['Pertanyaan'] == selected_question]['Rata-Rata Skor'].values[0]

    # Tampilkan nilai terpilih
    st.metric(f"Skor untuk {selected_question}", f"{selected_value:.2f}")

    # Menghitung persentase skor untuk pertanyaan yang dipilih (skala 1-5)
    percentage_score = (selected_value / 5) * 100  # Konversi ke persentase (1-5 skala)

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

    # Tampilkan nilai rata-rata dan Donut Chart
    st.metric(f"Rata-Rata Skor untuk {selected_question}", f"{selected_value:.2f} dari 5")
    st.plotly_chart(fig_donut, use_container_width=True)

    # Tampilkan data dalam bentuk tabel
    st.subheader("📋 Data Rata-Rata Skor:")
    st.dataframe(avg_scores2)

