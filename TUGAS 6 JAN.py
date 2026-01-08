import streamlit as st
st.title("Aplikasi Hitung Bangun Datar")

opt = st.selectbox(
  label="Pilih operasi perhitungan",
  options=['Hitung Luas', 'Hitung keliling'] 
)

def pilih_rumus(option):
  allRumus = {}

if (option == 'Hitung Luas'):
  allRumus = hitungluas
else:
  allRumus = hitungkeliling

return allRumus

opt = st.selectbox(
  label="Pilih operasi perhitungan",
  options=['Hitung Luas', 'Hitung Keliling']
)

allRumus = pilih_rumus(opt)

pilih_hitung = st.radio(
  label='Pilih Hitung',
  options=a;;_rumus.keys(),
horizontal=True

inputs = [st.number_input(label, value=0.0) for label in all_rumus[pilih_hitung]["inputan"]

if st.button('Hitung'):
    hasil = all_Rumus[pilih_hitung]["Fungsi"](*inputs)
    st.markdown(f'<h2 style="color:green; text-align:center;">Hasil: {hasil})</h2',
                unsafe_allow_html=True)

# Hitung Luas
def luas_segitiga(a, t):
  return (a * t) / 2
def luas_persegi_panjang(p, l):
  return p * l
def luas_jajar_genjang(a, t):
  return a * t
# Hitung Keliling
def keliling_segitiga(a, b, c):
  return a + b + c
def keliling_persegi_panjang(p, l):
  return 2 * (p + l)
def keliling_jajr_genjang(a, b):
  return 2 * (a + b)

hitungLuas = {
  "Luas Segitiga": {
    "Fungsi": luas_segitiga,
    "Inputan": ['Alas', 'Tinggi']
  },
  "Luas Persegi Panjang": {
    "Fungsi": luas_persegi_panjang,
    "Inputan": ['Panjang', 'Lebar']
  },
  "Luas Jajar Genjang": {
    "Fungsi": luas_jajar_genjang,
    "Inputan": ['Alas', 'Tinggi']
  },
}

hitungKeliling = {
  "Keliling Segitiga": {
    "Fungsi": Keliling_segitiga,
    "Inputan": ['Alas', 'Tinggi']
  },
  "Keliling Persegi Panjang": {
    "Fungsi": Keliling_persegi_panjang,
    "Inputan": ['Panjang', 'Lebar']
  },
  "Keliling Jajar Genjang": {
    "Fungsi": Keliling_jajar_genjang,
    "Inputan": ['Alas', 'Tinggi']
  },
}


