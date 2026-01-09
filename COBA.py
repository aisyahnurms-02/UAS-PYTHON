import streamlit as st
import math

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Model Caesar Cipher",
    layout="centered",
    page_icon="💜"
)

# ================== CSS ==================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #2b003f 0%, #6a1b9a 55%, #f3e5f5 100%);
    background-attachment: fixed;
}

/* Card utama */
div[data-testid="block-container"] {
    background: linear-gradient(145deg, rgba(106,27,154,0.95), rgba(74,20,140,0.95));
    padding: 3rem;
    border-radius: 22px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.35);
    max-width: 720px;
    margin-top: 60px;
}

/* Judul */
h1 {
    text-align: center;
    color: white;
    font-weight: 700;
    margin-bottom: 1.8rem;
}

/* Label */
label {
    color: #f3e5f5 !important;
    font-weight: 600;
}

/* Input */
textarea, input {
    border-radius: 10px !important;
    border: none !important;
}

/* Tombol */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #8e24aa, #d500f9);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
    height: 45px;
    border: none;
}
div.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #1565c0, #1e88e5);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
    height: 45px;
    border: none;
}

/* Kotak gabungan */
.unified-box {
    background: rgba(255,255,255,0.18);
    border: 2px dashed rgba(255,255,255,0.6);
    border-radius: 14px;
    padding: 18px;
    color: #ffffff;
    font-family: monospace;
    line-height: 1.7;
    margin-top: 20px;
}
.unified-box .title {
    font-weight: bold;
    font-size: 1.1rem;
    margin-bottom: 10px;
    color: #ffeb3b;
}
.unified-box code {
    color: #ffd54f;
}

/* Hilangkan menu */
#MainMenu, footer, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ================== LOGIKA CAESAR ==================
def caesar_cipher(text, shift):
    hasil = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            hasil += chr((ord(char) - base + shift) % 26 + base)
        else:
            hasil += char
    return hasil

# ================== UI ==================
st.markdown("<h1>Model Caesar Cipher</h1>", unsafe_allow_html=True)

text = st.text_area(
    "Masukkan Teks (Plaintext / Ciphertext):",
    height=120
)

key = st.text_input(
    "Kunci Pergeseran (Key):",
    "12"
)

col1, col2 = st.columns(2)

if "hasil" not in st.session_state:
    st.session_state.hasil = ""

with col1:
    if st.button("Enkripsi", type="primary"):
        if text and key.isdigit():
            st.session_state.hasil = caesar_cipher(text, int(key))
        else:
            st.error("Masukkan teks dan key angka")

with col2:
    if st.button("Dekripsi", type="secondary"):
        if text and key.isdigit():
            st.session_state.hasil = caesar_cipher(text, -int(key))
        else:
            st.error("Masukkan teks dan key angka")

# ================== HASIL + FUNGSI (GABUNG) ==================
st.markdown(f"""
<div class="unified-box">
    <div class="title">Hasil Akhir</div>
    <code>{st.session_state.hasil}</code>

    <br><br>

    <div class="title">Tampilan Fungsi</div>

    <b>Input Teks:</b><br>
    <code>{text}</code><br><br>

    <b>Kunci (Shift):</b><br>
    <code>{key}</code><br><br>

    <b>Rumus Caesar Cipher:</b><br>
    <code>(x + key) mod 26</code><br><br>

    <b>Fungsi yang Digunakan:</b><br>
    <code>caesar_cipher(teks, key)</code>
</div>
""", unsafe_allow_html=True)
