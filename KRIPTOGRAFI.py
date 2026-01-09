import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Crypto Aisyah - Purple Edition", 
    layout="centered", 
    page_icon="💜"
)

# --- CUSTOM CSS (TAMPILAN SERBA UNGU) ---
st.markdown("""
    <style>
    /* 1. Background Halaman: Gradasi Ungu Gelap ke Putih (Sesuai gambar) */
    .stApp {
        background: rgb(68,10,103);
        background: linear-gradient(180deg, rgba(68,10,103,1) 0%, rgba(180,135,255,1) 80%, rgba(255,255,255,1) 100%);
        background-attachment: fixed;
    }

    /* 2. Kartu Utama: Ungu Gradasi (Sesuai gambar) */
    div[data-testid="block-container"] {
        background: linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%);
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
        margin-top: 50px;
        max-width: 700px;
    }

    /* 3. Semua Teks Menjadi PUTIH (Agar terbaca di background ungu) */
    h1, h2, h3, p, div, label, span {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* 4. Input Fields: Putih Bersih dengan Teks Hitam */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 8px;
        border: none;
    }
    /* Warna Label Input */
    .stTextInput > label, .stTextArea > label {
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 8px;
    }

    /* 5. Tombol */
    /* Tombol Enkripsi (Kiri): Ungu Neon/Magenta */
    div.stButton > button[kind="primary"] {
        background-color: #D500F9 !important; /* Magenta terang */
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem;
        font-size: 16px;
    }
    
    /* Tombol Dekripsi (Kanan): Biru Tua (Navy) */
    div.stButton > button[kind="secondary"] {
        background-color: #0D47A1 !important; /* Biru Tua */
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem;
        font-size: 16px;
    }

    /* 6. Kotak Hasil: Transparan dengan Border Putus-putus (Sesuai gambar) */
    .result-box {
        background-color: rgba(255, 255, 255, 0.2); /* Transparan putih */
        border: 2px dashed rgba(255, 255, 255, 0.6);
        border-radius: 10px;
        padding: 15px;
        color: #FFFFFF;
        font-family: monospace;
        font-weight: bold;
        font-size: 1.2rem;
        min-height: 60px;
        margin-top: 5px;
    }
    
    /* Footer Style */
    .credit-text {
        text-align: center;
        color: rgba(255,255,255,0.7) !important;
        font-size: 12px;
        margin-top: 30px;
        font-style: italic;
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA PROGRAM (TETAP SAMA) ---

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

# Judul
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Kriptografi Aisyah</h1>", unsafe_allow_html=True)

# Input Text
plaintext = st.text_area("Masukkan Teks (Plaintext/Ciphertext):", height=100)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<label>Konfigurasi Kunci:</label>", unsafe_allow_html=True)

# Input Kunci (Disusun Berjajar 3 agar rapi seperti kolom input tunggal)
c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu", "Separuh Nafas")
with c2:
    durasi = st.text_input("Durasi (Ex: 4.14)", "4.14")
with c3:
    kunci_transposisi = st.text_input("Key Transpose", "3142")

st.markdown("<br>", unsafe_allow_html=True)

# Tombol Action (Warna disesuaikan CSS)
col_btn1, col_btn2 = st.columns(2)

# Session State
if 'hasil_ungu' not in st.session_state:
    st.session_state['hasil_ungu'] = ""

with col_btn1:
    # Tombol Enkripsi (Magenta)
    if st.button("Enkripsi", type="primary"):
        if plaintext and judul_lagu and durasi and kunci_transposisi:
            shift = hitung_shift_key(judul_lagu, durasi)
            t1 = enkripsi_substitusi(plaintext, shift)
            t2 = enkripsi_transposisi(t1, kunci_transposisi)
            st.session_state['hasil_ungu'] = enkripsi_ekp(t2)
        else:
            st.warning("Data belum lengkap!")

with col_btn2:
    # Tombol Dekripsi/Reset (Biru Tua)
    if st.button("Dekripsi / Reset", type="secondary"):
        st.session_state['hasil_ungu'] = ""
        st.rerun()

# Output Box
st.markdown("<label style='margin-top: 20px; display:block;'>Hasil:</label>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="result-box">
        {st.session_state['hasil_ungu']}
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="credit-text">
        create by Aisyah Nur Maya Silviyani
    </div>
""", unsafe_allow_html=True)
