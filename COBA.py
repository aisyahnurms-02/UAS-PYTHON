import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Crypto Aisyah - EKP Model", layout="centered", page_icon="💜")

# --- CUSTOM CSS (UNTUK TAMPILAN KARTU & GRADASI) ---
st.markdown("""
    <style>
    /* 1. Background Utama: Gradasi Ungu Gelap ke Putih */
    .stApp {
        background: linear-gradient(180deg, #2E003E 0%, #6A1B9A 50%, #FFFFFF 100%);
        background-attachment: fixed;
    }

    /* 2. Mengubah Container Utama menjadi "Kartu Putih" di tengah */
    div.block-container {
        background-color: #FFFFFF;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 700px; /* Lebar kartu dibatasi agar rapi */
        margin-top: 50px;
    }

    /* 3. Styling Judul */
    h1 {
        color: #333333;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        margin-bottom: 0px;
    }
    
    /* Label Input */
    .stTextInput > label, .stTextArea > label {
        color: #333333;
        font-weight: bold;
        font-size: 14px;
    }

    /* 4. Styling Tombol (Mirip Screenshot) */
    /* Tombol Enkripsi (Primary) -> Hijau */
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        height: 45px;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #218838;
    }

    /* Tombol Dekripsi (Secondary) -> Biru */
    div.stButton > button[kind="secondary"] {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        height: 45px;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #0069d9;
        border-color: #0062cc;
        color: white;
    }

    /* 5. Kotak Hasil (Abu-abu seperti screenshot) */
    .result-box {
        background-color: #E9ECEF;
        border: 1px solid #CED4DA;
        border-radius: 5px;
        padding: 15px;
        color: #000;
        font-family: monospace;
        font-weight: bold;
        margin-top: 5px;
    }

    /* 6. Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4A148C;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        letter-spacing: 1px;
        z-index: 999;
    }
    
    /* Menyembunyikan elemen bawaan Streamlit yang tidak perlu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI ---

def hitung_shift_key(judul_lagu, durasi_menit):
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    durasi_bersih = durasi_menit.replace(".", "")
    
    if not durasi_bersih.isdigit():
        return 0, "⚠️ Error: Durasi harus angka."
        
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

# Judul di dalam kartu putih
st.markdown("<h1>Kriptografi EKP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Metode Substitusi Lagu + Transposisi + Ekspansi Karakter</p>", unsafe_allow_html=True)

# Input Plaintext
plaintext = st.text_area("Masukkan Teks (Plaintext):", placeholder="Ketik pesan rahasia di sini...", height=100)

st.markdown("---")
st.markdown("##### 🔑 Konfigurasi Kunci")

# Menggunakan Columns untuk input kunci agar rapi
c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu", "Separuh Nafas")
with c2:
    durasi = st.text_input("Durasi (Cth: 4.14)", "4.14")
with c3:
    kunci_transposisi = st.text_input("Key Transposisi", "3142", max_chars=4)

st.markdown("<br>", unsafe_allow_html=True)

# Tombol Action (Hijau dan Biru bersampingan)
col_btn1, col_btn2 = st.columns(2)

hasil_akhir = ""
detail_shift = ""
show_result = False

with col_btn1:
    # Tombol Enkripsi (Hijau - Primary)
    if st.button("Enkripsi", key="btn_encrypt", type="primary"):
        if not plaintext or not judul_lagu or not durasi or not kunci_transposisi:
            st.error("⚠️ Semua input harus diisi!")
        else:
            # Proses
            shift_val, detail_shift = hitung_shift_key(judul_lagu, durasi)
            step1 = enkripsi_substitusi(plaintext, shift_val)
            step2 = enkripsi_transposisi(step1, kunci_transposisi)
            hasil_akhir = enkripsi_ekp(step2)
            show_result = True

with col_btn2:
    # Tombol Dekripsi/Reset (Biru - Secondary)
    # Karena dekripsi EKP kompleks (banyak ke satu), tombol ini kita buat refresh/info
    if st.button("Dekripsi / Reset", key="btn_decrypt", type="secondary"):
        st.rerun()

# Menampilkan Hasil
if show_result:
    st.markdown("##### Hasil:")
    
    # Kotak Abu-abu seperti screenshot
    st.markdown(f"""
    <div class="result-box">
        {hasil_akhir}
    </div>
    """, unsafe_allow_html=True)
    
    # Penjelasan singkat (Opsional, agar user paham prosesnya)
    with st.expander("Lihat Detail Proses"):
        st.write(f"**1. Shift Key:** {detail_shift}")
        st.write(f"**2. Hasil Substitusi:** {enkripsi_substitusi(plaintext, hitung_shift_key(judul_lagu, durasi)[0])}")
        st.write(f"**3. Hasil Transposisi:** {enkripsi_transposisi(enkripsi_substitusi(plaintext, hitung_shift_key(judul_lagu, durasi)[0]), kunci_transposisi)}")

# Spacer agar tidak tertutup footer
st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        create by Aisyah Nur Maya Silviyani
    </div>
""", unsafe_allow_html=True)
