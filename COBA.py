import streamlit as st
import math

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Kriptografi EKP - Aisyah",
    page_icon="🔐",
    layout="centered"
)

# --- 2. Custom CSS (Tampilan Ungu, Teks Jelas, Tombol Rapi) ---
st.markdown("""
    <style>
    /* Background Gradient Ungu */
    .stApp {
        background: linear-gradient(135deg, #2e003e 0%, #4b0082 50%, #800080 100%);
        background-attachment: fixed;
    }
    
    /* Container Putih (Tempat Isi Konten) */
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* Memastikan Teks Berwarna Hitam/Gelap */
    h2, h3, h4, h5, p, span, div, label, .stMarkdown {
        color: #333333 !important;
    }
    
    /* Judul Utama */
    h1 {
        color: #4b0082 !important;
        text-align: center;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    /* Input Field */
    .stTextInput input, .stTextArea textarea {
        background-color: #f8f9fa;
        color: #000000 !important;
        border: 1px solid #ced4da;
    }
    
    /* Hide elemen bawaan */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. Logika Kriptografi ---

def get_shift_value(judul, durasi):
    # Hitung huruf judul (tanpa spasi)
    judul_clean = ''.join(filter(str.isalpha, judul))
    len_judul = len(judul_clean)
    
    # Ambil angka durasi
    durasi_clean = durasi.replace(".", "").replace(":", "")
    try:
        val_durasi = int(durasi_clean)
    except ValueError:
        val_durasi = 0
    
    # Hitung Modulus 26
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

# LOGIKA BARU SESUAI REQUEST
def ekp_cipher(text, encrypt=True):
    # Mapping sesuai permintaan user
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
        # LOGIKA DEKRIPSI (Reverse Mapping)
        # Kita harus hati-hati karena panjang simbol berbeda-beda.
        # Strategi: Urutkan simbol dari yang terpanjang ke terpendek untuk pencocokan.
        reverse_map = {v: k for k, v in ekp_map.items()}
        # Urutkan key reverse (simbol) berdasarkan panjang string descending
        sorted_symbols = sorted(reverse_map.keys(), key=len, reverse=True)
        
        hasil = ""
        i = 0
        while i < len(text):
            match_found = False
            # Cek apakah text dimulai dengan salah satu simbol EKP
            for sym in sorted_symbols:
                if text.startswith(sym, i):
                    hasil += reverse_map[sym]
                    i += len(sym)
                    match_found = True
                    break
            
            if not match_found:
                hasil += text[i]
                i += 1
        return hasil

# --- 4. Tampilan Antarmuka ---

st.title("KRIPTOGRAFI EKP")
st.markdown("<p style='text-align: center; margin-top: -15px; font-size: 14px; color: #555 !important;'>Metode Substitusi Lagu + Transposisi + Ekspansi Karakter Polialfanumerik</p>", unsafe_allow_html=True)

# Input
st.markdown("##### Masukkan Teks:")
input_text = st.text_area("", height=100, placeholder="Ketik pesan di sini...", label_visibility="collapsed")

st.markdown("##### Konfigurasi Kunci:")
col_k1, col_k2, col_k3 = st.columns(3)

with col_k1:
    judul_lagu = st.text_input("Judul Lagu", placeholder="Cth: Separuh Nafas")
with col_k2:
    durasi_lagu = st.text_input("Durasi", placeholder="Cth: 4.14")
with col_k3:
    key_trans = st.text_input("Key Transposisi", placeholder="Max 4 angka (3142)", max_chars=4)

st.write("") # Spacer

# Tombol
c1, btn_enc, btn_dec, c2 = st.columns([0.2, 2, 2, 0.2])
with btn_enc:
    encrypt_state = st.button("ENKRIPSI", use_container_width=True)
with btn_dec:
    decrypt_state = st.button("DEKRIPSI / RESET", use_container_width=True)

# CSS Tombol (Tinggi & Warna)
st.markdown("""
<style>
div[data-testid="column"]:nth-of-type(2) button {
    background-color: #4b0082 !important; 
    color: white !important; font-weight: bold; border-radius: 8px; height: 55px; font-size: 16px;
}
div[data-testid="column"]:nth-of-type(3) button {
    background-color: #9932cc !important;
    color: white !important; font-weight: bold; border-radius: 8px; height: 55px; font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Proses
final_result = ""
msg_status = ""

if encrypt_state and input_text and judul_lagu and durasi_lagu and key_trans:
    # Urutan: Substitusi -> Transposisi -> EKP
    s1 = substitution_cipher(input_text, get_shift_value(judul_lagu, durasi_lagu), True)
    s2 = transposition_cipher(s1, key_trans, True)
    final_result = ekp_cipher(s2, True)
    msg_status = "Enkripsi Berhasil"

elif decrypt_state and input_text and judul_lagu and durasi_lagu and key_trans:
    # Urutan Balik: EKP -> Transposisi -> Substitusi
    s1 = ekp_cipher(input_text, False)
    s2 = transposition_cipher(s1, key_trans, False)
    final_result = substitution_cipher(s2, get_shift_value(judul_lagu, durasi_lagu), False)
    msg_status = "Dekripsi Berhasil"

# Hasil & Footer
if final_result:
    if msg_status == "Enkripsi Berhasil":
        st.success(msg_status)
    else:
        st.info(msg_status)
        
    st.markdown("##### Hasil:")
    st.code(final_result)
    
    # CREDIT NAMA DI BAWAH HASIL (Kecil)
    st.markdown("""
        <div style='text-align: center; margin-top: 20px; color: #666; font-size: 13px; font-style: italic;'>
            create by Aisyah Nur Maya Silviyani
        </div>
    """, unsafe_allow_html=True)

elif not final_result:
    # Tampilkan credit tetap ada di bawah meski belum ada hasil
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; color: #666; font-size: 13px; font-style: italic;'>
            create by Aisyah Nur Maya Silviyani
        </div>
    """, unsafe_allow_html=True)
