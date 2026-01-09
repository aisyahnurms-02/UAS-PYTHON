import streamlit as st
import math

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kriptografi",
    layout="centered" # Penting agar posisi default di tengah
)

# --- 2. CSS "CARD UI" (Kotak Besar di Tengah) ---
st.markdown("""
    <style>
    /* 1. Background Halaman Utama (Luar Kotak) - Tetap Ungu */
    .stApp {
        background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%);
        background-attachment: fixed;
    }

    /* 2. Mengatur Container Utama menjadi "KOTAK BESAR" (Card) */
    div.block-container {
        background-color: rgba(255, 255, 255, 0.95); /* Putih sedikit transparan */
        padding: 3rem;       /* Jarak dalam kotak */
        border-radius: 25px; /* Sudut membulat */
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); /* Bayangan hitam di belakang kotak */
        max-width: 700px;    /* Lebar maksimal kotak agar terlihat rapi */
        margin-top: 2rem;
    }

    /* 3. Memastikan SEMUA TEKS di dalam kotak berwarna HITAM/GELAP */
    h1, h2, h3, h4, h5, p, label, div, span, .stMarkdown {
        color: #333333 !important;
    }
    
    /* Judul Utama */
    h1 {
        text-align: center;
        font-weight: 800;
        color: #4b0082 !important; /* Ungu gelap */
        margin-bottom: 30px;
        text-shadow: none; /* Hapus shadow jika ada sisa */
    }

    /* 4. Styling Input Fields (Agar border jelas) */
    .stTextInput input, .stTextArea textarea {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 2px solid #d1d1d1 !important;
        border-radius: 10px;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4b0082 !important; /* Border ungu saat diklik */
    }
    
    /* 5. Styling Tombol */
    /* Tombol Enkripsi (Kiri) */
    div[data-testid="column"]:nth-of-type(2) button {
        background-color: #aa00ff !important; /* Ungu Neon */
        color: white !important;
        border: none;
        height: 50px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* Tombol Dekripsi (Kanan) */
    div[data-testid="column"]:nth-of-type(3) button {
        background-color: #004ba0 !important; /* Biru Gelap */
        color: white !important;
        border: none;
        height: 50px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* 6. Styling Kotak Hasil */
    code {
        color: #d63384 !important; /* Warna teks hasil pink/ungu */
        background-color: #f1f1f1 !important; /* Background hasil abu terang */
        font-weight: bold;
        border: 1px dashed #4b0082;
    }
    
    /* Sembunyikan elemen bawaan */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA KRIPTOGRAFI ---

def get_shift_value(judul, durasi):
    judul_clean = ''.join(filter(str.isalpha, judul))
    len_judul = len(judul_clean)
    durasi_clean = durasi.replace(".", "").replace(":", "")
    try:
        val_durasi = int(durasi_clean)
    except ValueError:
        val_durasi = 0
    total = len_judul + val_durasi
    shift = total % 26
    return shift

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
        grid = []
        for r in range(num_rows):
            grid.append(list(padded_text[r*num_cols : (r+1)*num_cols]))
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

# --- 4. TAMPILAN UTAMA (UI) ---

st.title("ALGORITMA KREASI")

# Input Utama
st.markdown("### Masukkan Teks (Plaintext/Ciphertext):")
input_text = st.text_area("", height=100, placeholder="Ketik amikom...", label_visibility="collapsed")

# Konfigurasi
st.markdown("### Konfigurasi Kunci:")
c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu", placeholder="Separuh Nafas")
with c2:
    durasi_lagu = st.text_input("Durasi", placeholder="4.14")
with c3:
    key_trans = st.text_input("Key Transposisi", placeholder="1234", max_chars=4)

st.write("") # Spacer

# Tombol
col_l, btn_enc, btn_dec, col_r = st.columns([0.1, 2, 2, 0.1])
with btn_enc:
    do_encrypt = st.button("Enkripsi", use_container_width=True)
with btn_dec:
    do_decrypt = st.button("Dekripsi", use_container_width=True)

# Logika
final_res = ""
status_msg = ""

if do_encrypt and input_text and judul_lagu and durasi_lagu and key_trans:
    s1 = substitution_cipher(input_text, get_shift_value(judul_lagu, durasi_lagu), True)
    s2 = transposition_cipher(s1, key_trans, True)
    final_res = ekp_cipher(s2, True)
    status_msg = "Enkripsi Berhasil"

elif do_decrypt and input_text and judul_lagu and durasi_lagu and key_trans:
    s1 = ekp_cipher(input_text, False)
    s2 = transposition_cipher(s1, key_trans, False)
    final_res = substitution_cipher(s2, get_shift_value(judul_lagu, durasi_lagu), False)
    status_msg = "Dekripsi Berhasil"

# Hasil
if final_res:
    if status_msg == "Enkripsi Berhasil":
        st.success(status_msg)
    else:
        st.info(status_msg)
        
    st.markdown("### Hasil:")
    st.code(final_res)
    
    st.markdown("""
        <div style='text-align: center; margin-top: 20px; font-size: 12px; color: #888;'>
            create by Aisyah Nur Maya Silviyani
        </div>
    """, unsafe_allow_html=True)

elif not final_res:
    st.markdown("""
        <div style='text-align: center; margin-top: 40px; font-size: 12px; color: #888;'>
            create by Aisyah Nur Maya Silviyani
        </div>
    """, unsafe_allow_html=True)
