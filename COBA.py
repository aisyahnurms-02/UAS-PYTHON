import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Crypto Aisyah", 
    layout="centered", 
    page_icon="💜"
)

# --- CUSTOM CSS (UNTUK TAMPILAN KARTU & GRADASI) ---
st.markdown("""
    <style>
    /* 1. Background Utama: Gradasi Ungu Gelap ke Putih */
    .stApp {
        background: rgb(34,0,56);
        background: linear-gradient(180deg, rgba(34,0,56,1) 0%, rgba(106,27,154,1) 45%, rgba(255,255,255,1) 100%);
        background-attachment: fixed;
    }

    /* 2. Mengubah Container Utama menjadi "Kartu Putih" di tengah */
    div[data-testid="block-container"] {
        background-color: #FFFFFF;
        padding: 3rem 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-top: 50px;
        max-width: 700px;
    }

    /* 3. Styling Judul */
    h1 {
        color: #333333;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Subjudul */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* 4. Styling Label Input */
    .stTextInput > label, .stTextArea > label {
        color: #333333 !important;
        font-weight: bold;
        font-size: 1rem;
    }

    /* 5. Tombol (Hijau & Biru) */
    /* Tombol Enkripsi (Primary - Hijau) */
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem 1rem;
        transition: 0.3s;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #218838;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Tombol Dekripsi/Reset (Secondary - Biru) */
    div.stButton > button[kind="secondary"] {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem 1rem;
        transition: 0.3s;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #0069d9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* 6. Kotak Hasil (Abu-abu dengan border dashed) */
    .result-label {
        font-weight: bold;
        color: #333;
        margin-top: 20px;
        margin-bottom: 5px;
    }
    .result-box {
        background-color: #E9ECEF;
        border: 2px dashed #CED4DA;
        border-radius: 8px;
        padding: 15px;
        color: #000;
        font-family: monospace;
        font-weight: bold;
        font-size: 1.1rem;
        min-height: 50px;
        word-wrap: break-word;
    }

    /* 7. Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4A148C; /* Ungu Footer */
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 1px;
        z-index: 9999;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI (CORE LOGIC) ---

def hitung_shift_key(judul_lagu, durasi_menit):
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    durasi_bersih = durasi_menit.replace(".", "")
    if not durasi_bersih.isdigit():
        return 0
    nilai_durasi = int(durasi_bersih)
    total = jumlah_huruf + nilai_durasi
    shift = total % 26
    return shift

def enkripsi_substitusi(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result += shifted_char
        else:
            result += char
    return result

def enkripsi_transposisi(text, key):
    if not key.isdigit():
        return text
    msg_len = float(len(text))
    key_lst = list(key)
    num_cols = len(key)
    num_rows = int(math.ceil(msg_len / num_cols))
    msg_lst = list(text)
    num_empty = (num_rows * num_cols) - len(msg_lst)
    msg_lst.extend(['_'] * num_empty)
    matrix = [msg_lst[i * num_cols: (i + 1) * num_cols] for i in range(num_rows)]
    ciphertext = ""
    key_with_index = sorted([(k, i) for i, k in enumerate(key_lst)])
    for _, k_index in key_with_index:
        for row in matrix:
            ciphertext += row[k_index]
    return ciphertext

def enkripsi_ekp(text):
    ekp_map = {
        'A': '@1', 'B': '&2*', 'C': '!3%', 'D': '^4$', 'E': '~5=',
        'F': '+6?', 'G': '<7>', 'H': '#8', 'I': '9!', 'J': '{1}0',
        'K': '1-1-', 'L': '`12~', 'M': ':1;3', 'N': '1,4<', 'O': 'Ø15',
        'P': '_1-6', 'Q': '1=7+', 'R': '1®8', 'S': '#1#9', 'T': '2@0@',
        'U': '2**1', 'V': '%2√2', 'W': '3&2∑', 'X': '2×4!!', 'Y': '^2¥5^', 'Z': '2Ω6$',
        ' ': '_', '_': '~'
    }
    hasil = ""
    for char in text:
        upper_char = char.upper()
        if upper_char in ekp_map:
            hasil += ekp_map[upper_char]
        else:
            hasil += char
    return hasil

# --- UI VISUAL ---

# Judul Utama
st.markdown("<h1>Kriptografi Aisyah</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Metode: Lagu Subtitusi + Transposisi + EKP</div>", unsafe_allow_html=True)

# Input Text Area
plaintext = st.text_area("Masukkan Teks (Plaintext/Ciphertext):", height=100)

# Input Kunci (Disusun rapi agar tidak memenuhi tempat)
st.markdown("<p style='font-weight:bold; margin-bottom:5px; color:#333;'>Konfigurasi Kunci:</p>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu", "Separuh Nafas")
with c2:
    durasi = st.text_input("Durasi (Ex: 4.14)", "4.14")
with c3:
    kunci_transposisi = st.text_input("Key Transpose", "3142")

st.markdown("<br>", unsafe_allow_html=True)

# Tombol
col_btn1, col_btn2 = st.columns(2)

hasil_akhir = "..."

with col_btn1:
    if st.button("Enkripsi", type="primary"):
        if plaintext and judul_lagu and durasi and kunci_transposisi:
            shift = hitung_shift_key(judul_lagu, durasi)
            tahap1 = enkripsi_substitusi(plaintext, shift)
            tahap2 = enkripsi_transposisi(tahap1, kunci_transposisi)
            hasil_akhir = enkripsi_ekp(tahap2)
            st.session_state['hasil'] = hasil_akhir
        else:
            st.error("Mohon lengkapi data")

with col_btn2:
    if st.button("Dekripsi / Reset", type="secondary"):
        st.session_state['hasil'] = "..."
        st.rerun()

# Menampilkan Hasil
if 'hasil' not in st.session_state:
    st.session_state['hasil'] = "..."

st.markdown("<div class='result-label'>Hasil:</div>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="result-box">
        {st.session_state['hasil']}
    </div>
""", unsafe_allow_html=True)

# Spacer
st.markdown("<br><br>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        create by Aisyah Nur Maya Silviyani
    </div>
""", unsafe_allow_html=True)
