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
st.title("Dashboard Survei Visi dan Misi STT Wastukancana")

# Pilih file dataset
data_files = {
    "STTWASTUKANCANA": "C.1.HasilSurveyPemahamanVMTSUPPS2024.csv",
    "TEKNIKINFORMATIKA": "C.1.HasilSurveyPemahamanVMTSPS2024.csv"
}

try:
    # Membaca data
    data_STTWASTUKANCANA = pd.read_csv(data_files["STTWASTUKANCANA"])
    data_TEKNIKINFORMATIKA = pd.read_csv(data_files["TEKNIKINFORMATIKA"])

    # Membersihkan data
    data_STTWASTUKANCANA.columns = data_STTWASTUKANCANA.columns.str.strip()
    data_TEKNIKINFORMATIKA.columns = data_TEKNIKINFORMATIKA.columns.str.strip()

    # Filter berdasarkan status
    status_STTWASTUKANCANA = data_STTWASTUKANCANA['1. Status Bpk/Ibu/Saudara/i:'].unique()
    status_TEKNIKINFORMATIKA = data_TEKNIKINFORMATIKA['1. Status Bpk/Ibu/Saudara/i:'].unique()

    # Analisis Pemahaman Visi dan Misi
    st.subheader("Skala Pemahaman Visi dan Misi")

    skala_cols = [
        '5. Saya memahami Visi dan Misi STT Wastukancana.',
        '6. Saya memahami bahwa Visi dan Misi STT Wastukancana harus dilaksanakan.',
        '7. Saya memahami fungsi Visi dan Misi STT Wastukancana sebagai arahan dalam kegiatan akademik.',
        '8. Saya memahami dengan baik bahwa setiap program harus dilaksanakan harus berdasarkan Visi dan Misi STT Wastukancana.',
        '9. Saya memahami Visi dan Misi STT Wastukancana sudah realistik.',
        '5. Saya memahami Visi dan Misi Program Studi Teknik Informatika STT Wastukancana.',
        '6. Saya memahami bahwa Visi dan Misi Program Studi Teknik Informatika STT Wastukancana harus dilaksanakan.',
        '7. Saya memahami fungsi Visi dan Misi Program Studi Teknik Informatika STT Wastukancana sebagai arahan dalam kegiatan akademik.',
        '8. Saya memahami dengan baik bahwa setiap program harus dilaksanakan harus berdasarkan Visi dan Misi Program Studi Teknik Informatika STT Wastukancana.',
        '9. Saya memahami Visi dan Misi Program Studi Teknik Informatika STT Wastukancana sudah realistik.'
    ]

    # Tampilkan deskripsi survey dan grafik
    c1, c2 = st.columns(2)

    # Bagian STTWASTUKANCANA
    with c1:
        st.markdown("""
        **Survey Pemahaman Visi dan Misi STT Wastukancana**
        Survey ini bertujuan untuk mengetahui pemahaman responden mengenai visi dan misi yang ada di STT Wastukancana.
        """)
        
        st.write("Data STT WASTUKANCANA:")
        st.dataframe(data_STTWASTUKANCANA)

        selected_status_STTWASTUKANCANA = st.selectbox("Pilih Status (STTWASTUKANCANA)", options=["All"] + list(status_STTWASTUKANCANA))
        
        if selected_status_STTWASTUKANCANA != "All":  # Terapkan filter status
            data_STTWASTUKANCANA = data_STTWASTUKANCANA[data_STTWASTUKANCANA['1. Status Bpk/Ibu/Saudara/i:'] == selected_status_STTWASTUKANCANA]

        status_counts_STTWASTUKANCANA = data_STTWASTUKANCANA['1. Status Bpk/Ibu/Saudara/i:'].value_counts()
        fig_status_STTWASTUKANCANA = px.bar(status_counts_STTWASTUKANCANA, x=status_counts_STTWASTUKANCANA.index, y=status_counts_STTWASTUKANCANA.values, 
                                 labels={'x': 'Status', 'y': 'Jumlah'}, title="Distribusi Status STTWASTUKANCANA")
        st.plotly_chart(fig_status_STTWASTUKANCANA, use_container_width=True)

        durasi_counts_STTWASTUKANCANA = data_STTWASTUKANCANA['2. Berapa lama Bpk/Ibu/Saudara/i bergabung atau mengenal STT Wastukancana?'].value_counts()
        fig_durasi_STTWASTUKANCANA = px.pie(durasi_counts_STTWASTUKANCANA, names=durasi_counts_STTWASTUKANCANA.index, values=durasi_counts_STTWASTUKANCANA.values, 
                                 title="Durasi Mengenal STTWASTUKANCANA")
        st.plotly_chart(fig_durasi_STTWASTUKANCANA, use_container_width=True)

        for col in skala_cols:
            if col in data_STTWASTUKANCANA.columns:
                st.write(f"**{col} (STTWASTUKANCANA)**")
                fig_scale_STTWASTUKANCANA = px.histogram(data_STTWASTUKANCANA, x=col, nbins=5, 
                                              labels={col: "Skala"}, title=f"Distribusi {col} (STTWASTUKANCANA)")
                st.plotly_chart(fig_scale_STTWASTUKANCANA, use_container_width=True)

    # Bagian TEKNIKINFORMATIKA
    with c2:
        st.markdown("""
        **Survey Pemahaman Visi dan Misi Teknik Informatika**
        Survey ini bertujuan untuk mengetahui pemahaman responden mengenai visi dan misi yang ada di Program Studi Teknik Informatika.
        """)
        
        st.write("Data TEKNIK INFORMATIKA:")
        st.dataframe(data_TEKNIKINFORMATIKA)

        selected_status_TEKNIKINFORMATIKA = st.selectbox("Pilih Status (TEKNIKINFORMATIKA)", options=["All"] + list(status_TEKNIKINFORMATIKA))
        
        if selected_status_TEKNIKINFORMATIKA != "All":  # Terapkan filter status
            data_TEKNIKINFORMATIKA = data_TEKNIKINFORMATIKA[data_TEKNIKINFORMATIKA['1. Status Bpk/Ibu/Saudara/i:'] == selected_status_TEKNIKINFORMATIKA]

        status_counts_TEKNIKINFORMATIKA = data_TEKNIKINFORMATIKA['1. Status Bpk/Ibu/Saudara/i:'].value_counts()
        fig_status_TEKNIKINFORMATIKA = px.bar(status_counts_TEKNIKINFORMATIKA, x=status_counts_TEKNIKINFORMATIKA.index, y=status_counts_TEKNIKINFORMATIKA.values, 
                                labels={'x': 'Status', 'y': 'Jumlah'}, title="Distribusi Status TEKNIKINFORMATIKA")
        st.plotly_chart(fig_status_TEKNIKINFORMATIKA, use_container_width=True)

        durasi_counts_TEKNIKINFORMATIKA = data_TEKNIKINFORMATIKA['2. Berapa lama Bpk/Ibu/Saudara/i bergabung atau mengenal STT Wastukancana?'].value_counts()
        fig_durasi_TEKNIKINFORMATIKA = px.pie(durasi_counts_TEKNIKINFORMATIKA, names=durasi_counts_TEKNIKINFORMATIKA.index, values=durasi_counts_TEKNIKINFORMATIKA.values, 
                                title="Durasi Mengenal TEKNIKINFORMATIKA")
        st.plotly_chart(fig_durasi_TEKNIKINFORMATIKA, use_container_width=True)

        for col in skala_cols:
            if col in data_STTWASTUKANCANA.columns:
                st.write(f"**{col} (TEKNIKINFORMATIKA)**")
                fig_scale_STTWASTUKANCANA = px.histogram(data_STTWASTUKANCANA, x=col, nbins=5, 
                                              labels={col: "Skala"}, title=f"Distribusi {col} (TEKNIKINFORMATIKA)")
                st.plotly_chart(fig_scale_STTWASTUKANCANA, use_container_width=True)

except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
except KeyError as e:
    st.error(f"Kolom tidak ditemukan: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
