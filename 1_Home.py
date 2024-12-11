import streamlit as st

# Set title of the app
st.title("Halaman Home")

# Add a subtitle
st.subheader("Selamat datang di aplikasi Streamlit!")

# Menambahkan teks penjelasan
st.write("""
    Ini adalah contoh halaman home yang dapat Anda sesuaikan dengan kebutuhan proyek Anda.
    Streamlit memungkinkan Anda untuk membuat aplikasi web interaktif dengan cepat.
""")

# Menambahkan tombol
if st.button('Klik Saya'):
    st.write("Tombol telah diklik!")

# Menambahkan input teks
name = st.text_input("Masukkan nama Anda:")
if name:
    st.write(f"Hello, {name}!")

# Menambahkan gambar (misalnya gambar logo atau gambar terkait)
st.image('https://upload.wikimedia.org/wikipedia/commons/1/1b/Streamlit_logo.png', caption='Streamlit Logo')

# Menambahkan footer
st.markdown("---")
st.write("Aplikasi ini dibangun menggunakan Streamlit.")
