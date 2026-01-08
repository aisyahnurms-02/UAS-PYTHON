import streamlit as st

# ===============================
# FUNGSI HITUNG LUAS
# ===============================
def luas_segitiga(a, t):
    return (a * t) / 2

def luas_persegi_panjang(p, l):
    return p * l

def luas_jajar_genjang(a, t):
    return a * t


# ===============================
# FUNGSI HITUNG KELILING
# ===============================
def keliling_segitiga(a, b, c):
    return a + b + c

def keliling_persegi_panjang(p, l):
    return 2 * (p + l)

def keliling_jajar_genjang(a, b):
    return 2 * (a + b)


# ===============================
# DICTIONARY RUMUS
# ===============================
hitungLuas = {
    "Luas Segitiga": {
        "Fungsi": luas_segitiga,
        "Inputan": ["Alas", "Tinggi"]
    },
    "Luas Persegi Panjang": {
        "Fungsi": luas_persegi_panjang,
        "Inputan": ["Panjang", "Lebar"]
    },
    "Luas Jajar Genjang": {
        "Fungsi": luas_jajar_genjang,
        "Inputan": ["Alas", "Tinggi"]
    }
}

hitungKeliling = {
    "Keliling Segitiga": {
        "Fungsi": keliling_segitiga,
        "Inputan": ["Sisi A", "Sisi B", "Sisi C"]
    },
    "Keliling Persegi Panjang": {
        "Fungsi": keliling_persegi_panjang,
        "Inputan": ["Panjang", "Lebar"]
    },
    "Keliling Jajar Genjang": {
        "Fungsi": keliling_jajar_genjang,
        "Inputan": ["Sisi A", "Sisi B"]
    }
}


# ===============================
# STREAMLIT UI
# ===============================
st.title("Aplikasi Hitung Bangun Datar")

opt = st.selectbox(
    "Pilih operasi perhitungan",
    ["Hitung Luas", "Hitung Keliling"]
)

def pilih_rumus(option):
    if option == "Hitung Luas":
        return hitungLuas
    else:
        return hitungKeliling

all_rumus = pilih_rumus(opt)

pilih_hitung = st.radio(
    "Pilih Bangun",
    list(all_rumus.keys()),
    horizontal=True
)

inputs = [
    st.number_input(label, min_value=0.0)
    for label in all_rumus[pilih_hitung]["Inputan"]
]

if st.button("Hitung"):
    hasil = all_rumus[pilih_hitung]["Fungsi"](*inputs)
    st.markdown(
        f"<h2 style='color:green; text-align:center;'>Hasil: {hasil}</h2>",
        unsafe_allow_html=True
    )


