import streamlit as st
import math

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="ALGORITMA KREASI",
    layout="centered"
)

# --- 2. Custom CSS (Tampilan Ungu Gradasi & Tombol Rapi) ---
st.markdown("""
    <style>
    /* Background Gradient Ungu Gelap ke Putih/Abu Gelap */
    .stApp {
        background: linear-gradient(135deg, #2e003e 0%, #4b0082 50%, #800080 100%);
        background-attachment: fixed;
    }
    
    /* Container Putih Transparan (Glassmorphism) */
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* Warna Teks Default Hitam agar terbaca di box putih */
    h1, h2, h3, p, label, div, span {
        color: #1a1a1a !important;
    }
    
    /* Judul Utama */
    h1 {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 800;
        color: #4b0082 !important; /* Judul Ungu */
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Input Field Styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        color: #333;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #800080;
        box-shadow: 0 0 5px rgba(128, 0, 128, 0.5);
    }

    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1a1a1a;
        color: white !important;
        text-align: center;
        padding: 12px;
        font-size: 14px;
        font-weight: bold;
        z-index: 999;
        letter-spacing: 1.5px;
    }
    
    /* Tombol Custom: Enkripsi (Ungu Gelap) & Dekripsi (Ungu Terang) */
    /* Kita gunakan selector urutan kolom tombol nanti */
    
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. Logika Kriptografi ---

# A. Logika Kunci Substitusi (Judul Lagu + Durasi)
def get_shift_value(judul, durasi):
    # 1. Hitung jumlah huruf judul (tanpa spasi)
    judul_clean = ''.join(filter(str.isalpha, judul))
    len_judul = len(judul_clean)
    
    # 2. Ambil angka durasi (hilangkan titik/titik dua)
    durasi_clean = durasi.replace(".", "").replace(":", "")
    try:
        val_durasi = int(durasi_clean)
    except ValueError:
        val_durasi = 0
    
    # 3. Hitung Modulus 26
    total = len_judul + val_durasi
    shift = total % 26
    return shift

# B. Cipher Substitusi (Caesar)
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

# C. Cipher Transposisi (Columnar)
def transposition_cipher(text, key_str, encrypt=True):
    # Validasi key (maks 4 angka)
    if not key_str.isdigit(): return text
    
    # Ambil maks 4 digit pertama sesuai request
    key_str = key_str[:4]
    key = [int(k) for k in key_str]
    num_cols = len(key)
    if num_cols == 0: return text
    
    # Urutan pembacaan kolom berdasarkan nilai angka kunci (misal 3142 -> urutan index 1, 3, 0, 2)
    # Kita urutkan index berdasarkan nilai key-nya
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    if encrypt:
        # Padding
        num_rows = math.ceil(len(text) / num_cols)
        padded_text = text.ljust(num_rows * num_cols, '_') # _ sebagai padding
        
        # Buat Grid
        grid = []
        for r in range(num_rows):
            grid.append(list(padded_text[r*num_cols : (r+1)*num_cols]))
            
        # Baca kolom berdasarkan urutan key
        cipher = ""
        for col_idx in key_order:
            for row in range(num_rows):
                cipher += grid[row][col_idx]
        return cipher.replace('_', '') # Hapus padding visual untuk output
        
    else: # Decrypt
        # Hitung baris
        num_rows = math.ceil(len(text) / num_cols)
        num_empty = (num_rows * num_cols) - len(text) # Slot kosong di akhir (jika padding dihapus)
        
        # Grid kosong
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        # Mengisi Grid kolom demi kolom
        idx = 0
        for k_idx in key_order:
            # Hitung panjang kolom ini (apakah full atau kena potong di baris terakhir?)
            # Logic sederhana: Anggap input text sudah termasuk padding _ jika user copy paste hasil enkripsi
            # Jika tidak, kita asumsikan rata untuk mempermudah, atau fill sebisanya.
            
            # Kita isi grid kolom demi kolom
            for r in range(num_rows):
                if idx < len(text):
                    grid[r][k_idx] = text[idx]
                    idx += 1
        
        # Baca baris demi baris
        plain = ""
        for r in range(num_rows):
            for c in range(num_cols):
                plain += grid[r][c]
        return plain.rstrip('_')

# D. Cipher EKP (Ekspansi Karakter Polialfanumerik)
def ekp_cipher(text, encrypt=True):
    # Peta Simbol (Simulasi Ekspansi)
    # Memetakan huruf biasa ke simbol 'unik'
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    # Simbol menggunakan karakter Yunani/Math agar terlihat 'Expanded'
    symbols = [
        "α","β","χ","δ","ε","φ","γ","η","ι","θ","κ","λ","μ","ν","ο","π","ψ","ρ","σ","τ","υ","ω","ξ","ζ","ψ","ω", # a-z
        "Α","Β","Χ","Δ","Ε","Φ","Γ","Η","Ι","Θ","Κ","Λ","Μ","Ν","Ο","Π","Ψ","Ρ","Σ","Τ","Υ","Ω","Ξ","Ζ","Ψ","Ω", # A-Z
        "①","②","③","④","⑤","⑥","⑦","⑧","⑨","⓪", # 0-9
        "∆" # Spasi
    ]
    
    # Dictionary mapping
    char_to_sym = {c: s for c, s in zip(chars, symbols)}
    sym_to_char = {s: c for c, s in zip(chars, symbols)}
    
    result = ""
    if encrypt:
        for char in text:
            # Jika karakter ada di map, ganti. Jika tidak (tanda baca lain), biarkan.
            result += char_to_sym.get(char, char)
    else:
        for char in text:
            result += sym_to_char.get(char, char)
            
    return result

# --- 4. Tampilan Antarmuka (UI) ---

st.title("KRIPTOGRAFI EKP")
st.markdown("<p style='text-align: center; margin-top: -20px; color: #666 !important;'>Metode Substitusi Lagu + Transposisi + Ekspansi Karakter Polialfanumerik</p>", unsafe_allow_html=True)

# Area Input Plaintext
input_text = st.text_area("Masukkan Teks (Plaintext / Ciphertext)", height=120, placeholder="Ketik pesan rahasia di sini...")

st.markdown("### Konfigurasi Kunci")

# Kolom untuk Input Kunci (3 Kolom Sejajar)
col_k1, col_k2, col_k3 = st.columns(3)

with col_k1:
    judul_lagu = st.text_input("1. Judul Lagu", placeholder="Cth: Separuh Nafas")
    st.caption("Untuk hitung huruf")

with col_k2:
    durasi_lagu = st.text_input("2. Menit Lagu", placeholder="Cth: 4.14")
    st.caption("Hilangkan titik (414)")

with col_k3:
    key_trans = st.text_input("3. Key Transposisi", placeholder="Max 4 angka (3142)", max_chars=4)
    st.caption("Angka bebas")

st.write("---")

# --- TOMBOL AKSI SEJAJAR ---
# Menggunakan columns untuk menengahkan dan merapikan tombol
c_spacer1, c_btn1, c_btn2, c_spacer2 = st.columns([0.5, 2, 2, 0.5])

encrypt_state = False
decrypt_state = False

with c_btn1:
    encrypt_state = st.button("ENKRIPSI 🔒", use_container_width=True)

with c_btn2:
    decrypt_state = st.button("DEKRIPSI 🔓", use_container_width=True)

# CSS Khusus untuk mewarnai tombol (Inject CSS based on column index)
st.markdown("""
<style>
/* Tombol Kiri (Enkripsi) - Warna Ungu Tua */
div[data-testid="column"]:nth-of-type(2) button {
    background-color: #4b0082 !important; 
    color: white !important;
    border: none;
    font-weight: bold;
    padding: 15px;
    border-radius: 8px;
    transition: 0.3s;
}
div[data-testid="column"]:nth-of-type(2) button:hover {
    background-color: #320057 !important;
    box-shadow: 0 4px 10px rgba(75, 0, 130, 0.4);
}

/* Tombol Kanan (Dekripsi) - Warna Ungu Muda/Magenta */
div[data-testid="column"]:nth-of-type(3) button {
    background-color: #9932cc !important;
    color: white !important;
    border: none;
    font-weight: bold;
    padding: 15px;
    border-radius: 8px;
    transition: 0.3s;
}
div[data-testid="column"]:nth-of-type(3) button:hover {
    background-color: #7b1fa2 !important;
    box-shadow: 0 4px 10px rgba(153, 50, 204, 0.4);
}
</style>
""", unsafe_allow_html=True)

# --- 5. Proses Eksekusi ---

final_result = ""
log_steps = []

if encrypt_state:
    if not input_text or not judul_lagu or not durasi_lagu or not key_trans:
        st.error("Mohon lengkapi Teks, Judul Lagu, Durasi, dan Key Transposisi!")
    else:
        # STEP 1: Substitusi
        shift_val = get_shift_value(judul_lagu, durasi_lagu)
        res_sub = substitution_cipher(input_text, shift_val, encrypt=True)
        log_steps.append(f"**1. Substitusi** (Shift {shift_val}): `{res_sub}`")
        
        # STEP 2: Transposisi
        res_trans = transposition_cipher(res_sub, key_trans, encrypt=True)
        log_steps.append(f"**2. Transposisi** (Key {key_trans}): `{res_trans}`")
        
        # STEP 3: EKP (Ekspansi)
        res_ekp = ekp_cipher(res_trans, encrypt=True)
        log_steps.append(f"**3. EKP (Simbol):** `{res_ekp}`")
        
        final_result = res_ekp
        st.success("Enkripsi Selesai!")

elif decrypt_state:
    if not input_text or not judul_lagu or not durasi_lagu or not key_trans:
        st.error("Mohon lengkapi semua data untuk dekripsi!")
    else:
        # STEP 1: Reverse EKP
        res_ekp = ekp_cipher(input_text, encrypt=False)
        log_steps.append(f"**1. Reverse EKP:** `{res_ekp}`")
        
        # STEP 2: Reverse Transposisi
        res_trans = transposition_cipher(res_ekp, key_trans, encrypt=False)
        log_steps.append(f"**2. Reverse Transposisi:** `{res_trans}`")
        
        # STEP 3: Reverse Substitusi
        shift_val = get_shift_value(judul_lagu, durasi_lagu)
        res_sub = substitution_cipher(res_trans, shift_val, encrypt=False)
        log_steps.append(f"**3. Hasil Dekripsi:** `{res_sub}`")
        
        final_result = res_sub
        st.info("Dekripsi Selesai!")

# --- Output Area ---
if final_result:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📤 Hasil Akhir")
    st.text_area("Output", value=final_result, height=100, disabled=True)
    
    with st.expander("🔍 Lihat Detail Proses (Logika)"):
        for step in log_steps:
            st.markdown(step)

# --- Footer ---
st.markdown('<div class="footer">create by Aisyah Nur Maya Silviyani</div>', unsafe_allow_html=True)
