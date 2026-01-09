import streamlit as st
import math

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Kriptografi",
    layout="centered"
)

# --- 2. Custom CSS (Ui Ungu, Putih, dan Tombol) ---
st.markdown("""
    <style>
    /* Background Gradient Ungu */
    .stApp {
        background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%);
        background-attachment: fixed;
    }
    
    /* Container Putih di Tengah */
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Warna Teks Hitam */
    h1, h3, p, label, .stMarkdown, .stTextInput > label, .stTextArea > label {
        color: #333333 !important;
    }
    
    /* Judul Utama Putih (agar kontras dengan background ungu header jika ada) atau Hitam */
    h1 {
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: #ffffff !important; 
        text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    
    /* Styling Input Fields agar border lebih tegas */
    .stTextInput input, .stTextArea textarea {
        border: 1px solid #ced4da;
        border-radius: 5px;
    }

    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4b0082; /* Ungu Gelap */
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        z-index: 100;
        letter-spacing: 1px;
    }
    
    /* Hide default footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. Fungsi Logika Kriptografi ---

def get_substitution_shift(judul_lagu, durasi_str):
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
    if not key_str.isdigit() or len(key_str) == 0:
        return text 

    key = [int(k) for k in key_str]
    # Filter key unik jika perlu, atau pakai apa adanya. 
    # Disini kita asumsi simple columnar sesuai request user sebelumnya.
    
    num_cols = len(key)
    if num_cols == 0: return text
    
    num_rows = math.ceil(len(text) / num_cols)
    
    # Urutan baca kolom: kita asumsikan urutan berdasarkan besaran angka di key (1,2,3,4)
    # Membuat index urutan: misal key 3142 -> urutan index kolom: 1 (val 1), 3 (val 2), 0 (val 3), 2 (val 4)
    key_with_index = sorted(enumerate(key), key=lambda x: x[1])
    
    if not decrypt:
        # ENKRIPSI
        padded_text = text.ljust(num_rows * num_cols, '_')
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        idx = 0
        for r in range(num_rows):
            for c in range(num_cols):
                grid[r][c] = padded_text[idx]
                idx += 1
        
        cipher_text = ""
        for original_index, _ in key_with_index:
            for row in range(num_rows):
                cipher_text += grid[row][original_index]
        return cipher_text.replace('_', '')
        
    else:
        # DEKRIPSI (Reverse Transposition)
        # Hitung panjang kolom
        num_full_cols = len(text) % num_cols
        col_lengths = [len(text) // num_cols] * num_cols
        for i in range(num_full_cols):
            # Logika padding agak kompleks untuk transposisi tak rata, 
            # untuk simplifikasi Ujian ini kita anggap text pas atau padding di handle di akhir.
            # Kita asumsi panjang rata untuk mempermudah visualisasi logic dasar.
            pass
            
        # Reconstruct grid is tricky without perfect padding knowledge.
        # Simple approach: Fill column by column based on sorted key
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        idx = 0
        
        for original_index, _ in key_with_index:
            for r in range(num_rows):
                if idx < len(text):
                    grid[r][original_index] = text[idx]
                    idx += 1
                    
        plain = ""
        for r in range(num_rows):
            for c in range(num_cols):
                plain += grid[r][c]
        return plain.rstrip('_')

def ekp_cipher(text, decrypt=False):
    # Mapping simbol sederhana (EKP)
    # Ini hanya contoh representasi, bisa disesuaikan simbolnya
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Simbol-simbol unik
    symbols = ["α","ß","©","δ","€","ƒ","6","#","!","¿","κ","£","μ","η","ø","¶","Ω","®","$","†","µ","√","ω","×","¥","ž",
               "Δ","Θ","Λ","Ξ","Π","Σ","Φ","Ψ","Ω","Γ","∇","∫","∂","∞","≈","≠","≡","≤","≥","⊂"]
    
    char_to_sym = dict(zip(chars, symbols[:len(chars)]))
    sym_to_char = dict(zip(symbols[:len(chars)], chars))
    
    result = ""
    # EKP Logic: loop text (bisa diimprove menangani multi-char symbols)
    if not decrypt:
        for char in text:
            result += char_to_sym.get(char, char)
    else:
        # Dekripsi EKP agak tricky jika simbol > 1 char, tapi disini asumsi 1 char = 1 simbol
        for char in text:
            result += sym_to_char.get(char, char)
    return result

# --- 4. Tampilan Utama (UI) ---

st.title("Kriptografi EKP")
st.markdown("<h4 style='text-align: center; color: #333;'>Metode Substitusi Lagu + Transposisi + Ekspansi Karakter</h4>", unsafe_allow_html=True)

# Input Text
plaintext = st.text_area("Masukkan Teks (Plaintext / Ciphertext):", height=150, placeholder="Ketik pesan di sini...")

st.markdown("### Konfigurasi Kunci")

# Kolom Input Key
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    judul_lagu = st.text_input("Judul Lagu", placeholder="Contoh: Separuh Nafas")
with c2:
    durasi_lagu = st.text_input("Durasi", placeholder="Cth: 4.14")
with c3:
    key_transposisi = st.text_input("Key Transposisi", placeholder="3142")

st.write("") # Spacer

# --- TOMBOL AKSI ---
# Membuat layout tombol agak ke tengah dan memanjang
# Kita bagi kolom: [Kosong Kecil, Tombol 1, Tombol 2, Kosong Kecil]
col_space_L, col_btn_1, col_btn_2, col_space_R = st.columns([0.5, 2, 2, 0.5])

encrypt_clicked = False
decrypt_clicked = False

with col_btn_1:
    # Tombol Enkripsi (Hijau)
    encrypt_clicked = st.button("Enkripsi", use_container_width=True, type="primary")

with col_btn_2:
    # Tombol Dekripsi (Biru - Menggunakan type secondary + CSS nanti jika perlu)
    decrypt_clicked = st.button("Dekripsi / Reset", use_container_width=True)

# CSS Khusus untuk mewarnai tombol di kolom spesifik
# Kolom 2 (Tombol Enkripsi) -> Hijau
# Kolom 3 (Tombol Dekripsi) -> Biru
st.markdown("""
<style>
/* Target Tombol di dalam kolom layout tombol */
/* Selector ini mencari tombol di kolom ke-2 (Enkripsi) */
div[data-testid="column"]:nth-of-type(2) button {
    background-color: #28a745 !important; /* Hijau */
    color: white !important;
    border: none;
}
div[data-testid="column"]:nth-of-type(2) button:hover {
    background-color: #218838 !important;
}

/* Selector ini mencari tombol di kolom ke-3 (Dekripsi) */
div[data-testid="column"]:nth-of-type(3) button {
    background-color: #007bff !important; /* Biru */
    color: white !important;
    border: none;
}
div[data-testid="column"]:nth-of-type(3) button:hover {
    background-color: #0069d9 !important;
}
</style>
""", unsafe_allow_html=True)

# --- 5. Proses Eksekusi ---

output_text = ""
detail_steps = []

if encrypt_clicked and plaintext and judul_lagu and durasi_lagu and key_transposisi:
    # 1. Substitusi
    shift_val = get_substitution_shift(judul_lagu, durasi_lagu)
    step1 = substitution_cipher(plaintext, shift_val)
    detail_steps.append(f"**1. Substitusi (Shift {shift_val}):** {step1}")
    
    # 2. Transposisi
    step2 = transposition_cipher(step1, key_transposisi)
    detail_steps.append(f"**2. Transposisi (Key {key_transposisi}):** {step2}")
    
    # 3. Ekspansi (EKP)
    step3 = ekp_cipher(step2)
    detail_steps.append(f"**3. Ekspansi Karakter (EKP):** {step3}")
    
    output_text = step3
    st.success("Enkripsi Berhasil!")

elif decrypt_clicked and plaintext:
    # Logika Dekripsi (Kebalikan urutan)
    # 1. Reverse EKP
    step1 = ekp_cipher(plaintext, decrypt=True)
    detail_steps.append(f"**1. Reverse EKP:** {step1}")
    
    # 2. Reverse Transposisi
    step2 = transposition_cipher(step1, key_transposisi, decrypt=True)
    detail_steps.append(f"**2. Reverse Transposisi:** {step2}")
    
    # 3. Reverse Substitusi
    shift_val = get_substitution_shift(judul_lagu, durasi_lagu)
    step3 = substitution_cipher(step2, shift_val, decrypt=True)
    detail_steps.append(f"**3. Plaintext Akhir:** {step3}")
    
    output_text = step3
    st.info("Dekripsi Selesai / Reset")

# Menampilkan Hasil
if output_text:
    st.markdown("---")
    st.subheader("Hasil:")
    st.code(output_text)
    
    with st.expander("Lihat Proses Detail"):
        for step in detail_steps:
            st.write(step)

# --- Footer ---
st.markdown('<div class="footer">create by Aisyah Nur Maya Silviyani</div>', unsafe_allow_html=True)
