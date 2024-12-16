import streamlit as st
import json
import os

# Nama file JSON untuk menyimpan pengaturan
SETTINGS_FILE = "user.json"

# Fungsi untuk membaca pengaturan dari file JSON
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {}  # Jika file tidak ada, kembalikan dictionary kosong

# Fungsi untuk menyimpan pengaturan ke file JSON
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

# Load pengaturan saat aplikasi dimulai
settings = load_settings()

# Sidebar atau header untuk pengaturan
st.title("Pengaturan Aplikasi")

# Ambil nilai dari pengaturan atau gunakan default
language = st.selectbox("Pilih Bahasa :", ["Indonesia", "Inggris"], index=["Indonesia", "Inggris"].index(settings.get("language", "Light")))
username = st.text_input("Nama Pengguna", value=settings.get("username", "User"))

# Tampilkan pengaturan saat ini
st.write(f"Pengaturan Anda saat ini:")
st.write(f"- Tema: {language}")
st.write(f"- Nama Pengguna: {username}")


# Tombol untuk menyimpan pengaturan
if st.button("Simpan Pengaturan"):
    settings = {
        "language": language,
        "username": username,
        
    }
    save_settings(settings)
    st.success("Pengaturan berhasil disimpan!")

