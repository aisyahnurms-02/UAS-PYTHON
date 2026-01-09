import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kriptografi Aisyah", layout="centered", page_icon="💜")

# --- CUSTOM CSS (DIPERBAIKI UNTUK KETERBACAAN) ---
st.markdown("""
    <style>
    /* 1. Background Utama: Gradasi Ungu Gelap ke Putih */
    .stApp {
        background: linear-gradient(180deg, #2E003E 0%, #6A1B9A 50%, #FFFFFF 100%);
        background-attachment: fixed;
    }

    /* 2. Container "Kartu Putih" */
    div.block-container {
        background-color: #FFFFFF !important;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 700px;
        margin-top: 50px;
    }

    /* 3. PERBAIKAN TEKS (Memaksa warna gelap agar terbaca di latar putih) */
    h1 {
        color: #4A148C !important; /* Ungu Tua Gelap */
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: 900; /* Lebih tebal */
        margin-bottom: 5px;
        text-transform: uppercase; /* Huruf Kapital Semua */
    }
    
    p, label, .stMarkdown {
        color: #333333 !important; /* Abu-abu gelap untuk teks biasa */
    }

    /* 4. PERBAIKAN INPUT FIELD (Agar tidak hitam di dark mode) */
    .stTextInput input, .stTextArea textarea {
        background-color: #F8F9FA !important; /* Putih sedikit abu */
        color: #000000 !important; /* Teks Hitam Pekat */
        border: 1px solid #BA68C8 !important; /* Border Ungu */
    }
    
    /* Warna Label Input */
    div[data-testid="stMarkdownContainer"] p {
         color: #333333 !important;
    }

    /* 5. Tombol */
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white !important;
        border: none;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #007bff;
        color: white !important;
        border: none;
    }

    /* 6. Kotak Hasil */
    .result-box {
        background-color: #F3E5F5;
        border: 2px solid #8E24AA;
        border-radius: 10px;
        padding: 20px;
        color: #4A148C !important;
        font-family: monospace;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 20px;
        text-align: center;
    }

    /* 7. Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4A148C;
        color: white !important;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 999;
    }
    .footer p {
        color: white !important; /* Paksa teks footer putih */
        margin: 0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI (SAMA) ---

def hitung_shift_key(judul_lagu, durasi_menit):
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    durasi_bersih = durasi_menit.replace(".", "")
    if not durasi_bersih.isdigit():
        return 0, "Error"
    nilai_durasi = int(durasi_bersih)
    total = jumlah_huruf + nilai_durasi
    shift = total % 26
    penjelasan = f"(Huruf '{judul_lagu}' ({jumlah_huruf}) + Menit ({nilai_durasi})) mod 26 = {shift}"
    return shift, penjelasan

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
    if not key.isdigit(): return text
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

# 1. Judul Singkat & Jelas
st.markdown("<h1>KRIPTOGRAFI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.9em; opacity: 0.8;'>Metode Substitusi Lagu + Transposisi + Ekspansi Karakter</p>", unsafe_allow_html=True)

# 2. Input Plaintext
st.markdown("<b>Masukkan Teks (Plaintext):</b>", unsafe_allow_html=True)
plaintext = st.text_area("Label_Hidden", placeholder="Ketik pesan rahasia...", height=100, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# 3. Konfigurasi Kunci
st.markdown("<b>🔑 Konfigurasi Kunci</b>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<small>Judul Lagu</small>", unsafe_allow_html=True)
    judul_lagu = st.text_input("Lagu", "Separuh Nafas", label_visibility="collapsed")
with c2:
    st.markdown("<small>Durasi (Cth: 4.14)</small>", unsafe_allow_html=True)
    durasi = st.text_input("Durasi", "4.14", label_visibility="collapsed")
with c3:
    st.markdown("<small>Key Transposisi</small>", unsafe_allow_html=True)
    kunci_transposisi = st.text_input("Key", "3142", max_chars=4, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Tombol
col_btn1, col_btn2 = st.columns(2)
hasil_akhir = ""
detail_shift = ""
show_result = False

with col_btn1:
    if st.button("Enkripsi", key="btn_encrypt", type="primary"):
        if not plaintext or not judul_lagu or not durasi or not kunci_transposisi:
            st.error("Lengkapi semua data!")
        else:
            shift_val, detail_shift = hitung_shift_key(judul_lagu, durasi)
            step1 = enkripsi_substitusi(plaintext, shift_val)
            step2 = enkripsi_transposisi(step1, kunci_transposisi)
            hasil_akhir = enkripsi_ekp(step2)
            show_result = True

with col_btn2:
    if st.button("Dekripsi / Reset", key="btn_decrypt", type="secondary"):
        st.rerun()

# 5. Menampilkan Hasil
if show_result:
    st.markdown("---")
    st.markdown("<p style='text-align:center; font-weight:bold;'>HASIL ENKRIPSI:</p>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-box">
        {hasil_akhir}
    </div>
    """, unsafe_allow_html=True)

# Spacer
st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        <p>create by Aisyah Nur Maya Silviyani</p>
    </div>
""", unsafe_allow_html=True)
