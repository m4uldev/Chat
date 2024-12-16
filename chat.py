import re
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json
import os

SETTINGS_FILE = "user.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {} 

settings = load_settings()

language = settings.get("language", "Indonesia")
username = settings.get("username", "user")

st.title("Maulid AI")
genai.configure(api_key="AIzaSyC3rzL9U4ccMg5k9XpL9M8Hou-2ZVCXhk0")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

with st.chat_message("ai"):
    st.caption("MaulidAI")
    st.write("Hai, nama saya MaulidAI. Aku adalah kecerdasan buatan yang diciptakan oleh Maulid. Aku siap untuk melayani anda.")

if 'data_input' not in st.session_state:
    st.session_state.data_input = []

def tampilkan_pesan():
    for pengirim, pesan in st.session_state.data_input:
        with st.chat_message(pengirim):
            st.caption(f"{username}" if pengirim == f"user" else "Maulid AI")
            st.write(pesan)

chat_saya = st.chat_input("Ketik pesan")

def is_url(text):
    url_pattern = re.compile(
        r'^(https?://)?'                   
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'   
        r'(:\d+)?'                         
        r'(/[\w\-./?%&=]*)?'               
    )
    return bool(url_pattern.match(text))

# Header User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

if chat_saya:
    # Menambahkan instruksi untuk menjawab dalam bahasa Indonesia
    instruksi_bahasa = f"Jawab dalam bahasa {language}."
    
    # Memisahkan input menjadi URL dan teks
    validasi_pola_string = [part.strip() for part in chat_saya.split(",")]
    urls = []
    teks = []
    for part in validasi_pola_string:
        if is_url(part):
            urls.append(part)
        else:
            teks.append(part)

    # Jika ada URL dan teks
    if urls and teks:
        for url in urls:
            # Menambahkan User-Agent pada request
            response_from_url = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response_from_url.text, "html.parser")
            p_texts = [tag.get_text(strip=True) for tag in soup.find_all("p")]

        perintah_lengkap = " ".join(p_texts + teks)
        perintah_lengkap_dengan_instruksi = f"{instruksi_bahasa} {perintah_lengkap}"  # Sisipkan perintah bahasa
        response = st.session_state.chat_session.send_message(perintah_lengkap_dengan_instruksi)

        st.session_state.data_input.append(("user", chat_saya))
        st.session_state.data_input.append(("ai", response.text))
        tampilkan_pesan()

    # Jika hanya ada URL
    elif urls and not teks:
        for url in urls:
            # Menambahkan User-Agent pada request
            response_from_url = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response_from_url.text, "html.parser")
            p_texts = [tag.get_text(strip=True) for tag in soup.find_all("p")]

        perintah_lengkap = " ".join(p_texts)
        perintah_lengkap_dengan_instruksi = f"{instruksi_bahasa} {perintah_lengkap}"  # Sisipkan perintah bahasa
        response = st.session_state.chat_session.send_message(perintah_lengkap_dengan_instruksi)

        st.session_state.data_input.append(("user", chat_saya))
        st.session_state.data_input.append(("ai", response.text))
        tampilkan_pesan()

    # Jika hanya ada teks
    elif not urls and teks:
        perintah_lengkap = " ".join(teks)
        perintah_lengkap_dengan_instruksi = f"{instruksi_bahasa} {perintah_lengkap}"  # Sisipkan perintah bahasa
        response = st.session_state.chat_session.send_message(perintah_lengkap_dengan_instruksi)

        st.session_state.data_input.append(("user", chat_saya))
        st.session_state.data_input.append(("ai", response.text))
        tampilkan_pesan()
else:
    tampilkan_pesan()

