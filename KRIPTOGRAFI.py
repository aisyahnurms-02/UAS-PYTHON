import streamlit as st
import math

# --- KONFIGURASI HALAMAN & CSS (TEMA UNGU) ---
st.set_page_config(page_title="Crypto EKP Aisyah", layout="wide", page_icon="💜")

# Custom CSS untuk Tema Ungu & Putih
st.markdown("""
    <style>
    /* Mengubah warna background utama menjadi putih bersih */
    .stApp {
        background-color: #FFFFFF;
        color: #333333;
    }
    
    /* Mengubah warna Sidebar menjadi Ungu Muda (Lavender) */
    [data-testid="stSidebar"] {
        background-color: #F3E5F5;
        border-right: 2px solid #E1BEE7;
    }
    
    /* Mengubah warna Judul dan Header menjadi Ungu Tua */
    h1, h2, h3, h4, h5, h6 {
        color: #4A148C !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Styling Tombol (Button) menjadi Ungu */
    div.stButton > button {
        background-color: #7B1FA2;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #4A148C; /* Ungu lebih gelap saat hover */
        border: 2px solid #BA68C8;
        color: #fff;
    }
    
    /* Styling Input Field agar border ungu */
    div[data-baseweb="input"] {
        border: 1px solid #CE93D8;
        border-radius: 8px;
    }
    
    /* Styling Text Area */
    div[data-baseweb="textarea"] {
        border: 1px solid #CE93D8;
        border-radius: 8px;
    }
    
    /* Custom Box untuk Hasil */
    .custom-box {
        background-color: #F8F0FC; /* Ungu sangat muda */
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #8E24AA;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Footer Style */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4A148C;
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        letter-spacing: 1px;
        z-index: 999;
    }
    
    /* Spacer untuk konten agar tidak tertutup footer */
    .spacer {
        height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA KRIPTOGRAFI (SAMA SEPERTI SEBELUMNYA) ---

def hitung_shift_key(judul_lagu, durasi_menit):
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    durasi_bersih = durasi_menit.replace(".", "")
    
    if not durasi_bersih.isdigit():
        return 0, "⚠️ Error: Durasi harus angka."
        
    nilai_durasi = int(durasi_bersih)
    total = jumlah_huruf + nilai_durasi
    shift = total % 26
    
    # Penjelasan detail untuk UI
    penjelasan = f"""
    **Rumus:** (Huruf Lagu + Menit) mod 26
    <br>• Huruf '{judul_lagu}': {jumlah_huruf}
    <br>• Menit '{durasi_menit}': {nilai_durasi}
    <br>• Total: {total}
    <br>• **Shift Key:** {total} mod 26 = **{shift}**
    """
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
    msg_lst = list(text)
    key_lst = list(key)
    num_cols = len(key)
    num_rows = int(math.ceil(msg_len / num_cols))
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
    # Mapping Simbol Unik (Nuansa Alien/Kriptik)
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

# --- UI UTAMA ---

st.title("KRIPTOGRAFI")
st.markdown("<h5 style='color: #7B1FA2;'>Kombinasi Substitusi Lagu, Transposisi, dan Simbol</h5>", unsafe_allow_html=True)
st.markdown("---")

# Layout Kolom untuk Input
col_input1, col_input2 = st.columns([1, 2])

with col_input1:
    st.markdown("### Konfigurasi Kunci")
    with st.container():
        # Input Judul Lagu
        judul_lagu = st.text_input("🎵 Judul Lagu", "Separuh Nafas")
        # Input Durasi
        durasi = st.text_input("⏱️ Durasi (misal 4.14)", "4.14")
        # Input Kunci Transposisi
        kunci_transposisi = st.text_input("🔢 Kunci Transposisi (Maks 4 digit)", "3142", max_chars=4)

with col_input2:
    st.markdown("### Pesan Rahasia")
    plaintext = st.text_area("Masukkan Plaintext di sini:", "AISYAH NUR MAYA", height=200)

st.markdown("<br>", unsafe_allow_html=True)

# Tombol Proses (Full Width)
if st.button(" PROSES ENKRIPSI SEKARANG "):
    if not plaintext or not judul_lagu or not durasi or not kunci_transposisi:
        st.error("⚠️ Mohon lengkapi semua kolom input!")
    else:
        # --- PROSES ---
        shift_val, info_rumus = hitung_shift_key(judul_lagu, durasi)
        
        # 1. Substitusi
        cipher_1 = enkripsi_substitusi(plaintext, shift_val)
        
        # 2. Transposisi
        cipher_2 = enkripsi_transposisi(cipher_1, kunci_transposisi)
        
        # 3. EKP
        cipher_final = enkripsi_ekp(cipher_2)
        
        st.markdown("---")
        st.subheader("Hasil Enkripsi Bertahap")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown(f"""
            <div class="custom-box">
                <h4 style="color:#4A148C;">1. Metode Substitusi</h4>
                <div style="font-size:0.9em; color:#555;">{info_rumus}</div>
                <hr style="border-top: 1px dashed #BA68C8;">
                <b>Hasil:</b><br>
                <code style="color:#D500F9;">{cipher_1}</code>
            </div>
            """, unsafe_allow_html=True)
            
        with col_res2:
            st.markdown(f"""
            <div class="custom-box">
                <h4 style="color:#4A148C;">2. Metode Transposisi</h4>
                <div style="font-size:0.9em; color:#555;">
                Menggunakan kunci kolom: <b>{kunci_transposisi}</b><br>
                Padding karakter: '_'
                </div>
                <hr style="border-top: 1px dashed #BA68C8;">
                <b>Hasil:</b><br>
                <code style="color:#D500F9;">{cipher_2}</code>
            </div>
            """, unsafe_allow_html=True)
            
        with col_res3:
            st.markdown(f"""
            <div class="custom-box" style="background-color: #E1BEE7; border-left: 5px solid #4A148C;">
                <h4 style="color:#4A148C;">3. Metode EKP (Final)</h4>
                <div style="font-size:0.9em; color:#555;">
                Ekspansi ke simbol Polialfanumerik.
                </div>
                <hr style="border-top: 1px dashed #BA68C8;">
                <b>OUTPUT AKHIR:</b><br>
                <code style="color:#000; font-weight:bold; font-size:1.2em;">{cipher_final}</code>
            </div>
            """, unsafe_allow_html=True)

        # Area Copy Hasil Akhir
        st.markdown("### 📋 Salin Hasil Akhir")
        st.text_area("Ciphertext:", cipher_final, height=70)

# Spacer agar konten tidak tertutup footer
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        create by Aisyah Nur Maya Silviyani
    </div>
""", unsafe_allow_html=True)
