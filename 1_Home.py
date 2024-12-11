import streamlit as st

def main():
    # Konfigurasi halaman
    st.set_page_config(page_title="Dashboard Home", page_icon="🏢", layout="wide")

    # Header Halaman
    st.title("Selamat Datang di Dashboard")
    st.subheader("Visualisasi dan Analisis Data Anda dalam Satu Tempat")

    # Gambar atau Logo
    st.image("https://via.placeholder.com/800x300", caption="Dashboard Home", use_column_width=True)

    # Konten Utama
    st.markdown(
        """
        ### Apa yang Bisa Anda Lakukan?
        - **Pantau data Anda** secara real-time
        - **Visualisasikan tren dan pola** untuk wawasan yang lebih baik
        - **Analisis mendalam** dengan alat analitik interaktif
        
        Dashboard ini dirancang untuk mempermudah pengambilan keputusan berdasarkan data yang akurat dan terpercaya.
        """
    )

    # Kolom untuk Menampilkan Info Tambahan
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            #### Fitur Utama
            - Dashboard interaktif
            - Filter data fleksibel
            - Ekspor laporan
            """
        )

    with col2:
        st.markdown(
            """
            #### Kontak Kami
            Jika Anda memiliki pertanyaan atau memerlukan bantuan, silakan hubungi kami:
            - Email: support@example.com
            - Telepon: +62 123 4567 890
            """
        )

    # Footer
    st.write("---")
    st.markdown(
        "Terima kasih telah menggunakan dashboard kami! Jangan ragu untuk menjelajahi fitur-fitur yang tersedia."
    )

if __name__ == "__main__":
    main()
