import streamlit as st
import math

# --- 1. CONFIG ---
st.set_page_config(page_title="Kriptografi", layout="centered")

# --- 2. CSS (WARNA KOTAK & TEKS DIPERBAIKI) ---
st.markdown("""
    <style>
    /* Background Ungu */
    .stApp {
        background: linear-gradient(180deg, #4b0082 0%, #2e004f 100%);
    }

    /* LABEL / TULISAN JUDUL (Supaya kelihatan di background ungu) */
    h1, h2, h3, p, label, .stMarkdown, span {
        color: #e0e0e0 !important; /* Putih agak abu dikit biar gak sakit mata */
    }
    
    /* JUDUL UTAMA (Ungu Gelap dikit/Hitam sesuai request gambar, tapi dikasih shadow biar baca) */
    h1 {
        color: #1a1a1a !important; 
        text-shadow: 0px 0px 10px rgba(255,255,255,0.3);
    }

    /* KOTAK INPUT (TEXTAREA & INPUT BIASA) -> JADI PUTIH, TULISAN HITAM */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important; /* Kotak Putih */
        color: #000000 !important; /* Tulisan Hitam Pekat */
        border: 1px solid #ccc !important;
        border-radius: 8px;
    }
    
    /* TOMBOL (HITAM SESUAI GAMBAR) */
    div.stButton > button {
        background-color: #1a1a1a !important; /* Hitam */
        color: #ffffff !important; /* Tulisan Putih */
        border: none;
        height: 45px;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #333333 !important; /* Abu gelap pas hover */
    }

    /* HASIL BOX (Gelap transparan) */
    code {
        background-color: #1a1a1a !important;
        color: #00ff00 !important; /* Hasil warna hijau terminal */
        font-family: monospace;
    }
    
    /* Footer & Header hide */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA (TIDAK DIUBAH) ---

def get_shift_value(judul, durasi):
    judul_clean = ''.join(filter(str.isalpha, judul))
    len_judul = len(judul_clean)
    durasi_clean = durasi.replace(".", "").replace(":", "")
    try:
        val_durasi = int(durasi_clean)
    except ValueError:
        val_durasi = 0
    return (len_judul + val_durasi) % 26

def substitution_cipher(text, shift, encrypt=True):
    result = ""
    if not encrypt: shift = -shift
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def transposition_cipher(text, key_str, encrypt=True):
    if not key_str.isdigit(): return text
    key_str = key_str[:4]
    key = [int(k) for k in key_str]
    num_cols = len(key)
    if num_cols == 0: return text
    
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    if encrypt:
        num_rows = math.ceil(len(text) / num_cols)
        padded_text = text.ljust(num_rows * num_cols, '_')
        grid = [list(padded_text[r*num_cols : (r+1)*num_cols]) for r in range(num_rows)]
        cipher = ""
        for col_idx in key_order:
            for row in range(num_rows):
                cipher += grid[row][col_idx]
        return cipher.replace('_', '')
    else:
        num_rows = math.ceil(len(text) / num_cols)
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        idx = 0
        for k_idx in key_order:
            for r in range(num_rows):
                if idx < len(text):
                    grid[r][k_idx] = text[idx]
                    idx += 1
        plain = ""
        for r in range(num_rows):
            for c in range(num_cols):
                plain += grid[r][c]
        return plain.rstrip('_')

def ekp_cipher(text, encrypt=True):
    ekp_map = {
        'A': '@1', 'B': '&2*', 'C': '!3%', 'D': '^4$', 'E': '~5=',
        'F': '+6?', 'G': '<7>', 'H': '#8', 'I': '9!', 'J': '{1}0',
        'K': '1-1-', 'L': '`12~', 'M': ':1;3', 'N': '1,4<', 'O': 'Ø15',
        'P': '_1-6', 'Q': '1=7+', 'R': '1®8', 'S': '#1#9', 'T': '2@0@',
        'U': '2**1', 'V': '%2√2', 'W': '3&2∑', 'X': '2×4!!', 'Y': '^2¥5^', 'Z': '2Ω6$',
        ' ': '_', '_': '~'
    }
    
    if encrypt:
        hasil = ""
        for char in text:
            upper_char = char.upper()
            if upper_char in ekp_map:
                hasil += ekp_map[upper_char]
            else:
                hasil += char
        return hasil
    else:
        reverse_map = {v: k for k, v in ekp_map.items()}
        sorted_symbols = sorted(reverse_map.keys(), key=len, reverse=True)
        hasil = ""
        i = 0
        while i < len(text):
            match = False
            for sym in sorted_symbols:
                if text.startswith(sym, i):
                    hasil += reverse_map[sym]
                    i += len(sym)
                    match = True
                    break
            if not match:
                hasil += text[i]
                i += 1
        return hasil

# --- 4. TAMPILAN (LAYOUT) ---

st.markdown("<h1 style='text-align: center;'>ALGORITMA KREASI</h1>", unsafe_allow_html=True)

st.write("Masukkan Teks:")
input_text = st.text_area("", height=100, label_visibility="collapsed")

st.write("Konfigurasi Kunci:")
c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu", placeholder="Judul")
with c2:
    durasi_lagu = st.text_input("Durasi", placeholder="Cth: 3.12")
with c3:
    key_trans = st.text_input("Key Transposisi", placeholder="1725")

st.write("") # Spasi

# Tombol
col_l, col_btn1, col_btn2, col_r = st.columns([0.1, 1, 1, 0.1])
with col_btn1:
    enc_btn = st.button("ENKRIPSI", use_container_width=True)
with col_btn2:
    dec_btn = st.button("DEKRIPSI / RESET", use_container_width=True)

# Proses
result = ""
if enc_btn and input_text and judul_lagu and durasi_lagu and key_trans:
    s1 = substitution_cipher(input_text, get_shift_value(judul_lagu, durasi_lagu), True)
    s2 = transposition_cipher(s1, key_trans, True)
    result = ekp_cipher(s2, True)
    st.success("Enkripsi Berhasil")

elif dec_btn and input_text and judul_lagu and durasi_lagu and key_trans:
    s1 = ekp_cipher(input_text, False)
    s2 = transposition_cipher(s1, key_trans, False)
    result = substitution_cipher(s2, get_shift_value(judul_lagu, durasi_lagu), False)
    # Hack alert box color manually via markdown if needed, but standard st.info is mostly ok
    st.info("Dekripsi Berhasil")

if result:
    st.write("Hasil:")
    st.code(result)
    
    # Credit
    st.markdown("<div style='text-align: center; color: #888; font-size: 12px; margin-top: 20px;'>create by Aisyah Nur Maya Silviyani</div>", unsafe_allow_html=True)
