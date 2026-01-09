import streamlit as st
import math

# --- LOGIKA 1: SUBSTITUSI (MODIFIED CAESAR) ---
def hitung_shift_key(judul_lagu, durasi_menit):
    # 1. Hitung jumlah huruf judul lagu (hapus spasi agar akurat)
    jumlah_huruf = len(judul_lagu.replace(" ", ""))
    
    # 2. Proses durasi (hilangkan titik, ubah ke integer)
    # Contoh: "4.14" -> "414" -> 414
    durasi_bersih = durasi_menit.replace(".", "")
    if not durasi_bersih.isdigit():
        return 0, "Error: Durasi harus berupa angka (contoh: 4.14)"
    nilai_durasi = int(durasi_bersih)
    
    # 3. Rumus: (Jumlah Huruf + Nilai Durasi) MOD 26
    total = jumlah_huruf + nilai_durasi
    shift = total % 26
    
    return shift, f"Rumus: ({jumlah_huruf} huruf + {nilai_durasi}) % 26 = {shift}"

def enkripsi_substitusi(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            # Geser karakter
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result += shifted_char
        else:
            result += char
    return result

# --- LOGIKA 2: TRANSPOSISI (COLUMNAR) ---
def enkripsi_transposisi(text, key):
    # Key harus string angka, misal "3142"
    if not key.isdigit():
        return text # Kembalikan text asli jika key salah
    
    msg_len = float(len(text))
    msg_lst = list(text)
    key_lst = list(key) # ['3', '1', '4', '2']
    
    # Mengurutkan key untuk menentukan urutan baca kolom
    # Col_order akan berisi index asli. Misal key "3142" -> sorted "1234"
    # Urutan pengambilan kolom berdasarkan nilai angkanya
    
    # Hitung jumlah kolom dan baris
    num_cols = len(key)
    num_rows = int(math.ceil(msg_len / num_cols))
    
    # Isi padding jika kurang
    num_empty = (num_rows * num_cols) - len(msg_lst)
    msg_lst.extend(['_'] * num_empty) # Gunakan _ sebagai padding
    
    # Buat matrix
    matrix = [msg_lst[i * num_cols: (i + 1) * num_cols] for i in range(num_rows)]
    
    ciphertext = ""
    # Baca kolom berdasarkan urutan angka kunci (1 dulu, lalu 2, dst)
    # Kita butuh index dari key yang sudah diurutkan
    key_with_index = sorted([(k, i) for i, k in enumerate(key_lst)])
    
    for _, k_index in key_with_index:
        for row in matrix:
            ciphertext += row[k_index]
            
    return ciphertext

# --- LOGIKA 3: METODE EKP (CUSTOM SIMBOL) ---
def enkripsi_ekp(text):
    # Ini adalah simulasi EKP (Ekspansi Karakter). 
    # Logika: Mengubah 1 huruf menjadi simbol/kombinasi aneh.
    # Anda bisa mengedit mapping ini sesuai aturan "Ekspansi" Anda.
    ekp_map = {
        'A': '∆', 'B': 'ß', 'C': '©', 'D': '∂', 'E': '€',
        'F': 'ƒ', 'G': '6', 'H': '#', 'I': '!', 'J': '¿',
        'K': 'x', 'L': '£', 'M': 'µ', 'N': 'π', 'O': 'Ø',
        'P': '¶', 'Q': '9', 'R': '®', 'S': '$', 'T': '†',
        'U': 'µ', 'V': '√', 'W': '∑', 'X': '×', 'Y': '¥', 'Z': 'Ω',
        ' ': '_',  # Spasi jadi underscore
        '_': '~'   # Padding transposisi jadi tilde
    }
    
    hasil = ""
    for char in text:
        upper_char = char.upper()
        if upper_char in ekp_map:
            hasil += ekp_map[upper_char]
        else:
            # Jika tidak ada di map, ubah jadi hex code agar terlihat kriptik
            hasil += f"\\x{ord(char):02x}"
            
    return hasil

# --- UI STREAMLIT ---
st.set_page_config(page_title="Crypto Model EKP", layout="wide")

st.title("🔐 Kriptografi Hybrid: Substitusi + Transposisi + EKP")
st.write("Dibuat khusus untuk model kriptografi custom.")

with st.sidebar:
    st.header("Konfigurasi Kunci")
    st.markdown("### 1. Kunci Substitusi (Lagu)")
    judul_lagu = st.text_input("Judul Lagu", "Separuh Nafas")
    durasi = st.text_input("Durasi (Contoh: 4.14)", "4.14")
    
    st.markdown("---")
    st.markdown("### 2. Kunci Transposisi")
    kunci_transposisi = st.text_input("Kunci Angka (Maks 4 digit)", "3142", max_chars=4)

st.header("Input Pesan")
plaintext = st.text_area("Masukkan Plaintext", "AISYAH NUR MAYA")

if st.button("PROSES ENKRIPSI"):
    if not plaintext or not judul_lagu or not durasi or not kunci_transposisi:
        st.error("Mohon lengkapi semua input!")
    else:
        st.markdown("---")
        
        # --- TAHAP 1 ---
        shift_val, info_rumus = hitung_shift_key(judul_lagu, durasi)
        cipher_1 = enkripsi_substitusi(plaintext, shift_val)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("1. Tahap Substitusi")
            st.info(info_rumus)
            st.success(f"Shift: {shift_val}")
            st.code(cipher_1)
            
        # --- TAHAP 2 ---
        cipher_2 = enkripsi_transposisi(cipher_1, kunci_transposisi)
        
        with col2:
            st.subheader("2. Tahap Transposisi")
            st.info(f"Menggunakan Key: {kunci_transposisi}")
            st.warning("Padding '_' ditambahkan jika perlu.")
            st.code(cipher_2)
            
        # --- TAHAP 3 ---
        cipher_final = enkripsi_ekp(cipher_2)
        
        with col3:
            st.subheader("3. Tahap EKP (Final)")
            st.info("Metode Ekspansi Karakter Polialfanumerik")
            st.error("Output Simbol:")
            st.code(cipher_final)

        st.markdown("---")
        st.markdown("### Hasil Akhir:")
        st.text_area("Copy hasil di sini:", cipher_final, height=100)
