import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Crypto Aisyah",
    layout="centered",
    page_icon="💜"
)

# --- CUSTOM CSS (TEMA GELAP / CRYPTO) ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #020617 0%, #020617 100%);
    color: #e5e7eb;
}

/* Card utama */
div[data-testid="block-container"] {
    background-color: #020617;
    padding: 3rem;
    border-radius: 18px;
    box-shadow: 0 0 30px rgba(37,99,235,0.25);
    margin-top: 40px;
    max-width: 720px;
}

/* Judul */
h1 {
    color: #60a5fa;
    text-align: center;
    font-weight: 800;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 2rem;
}

/* Label input */
label {
    color: #e5e7eb !important;
    font-weight: 600;
}

/* Input */
textarea, input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border: 1px solid #334155 !important;
    border-radius: 6px;
}

/* Tombol */
div.stButton > button[kind="primary"] {
    background: #2563eb;
    color: white;
    font-weight: bold;
    width: 100%;
}
div.stButton > button[kind="primary"]:hover {
    background: #1d4ed8;
}

div.stButton > button[kind="secondary"] {
    background: #334155;
    color: white;
    font-weight: bold;
    width: 100%;
}
div.stButton > button[kind="secondary"]:hover {
    background: #475569;
}

/* Hasil */
.result-label {
    font-weight: bold;
    color: #93c5fd;
    margin-top: 25px;
}

.result-box {
    background-color: #000000;
    border: 1px solid #22c55e;
    border-radius: 10px;
    padding: 16px;
    color: #22c55e;
    font-family: monospace;
    font-size: 1.05rem;
    min-height: 60px;
    word-wrap: break-word;
}

/* Footer */
.credit-text {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 25px;
}

/* Hilangkan menu bawaan */
#MainMenu, footer, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI (TIDAK DIUBAH) ---

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

st.markdown("<h1>Kriptografi Aisyah</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Substitusi • Transposisi • EKP</div>", unsafe_allow_html=True)

plaintext = st.text_area("Masukkan Teks", height=100)

c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu", "Separuh Nafas")
with c2:
    durasi = st.text_input("Durasi (4.14)", "4.14")
with c3:
    kunci_transposisi = st.text_input("Key Transpose", "3142")

if "hasil" not in st.session_state:
    st.session_state["hasil"] = "..."

col1, col2 = st.columns(2)
with col1:
    if st.button("Enkripsi", type="primary"):
        shift = hitung_shift_key(judul_lagu, durasi)
        t1 = enkripsi_substitusi(plaintext, shift)
        t2 = enkripsi_transposisi(t1, kunci_transposisi)
        st.session_state["hasil"] = enkripsi_ekp(t2)

with col2:
    if st.button("Reset", type="secondary"):
        st.session_state["hasil"] = "..."
        st.rerun()

st.markdown("<div class='result-label'>Hasil Ciphertext</div>", unsafe_allow_html=True)
st.markdown(f"<div class='result-box'>{st.session_state['hasil']}</div>", unsafe_allow_html=True)

st.markdown("<div class='credit-text'>create by Aisyah Nur Maya Silviyani</div>", unsafe_allow_html=True)
