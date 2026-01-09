import streamlit as st
import math

# --- 1. CONFIG ---
st.set_page_config(page_title="Kriptografi", layout="centered")

# --- 2. CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #4b0082 0%, #2e004f 100%);
}
h1, h2, h3, p, label, .stMarkdown, span {
    color: #FFFFFF !important;
}
h1 {
    text-shadow: 0px 0px 10px rgba(255,255,255,0.3);
}
.stTextInput input, .stTextArea textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 8px;
}
div.stButton > button {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    height: 45px;
    font-weight: bold;
    width: 100%;
}
code {
    background-color: #1a1a1a !important;
    color: #00ff00 !important;
}
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA ---

def validasi_durasi(durasi):
    try:
        float(durasi)
        return True
    except ValueError:
        return False

def get_shift_value(judul, durasi):
    judul_clean = ''.join(filter(str.isalpha, judul))
    len_judul = len(judul_clean)
    durasi_clean = durasi.replace(".", "").replace(":", "")
    val_durasi = int(durasi_clean)
    return (len_judul + val_durasi) % 26

def substitution_cipher(text, shift, encrypt=True):
    result = ""
    if not encrypt:
        shift = -shift
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def transposition_cipher(text, key_str, encrypt=True):
    if not key_str.isdigit():
        return text
    key = [int(k) for k in key_str[:4]]
    num_cols = len(key)
    key_order = sorted(range(len(key)), key=lambda k: key[k])

    if encrypt:
        num_rows = math.ceil(len(text) / num_cols)
        padded_text = text.ljust(num_rows * num_cols, '_')
        grid = [list(padded_text[i*num_cols:(i+1)*num_cols]) for i in range(num_rows)]
        cipher = ""
        for col in key_order:
            for row in grid:
                cipher += row[col]
        return cipher.replace('_', '')
    else:
        num_rows = math.ceil(len(text) / num_cols)
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        idx = 0
        for col in key_order:
            for row in range(num_rows):
                if idx < len(text):
                    grid[row][col] = text[idx]
                    idx += 1
        return ''.join(''.join(row) for row in grid).rstrip('_')

def ekp_cipher(text, encrypt=True):
    ekp_map = {
        'A': '@1', 'B': '&2*', 'C': '!3%', 'D': '^4$', 'E': '~5=',
        'F': '+6?', 'G': '<7>', 'H': '#8', 'I': '9!', 'J': '{1}0',
        'K': '1-1-', 'L': '`12~', 'M': ':1;3', 'N': '1,4<', 'O': 'Ø15',
        'P': '_1-6', 'Q': '1=7+', 'R': '1®8', 'S': '#1#9', 'T': '2@0@',
        'U': '2**1', 'V': '%2√2', 'W': '3&2∑', 'X': '2×4!!', 'Y': '^2¥5^', 'Z': '2Ω6$'
    }
    if encrypt:
        return ''.join(ekp_map.get(c.upper(), c) for c in text)
    reverse_map = {v: k for k, v in ekp_map.items()}
    sorted_keys = sorted(reverse_map, key=len, reverse=True)
    hasil, i = "", 0
    while i < len(text):
        for k in sorted_keys:
            if text.startswith(k, i):
                hasil += reverse_map[k]
                i += len(k)
                break
        else:
            hasil += text[i]
            i += 1
    return hasil

# --- 4. TAMPILAN ---

st.markdown("<h1 style='text-align:center;'>ALGORITMA KREASI</h1>", unsafe_allow_html=True)
input_text = st.text_area("Masukkan Teks")

c1, c2, c3 = st.columns(3)
with c1:
    judul_lagu = st.text_input("Judul Lagu")
with c2:
    durasi_lagu = st.text_input("Durasi", placeholder="Contoh: 3.12")
with c3:
    key_trans = st.text_input("Key Transposisi")

col1, col2 = st.columns(2)
with col1:
    enc_btn = st.button("ENKRIPSI")
with col2:
    dec_btn = st.button("DEKRIPSI / RESET")

result = ""

if enc_btn or dec_btn:
    if not validasi_durasi(durasi_lagu):
        st.error("Durasi harus berupa angka dan boleh menggunakan titik.")
    elif input_text and judul_lagu and durasi_lagu and key_trans:
        if enc_btn:
            result = ekp_cipher(
                transposition_cipher(
                    substitution_cipher(input_text, get_shift_value(judul_lagu, durasi_lagu), True),
                    key_trans, True),
                True)
            st.success("Enkripsi Berhasil")
        else:
            result = substitution_cipher(
                transposition_cipher(
                    ekp_cipher(input_text, False),
                    key_trans, False),
                get_shift_value(judul_lagu, durasi_lagu), False)
            st.info("Dekripsi Berhasil")

if result:
    st.code(result)

st.markdown("<div style='text-align:center; font-size:12px; color:#888;'>create by Aisyah Nur Maya Silviyani</div>", unsafe_allow_html=True)
