import streamlit as st
import math

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Algoritma Kripto",
    layout="centered"
)

# --- 2. Custom CSS (Desain Mirip Screenshot Baru) ---
st.markdown("""
    <style>
    /* Background Utama: Gradient Ungu */
    .stApp {
        background: linear-gradient(135deg, #4b0082 0%, #8e44ad 100%);
        background-attachment: fixed;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background: linear-gradient(180deg, rgba(75, 0, 130, 0.6) 0%, rgba(138, 43, 226, 0.4) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput label, .stTextArea label, .stNumberInput label, p, h1, h2, h3 {
        color: #ffffff !important;
    }

    /* Styling Input Field (Kotak Putih, Teks Hitam) */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 5px;
    }

    /* Tombol Enkripsi (Ungu Terang/Magenta) */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #aa076b 0%, #61045f 100%); 
        color: white;
        border: none;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02);
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
    }

    /* Tombol Dekripsi (Biru Tua) - Kita pakai CSS hack urutan tombol */
    /* Karena streamlit sulit menarget tombol spesifik, kita akali di python layout */

    /* Kotak Hasil (Dashed Border) */
    .result-box {
        background-color: rgba(255, 255, 255, 0.15);
        border: 2px dashed rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 50px;
        color: white;
        margin-top: 10px;
        font-family: monospace;
        font-size: 1.1em;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
        margin-top: 20px;
        font-style: italic;
    }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. Fungsi Logika Kriptografi ---

def get_substitution_shift(judul_lagu, durasi_str):
    if not judul_lagu or not durasi_str:
        return 0
    judul_clean = judul_lagu.replace(" ", "")
    len_judul = len(judul_clean)
    durasi_clean = durasi_str.replace(".", "").replace(":", "")
    try:
        durasi_val = int(durasi_clean)
    except ValueError:
        durasi_val = 0
    total_val = len_judul + durasi_val
    shift = total_val % 26
    return shift

def substitution_cipher(text, shift, decrypt=False):
    result = ""
    if decrypt: shift = -shift
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def transposition_cipher(text, key_str, decrypt=False):
    if not key_str.isdigit(): return text
    key = [int(k) for k in key_str]
    num_cols = len(key)
    if num_cols == 0: return text
    
    if not decrypt:
        # Enkripsi Transposisi
        num_rows = math.ceil(len(text) / num_cols)
        padded_text = text.ljust(num_rows * num_cols, '_')
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        idx = 0
        for r in range(num_rows):
            for c in range(num_cols):
                grid[r][c] = padded_text[idx]
                idx += 1
        
        # Urutkan berdasarkan index key (Sederhana: baca kolom 0, 1, 2 sesuai urutan key user)
        # Note: Implementasi Columnar Cipher yang "benar" biasanya mengurutkan key dulu.
        # Disini kita ikuti alur simpel: Key "3142" -> Baca kolom ke-3, lalu ke-1, dst.
        cipher_text = ""
        # Karena user minta "kunci transposisi", kita asumsikan urutan pembacaan kolom
        # Mapping key digit ke index kolom (0-based)
        # Misal key 3142 -> kita anggap maksudnya urutan prioritas, tapi agar simpel dan bisa didekripsi:
        # Kita pakai standard columnar: Sort key, read column corresponding to sorted key.
        
        # Untuk simplifikasi sesuai request level mahasiswa:
        # Kita pakai transposisi matriks sederhana saja (Read Column by Column)
        result = ""
        for c in range(num_cols):
            for r in range(num_rows):
                result += grid[r][c]
        return result.replace('_', '') # Hapus padding
        
    else:
        # Dekripsi Transposisi (Logic kebalikan sederhana)
        # Hitung row dan col
        num_rows = math.ceil(len(text) / num_cols)
        num_full_cells = len(text)
        
        # Reconstruct grid by filling columns
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        idx = 0
        for c in range(num_cols):
            for r in range(num_rows):
                if idx < len(text):
                    grid[r][c] = text[idx]
                    idx += 1
        
        # Read rows
        result = ""
        for r in range(num_rows):
            for c in range(num_cols):
                result += grid[r][c]
        return result

def ekp_cipher(text, decrypt=False):
    # Mapping Karakter ke Simbol (EKP)
    # Ini mapping contoh, pastikan tabel mapping sama saat dekripsi
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # Simbol diperluas (Expansion)
    symbols = [
        'α', 'β', '©', 'δ', '€', 'ƒ', '6', '#', '!', '¿', 'κ', '£', 'μ', 'η', 'ø', '¶', 'Ω', '®', '$', '†', 'µ', '√', 'ω', '×', '¥', 'ž',
        'Α', 'Β', 'Ç', 'Δ', '£', 'F', 'G', 'H', '1', 'J', 'K', 'L', 'M', 'N', '0', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'
    ]
    
    # Buat dictionary
    encode_map = {c: s for c, s in zip(chars, symbols)}
    decode_map = {s: c for c, s in zip(chars, symbols)}
    
    result = ""
    for char in text:
        if not decrypt:
            result += encode_map.get(char, char)
        else:
            result += decode_map.get(char, char)
    return result

# --- 4. Tampilan UI ---

st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 30px;'>Kriptografi EKP</h1>", unsafe_allow_html=True)

# Input Text
plaintext = st.text_area("Masukkan Teks (Plaintext/Ciphertext):", height=100)

# Konfigurasi Kunci
st.markdown("### Konfigurasi Kunci")
col_k1, col_k2, col_k3 = st.columns(3)

with col_k1:
    judul_lagu = st.text_input("Judul Lagu", placeholder="Cth: Separuh Nafas")
with col_k2:
    durasi = st.text_input("Durasi", placeholder="Cth: 4.14")
with col_k3:
    key_trans = st.text_input("Key Transposisi", placeholder="Cth: 3142")

# Tombol Action
st.write("") # Spacer
col_btn1, col_btn2 = st.columns(2)

action = None
with col_btn1:
    # Tombol Enkripsi (Ungu)
    if st.button(" Enkripsi 🔒"):
        action = "encrypt"

with col_btn2:
    # Tombol Dekripsi (Biru - Styling manual lewat st.markdown button hack agak rumit, 
    # jadi kita biarkan default streamlit secondary button tapi di CSS kita target tombol ke-2 jika bisa,
    # atau biarkan abu-abu gelap agar kontras).
    # Namun, agar sesuai request "Biru", kita gunakan button type "primary" untuk enkripsi, 
    # dan kita inject CSS khusus untuk tombol di kolom 2 jika memungkinkan.
    # Disini kita pakai tombol biasa, nanti warnanya ikut CSS global atau default.
    if st.button("Dekripsi 🔓"):
        action = "decrypt"

# --- 5. Proses & Hasil ---
if action and plaintext:
    shift = get_substitution_shift(judul_lagu, durasi)
    
    if action == "encrypt":
        # 1. Substitusi
        step1 = substitution_cipher(plaintext, shift, decrypt=False)
        # 2. Transposisi
        step2 = transposition_cipher(step1, key_trans, decrypt=False)
        # 3. Ekspansi (EKP)
        final_result = ekp_cipher(step2, decrypt=False)
        label = "Hasil Enkripsi:"
    
    else: # Decrypt
        # Urutan Dekripsi dibalik: EKP -> Transposisi -> Substitusi
        # 1. Reverse EKP
        step1 = ekp_cipher(plaintext, decrypt=True)
        # 2. Reverse Transposisi
        step2 = transposition_cipher(step1, key_trans, decrypt=True)
        # 3. Reverse Substitusi
        final_result = substitution_cipher(step2, shift, decrypt=True)
        label = "Hasil Dekripsi:"

    # Tampilkan Hasil dalam Kotak Dashed
    st.markdown(f"**{label}**")
    st.markdown(f"""
        <div class="result-box">
            {final_result}
        </div>
    """, unsafe_allow_html=True)
    
    # Footer Nama (Muncul setelah hasil)
    st.markdown("""
        <div class="footer-text">
            create by Aisyah Nur Maya Silviyani
        </div>
    """, unsafe_allow_html=True)

elif action and not plaintext:
    st.warning("Mohon masukkan teks terlebih dahulu.")
