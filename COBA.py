import streamlit as st
import math

# --- 1. CONFIG HALAMAN ---
st.set_page_config(
    page_title="Kripto",
    layout="centered"
)

# --- 2. CSS "ANTI-GELAP" (FORCE CONTRAST) ---
st.markdown("""
    <style>
    /* 1. Background Halaman: Gradasi Ungu */
    .stApp {
        background: linear-gradient(180deg, #4b0082 0%, #240046 100%);
        background-attachment: fixed;
    }

    /* 2. Mengatur SEMUA Teks Label/Judul menjadi PUTIH agar terbaca di background ungu */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* 3. Mengatur KOTAK INPUT (Text Area & Input) menjadi PUTIH, Teks HITAM */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important; /* Warna teks ketikan hitam pekat */
        border: 2px solid #a0a0a0 !important;
        border-radius: 8px;
    }
    
    /* Fokus pada input */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 10px rgba(255,255,255,0.5);
    }
    
    /* 4. Menghilangkan elemen default Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 5. Styling Tombol Custom */
    div[data-testid="column"]:nth-of-type(2) button {
        background-color: #ffffff !important; /* Tombol Putih */
        color: #4b0082 !important; /* Teks Ungu */
        font-weight: bold;
        border: none;
        height: 50px;
    }
    div[data-testid="column"]:nth-of-type(3) button {
        background-color: #1abc9c !important; /* Tombol Tosca/Hijau */
        color: white !important;
        font-weight: bold;
        border: none;
        height: 50px;
    }
    
    /* 6. Styling Kotak Hasil (Code Block) */
    code {
        color: #e0e0e0 !important; /* Teks hasil agak terang */
        background-color: #1e1e1e !important; /* Background hasil gelap */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA KRIPTOGRAFI ---

def get_shift_value(judul, durasi):
    # Bersihkan input
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
    # Ambil 4 digit
    key_str = key_str[:4]
    key = [int(k) for k in key_str]
    num_cols = len(key)
    if num_cols == 0: return text
    
    # Urutan baca kolom
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
    # Mapping Simbol Sesuai Request
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
        # Dekripsi: Reverse Lookup (Cari simbol terpanjang dulu)
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
st.markdown("<p style='text-align: center; margin-top: -15px; opacity: 0.8;'>Metode Substitusi Lagu + Transposisi + Ekspansi Karakter</p>", unsafe_allow_html=True)

st.markdown("### 1. Masukkan Teks")
input_text = st.text_area("", height=100, placeholder="Ketik di sini...", label_visibility="collapsed")

st.markdown("### 2. Konfigurasi Kunci")
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown("**Judul Lagu**")
    judul_lagu = st.text_input("", placeholder="Contoh: Separuh Nafas", key="judul", label_visibility="collapsed")
with k2:
    st.markdown("**Durasi**")
    durasi_lagu = st.text_input("", placeholder="Contoh: 4.12", key="durasi", label_visibility="collapsed")
with k3:
    st.markdown("**Key Transposisi**")
    key_trans = st.text_input("", placeholder="Max 4 angka (1725)", max_chars=4, key="key", label_visibility="collapsed")

st.write("") # Spasi

# --- TOMBOL ---
col_space_1, btn_1, btn_2, col_space_2 = st.columns([0.2, 2, 2, 0.2])

with btn_1:
    encrypt_click = st.button("ENKRIPSI", use_container_width=True)
with btn_2:
    decrypt_click = st.button("DEKRIPSI / RESET", use_container_width=True)

# --- PROSES ---
hasil_akhir = ""
msg = ""

if encrypt_click and input_text and judul_lagu and durasi_lagu and key_trans:
    # 1. Sub
    s1 = substitution_cipher(input_text, get_shift_value(judul_lagu, durasi_lagu), True)
    # 2. Trans
    s2 = transposition_cipher(s1, key_trans, True)
    # 3. EKP
    hasil_akhir = ekp_cipher(s2, True)
    msg = "Enkripsi Berhasil!"

elif decrypt_click and input_text and judul_lagu and durasi_lagu and key_trans:
    # 1. Rev EKP
    s1 = ekp_cipher(input_text, False)
    # 2. Rev Trans
    s2 = transposition_cipher(s1, key_trans, False)
    # 3. Rev Sub
    hasil_akhir = substitution_cipher(s2, get_shift_value(judul_lagu, durasi_lagu), False)
    msg = "Dekripsi Berhasil!"

# --- OUTPUT ---
if msg:
    st.success(msg)

if hasil_akhir:
    st.markdown("### Hasil:")
    st.code(hasil_akhir)
    
    # CREDIT (Kecil di bawah hasil)
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #cccccc;">
    create by Aisyah Nur Maya Silviyani
    </div>
    """, unsafe_allow_html=True)
elif not hasil_akhir:
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; font-size: 12px; color: #cccccc;">
    create by Aisyah Nur Maya Silviyani
    </div>
    """, unsafe_allow_html=True)
