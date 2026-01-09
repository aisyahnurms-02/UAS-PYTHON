import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Crypto Aisyah 💖",
    layout="centered",
    page_icon="🌸"
)

# --- CUSTOM CSS TEMA KIYUT ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fce7f3 0%, #e9d5ff 100%);
}

/* Card utama */
div[data-testid="block-container"] {
    background-color: #ffffff;
    padding: 3rem;
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(236,72,153,0.25);
    margin-top: 40px;
    max-width: 720px;
}

/* Judul */
h1 {
    color: #db2777;
    text-align: center;
    font-weight: 800;
    font-family: 'Segoe UI', sans-serif;
}

.subtitle {
    text-align: center;
    color: #9333ea;
    margin-bottom: 2rem;
    font-size: 0.95rem;
}

/* Label */
label {
    color: #7c2d12 !important;
    font-weight: 600;
}

/* Input */
textarea, input {
    background-color: #fff1f2 !important;
    color: #831843 !important;
    border: 2px solid #f9a8d4 !important;
    border-radius: 12px !important;
}

/* Tombol */
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #ec4899, #d946ef);
    color: white;
    font-weight: bold;
    border-radius: 14px;
    width: 100%;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #db2777, #c026d3);
}

div.stButton > button[kind="secondary"] {
    background: #fbcfe8;
    color: #831843;
    font-weight: bold;
    border-radius: 14px;
    width: 100%;
}
div.stButton > button[kind="secondary"]:hover {
    background: #f9a8d4;
}

/* Hasil */
.result-label {
    font-weight: bold;
    color: #be185d;
    margin-top: 25px;
}

.result-box {
    background-color: #fff1f2;
    border: 2px dashed #f472b6;
    border-radius: 18px;
    padding: 16px;
    color: #9d174d;
    font-family: monospace;
    font-size: 1.05rem;
    min-height: 60px;
    word-wrap: break-word;
}

/* Footer */
.credit-text {
    text-align: center;
    color: #a855f7;
    font-size: 12px;
    margin-top: 25px;
    font-style: italic;
}

/* Hilangkan menu bawaan */
#MainMenu, footer, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI (TETAP SAMA) ---

def hitung_shift_key(judul_lagu, durasi_menit):
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    durasi_bersih = durasi_menit.replace(".", "")
    if not durasi_bersih.isdigit():
        return 0
    return (jumlah_huruf + int(durasi_bersih)) % 26

def enkripsi_substitusi(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def enkripsi_transposisi(text, key):
    if not key.isdigit():
        return text
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)
    padded = list(text.ljust(num_rows * num_cols, '_'))
    matrix = [padded[i*num_cols:(i+1)*num_cols] for i in range(num_rows)]
    result = ""
    for _, idx in sorted((k, i) for i, k in enumerate(key)):
        for row in matrix:
            result += row[idx]
    return result

def enkripsi_ekp(text):
    ekp_map = {
        'A': '@1','B': '&2*','C': '!3%','D': '^4$','E': '~5=',
        'F': '+6?','G': '<7>','H': '#8','I': '9!','J': '{1}0',
        'K': '1-1-','L': '`12~','M': ':1;3','N': '1,4<',
        'O': 'Ø15','P': '_1-6','Q': '1=7+','R': '1®8',
        'S': '#1#9','T': '2@0@','U': '2**1','V': '%2√2',
        'W': '3&2∑','X': '2×4!!','Y': '^2¥5^','Z': '2Ω6$',
        ' ': '_','_': '~'
    }
    return "".join(ekp_map.get(c.upper(), c) for c in text)

# --- UI ---

st.markdown("<h1>🌸 Kriptografi Aisyah 🌸</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Substitusi • Transposisi • EKP (versi kiyut)</div>", unsafe_allow_html=True)

plaintext = st.text_area("Masukkan Teks 💌", height=100)

c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu 🎵", "Separuh Nafas")
with c2:
    durasi = st.text_input("Durasi ⏱️ (4.14)", "4.14")
with c3:
    kunci_transposisi = st.text_input("Key Transpose 🔑", "3142")

if "hasil" not in st.session_state:
    st.session_state["hasil"] = "✨ hasil akan muncul di sini ✨"

col1, col2 = st.columns(2)
with col1:
    if st.button("💖 Enkripsi"):
        shift = hitung_shift_key(judul_lagu, durasi)
        t1 = enkripsi_substitusi(plaintext, shift)
        t2 = enkripsi_transposisi(t1, kunci_transposisi)
        st.session_state["hasil"] = enkripsi_ekp(t2)

with col2:
    if st.button("🧼 Reset"):
        st.session_state["hasil"] = "✨ hasil akan muncul di sini ✨"
        st.rerun()

st.markdown("<div class='result-label'>🎀 Hasil Ciphertext 🎀</div>", unsafe_allow_html=True)
st.markdown(f"<div class='result-box'>{st.session_state['hasil']}</div>", unsafe_allow_html=True)

st.markdown("<div class='credit-text'>create by Aisyah Nur Maya Silviyani 💕</div>", unsafe_allow_html=True)
