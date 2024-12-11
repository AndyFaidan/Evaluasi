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
    "UPPS": "C.1.HasilSurveyPemahamanVMTSUPPS2024.csv",
    "SPS": "C.1.HasilSurveyPemahamanVMTSPS2024.csv"
}

try:
    # Membaca data
    data_upps = pd.read_csv(data_files["UPPS"])
    data_sps = pd.read_csv(data_files["SPS"])

    # Membersihkan data
    data_upps.columns = data_upps.columns.str.strip()
    data_sps.columns = data_sps.columns.str.strip()

    # Filter berdasarkan status
    status_upps = data_upps['1. Status Bpk/Ibu/Saudara/i:'].unique()
    status_sps = data_sps['1. Status Bpk/Ibu/Saudara/i:'].unique()

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

    # Bagian UPPS
    with c1:
        st.markdown("""
        **Survey Pemahaman Visi dan Misi STT Wastukancana**
        Survey ini bertujuan untuk mengetahui pemahaman responden mengenai visi dan misi yang ada di STT Wastukancana.
        """)
        
        st.write("Data STT WASTUKANCANA:")
        st.dataframe(data_upps)

        selected_status_upps = st.selectbox("Pilih Status (UPPS)", options=["All"] + list(status_upps))
        
        if selected_status_upps != "All":  # Terapkan filter status
            data_upps = data_upps[data_upps['1. Status Bpk/Ibu/Saudara/i:'] == selected_status_upps]

        status_counts_upps = data_upps['1. Status Bpk/Ibu/Saudara/i:'].value_counts()
        fig_status_upps = px.bar(status_counts_upps, x=status_counts_upps.index, y=status_counts_upps.values, 
                                 labels={'x': 'Status', 'y': 'Jumlah'}, title="Distribusi Status UPPS")
        st.plotly_chart(fig_status_upps, use_container_width=True)

        durasi_counts_upps = data_upps['2. Berapa lama Bpk/Ibu/Saudara/i bergabung atau mengenal STT Wastukancana?'].value_counts()
        fig_durasi_upps = px.pie(durasi_counts_upps, names=durasi_counts_upps.index, values=durasi_counts_upps.values, 
                                 title="Durasi Mengenal UPPS")
        st.plotly_chart(fig_durasi_upps, use_container_width=True)

        for col in skala_cols:
            if col in data_upps.columns:
                st.write(f"**{col} (UPPS)**")
                fig_scale_upps = px.histogram(data_upps, x=col, nbins=5, 
                                              labels={col: "Skala"}, title=f"Distribusi {col} (UPPS)")
                st.plotly_chart(fig_scale_upps, use_container_width=True)

    # Bagian SPS
    with c2:
        st.markdown("""
        **Survey Pemahaman Visi dan Misi Teknik Informatika**
        Survey ini bertujuan untuk mengetahui pemahaman responden mengenai visi dan misi yang ada di Program Studi Teknik Informatika.
        """)
        
        st.write("Data TEKNIK INFORMATIKA:")
        st.dataframe(data_sps)

        selected_status_sps = st.selectbox("Pilih Status (SPS)", options=["All"] + list(status_sps))
        
        if selected_status_sps != "All":  # Terapkan filter status
            data_sps = data_sps[data_sps['1. Status Bpk/Ibu/Saudara/i:'] == selected_status_sps]

        status_counts_sps = data_sps['1. Status Bpk/Ibu/Saudara/i:'].value_counts()
        fig_status_sps = px.bar(status_counts_sps, x=status_counts_sps.index, y=status_counts_sps.values, 
                                labels={'x': 'Status', 'y': 'Jumlah'}, title="Distribusi Status SPS")
        st.plotly_chart(fig_status_sps, use_container_width=True)

        durasi_counts_sps = data_sps['2. Berapa lama Bpk/Ibu/Saudara/i bergabung atau mengenal STT Wastukancana?'].value_counts()
        fig_durasi_sps = px.pie(durasi_counts_sps, names=durasi_counts_sps.index, values=durasi_counts_sps.values, 
                                title="Durasi Mengenal SPS")
        st.plotly_chart(fig_durasi_sps, use_container_width=True)

        for col in skala_cols:
            if col in data_sps.columns:
                st.write(f"**{col} (SPS)**")
                fig_scale_sps = px.histogram(data_sps, x=col, nbins=5, 
                                             labels={col: "Skala"}, title=f"Distribusi {col} (SPS)")
                st.plotly_chart(fig_scale_sps, use_container_width=True)

except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
except KeyError as e:
    st.error(f"Kolom tidak ditemukan: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
