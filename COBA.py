import streamlit as st
import math
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CryptoLab Custom EKP", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS (AGAR MIRIP GAMBAR REFERENSI) ---
st.markdown("""
    <style>
    /* 1. Background Gelap Utama */
    .stApp {
        background-color: #0E1117;
        color: #C9D1D9;
    }
    
    /* 2. Styling Input & Text Area (Mirip Terminal) */
    .stTextInput > div > div > input {
        background-color: #161B22; 
        color: #E6EDF3;
        border: 1px solid #30363D;
        border-radius: 6px;
    }
    .stTextArea > div > div > textarea {
        background-color: #161B22;
        color: #E6EDF3;
        border: 1px solid #30363D;
        border-radius: 6px;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    /* 3. Styling Tombol (Hijau & Biru) */
    div.stButton > button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.2s;
    }
    /* Tombol Enkripsi (Hijau) - Kita targetkan tombol pertama */
    div.row-widget.stButton:nth-of-type(1) button {
        background-color: #238636;
        color: white;
    }
    div.row-widget.stButton:nth-of-type(1) button:hover {
        background-color: #2EA043;
    }

    /* 4. Kotak Hasil (Output Terminal Style) */
    .output-box {
        background-color: #0D1117;
        border: 1px solid #30363D;
        border-radius: 6px;
        padding: 15px;
        color: #28A745; /* Warna hijau hacker */
        font-family: 'Consolas', monospace;
        height: 250px;
        overflow-y: auto;
        font-size: 14px;
        box-shadow: inset 0 0 10px #000000;
    }

    /* 5. Header Section */
    .header-style {
        font-size: 24px;
        font-weight: bold;
        color: #58A6FF;
        margin-bottom: 10px;
        border-bottom: 1px solid #30363D;
        padding-bottom: 10px;
    }

    /* 6. Label Input */
    label {
        color: #8B949E !important;
        font-size: 12px !important;
        font-weight: bold;
    }
    
    /* 7. Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #161B22;
        color: #8B949E;
        text-align: center;
        padding: 8px;
        font-size: 12px;
        border-top: 1px solid #30363D;
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI (SAMA) ---
def hitung_shift_key(judul_lagu, durasi_menit):
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    durasi_bersih = durasi_menit.replace(".", "")
    if not durasi_bersih.isdigit(): return 0
    nilai_durasi = int(durasi_bersih)
    return (jumlah_huruf + nilai_durasi) % 26

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
    if not key.isdigit(): return text
    msg_len = float(len(text))
    key_lst = list(key)
    num_cols = len(key)
    num_rows = int(math.ceil(msg_len / num_cols))
    msg_lst = list(text)
    msg_lst.extend(['_'] * ((num_rows * num_cols) - len(msg_lst)))
    
    matrix = [msg_lst[i * num_cols: (i + 1) * num_cols] for i in range(num_rows)]
    ciphertext = ""
    key_with_index = sorted([(k, i) for i, k in enumerate(key_lst)])
    for _, k_index in key_with_index:
        for row in matrix:
            ciphertext += row[k_index]
    return ciphertext

def enkripsi_ekp(text):
    # Mapping Simbol EKP
    ekp_map = {
        'A': '∆', 'B': 'ß', 'C': '©', 'D': '∂', 'E': '€',
        'F': 'ƒ', 'G': '6', 'H': '#', 'I': '!', 'J': '¿',
        'K': 'x', 'L': '£', 'M': 'µ', 'N': 'π', 'O': 'Ø',
        'P': '¶', 'Q': '9', 'R': '®', 'S': '$', 'T': '†',
        'U': 'µ', 'V': '√', 'W': '∑', 'X': '×', 'Y': '¥', 'Z': 'Ω',
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

# --- UI LAYOUT ---

# Header mirip gambar
st.markdown('<div class="header-style">🛡️ CryptoLab Model v1 <span style="font-size:12px; background:#238636; color:white; padding:2px 6px; border-radius:4px; vertical-align:middle;">Aman</span></div>', unsafe_allow_html=True)

# Tab Bar Buatan (Visual Only)
st.markdown("""
<div style="display:flex; gap:20px; border-bottom:1px solid #30363D; margin-bottom:20px; color:#8B949E; font-size:14px;">
    <div style="color:#58A6FF; border-bottom:2px solid #58A6FF; padding-bottom:5px; cursor:pointer;">Custom EKP (Subst+Transp)</div>
    <div style="cursor:pointer;">Simetris (AES)</div>
    <div style="cursor:pointer;">Asimetris (RSA)</div>
</div>
""", unsafe_allow_html=True)

# Layout 2 Kolom Utama
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Input Data (Plaintext)")
    plaintext = st.text_area("Masukkan pesan rahasia di sini...", height=150, value="Ini adalah pesan rahasia yang akan dienkripsi.")
    
    st.markdown("### 2. Konfigurasi Algoritma")
    
    # Membuat 3 kolom kecil untuk konfigurasi agar rapi
    c1, c2, c3 = st.columns(3)
    with c1:
        judul_lagu = st.text_input("Judul Lagu", "Separuh Nafas")
    with c2:
        durasi = st.text_input("Durasi", "4.14")
    with c3:
        key_trans = st.text_input("Key Transposisi", "3142")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tombol Aksi
    # Kita gunakan kolom lagi agar tombolnya lebar penuh
    b1, b2 = st.columns(2)
    with b1:
        tombol_enkripsi = st.button("ENKRIPSI")
    with b2:
        st.button("DEKRIPSI (Coming Soon)") # Placeholder sesuai gambar

# Variabel untuk menampung hasil
final_output = ""
log_text = "Menunggu proses..."

if tombol_enkripsi:
    start_time = time.time()
    
    # Proses Enkripsi
    s_val = hitung_shift_key(judul_lagu, durasi)
    step1 = enkripsi_substitusi(plaintext, s_val)
    step2 = enkripsi_transposisi(step1, key_trans)
    final_output = enkripsi_ekp(step2)
    
    end_time = time.time()
    durasi_proses = end_time - start_time
    
    log_text = f"Waktu proses: {durasi_proses:.4f}s | Ukuran output: {len(final_output)} bytes"

with col2:
    st.markdown("### 3. Hasil (Ciphertext)")
    
    # Tampilan Output seperti Terminal Code di gambar
    # Jika belum ada hasil, tampilkan placeholder
    display_text = final_output if final_output else "Hasil enkripsi akan muncul di sini..."
    
    st.markdown(f"""
        <div class="output-box">
            {display_text}
        </div>
    """, unsafe_allow_html=True)
    
    # Tombol kecil di bawah output
    st.markdown("""
    <div style="display:flex; justify-content:space-between; margin-top:10px;">
        <button style="background:transparent; border:1px solid #30363D; color:#C9D1D9; padding:5px 10px; border-radius:4px; cursor:pointer;">📋 Copy ke Clipboard</button>
        <button style="background:transparent; border:1px solid #30363D; color:#C9D1D9; padding:5px 10px; border-radius:4px; cursor:pointer;">⬇️ Download</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 4. Log / Metadata")
    st.info(log_text)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        create by Aisyah Nur Maya Silviyani
    </div>
""", unsafe_allow_html=True)
