import streamlit as st
import pandas as pd
import io

st.title("📅 Cek Nasabah Perlu Perpanjang")

# Upload file
uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # Baca file
        df = pd.read_excel(uploaded_file)
        
        # Tampilkan preview data
        st.subheader("📊 Preview Data:")
        st.dataframe(df.head())
        
        # Pastikan kolom dob ada
        if 'dob' not in df.columns:
            st.error("Kolom 'dob' tidak ditemukan dalam file.")
            st.stop()
        
        # Ubah kolom dob ke datetime
        df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
        df = df.dropna(subset=['dob'])
        
        if df.empty:
            st.error("Tidak ada data valid setelah konversi tanggal.")
            st.stop()
        
        # Ekstrak bulan dari dob
        df['nama_bulan'] = df['dob'].dt.strftime('%B')
        
        # Pilih bulan yang ingin difilter
        bulan_dipilih = st.multiselect(
            "Pilih bulan untuk pengecekan perpanjangan:",
            options=sorted(df['nama_bulan'].unique()),
            default=[]
        )
        
        if bulan_dipilih:
            # Filter berdasarkan bulan yang dipilih
            df_filtered = df[df['nama_bulan'].isin(bulan_dipilih)]
            
            # Tampilkan hasil
            st.subheader("📋 Daftar Nasabah Perlu Perpanjang:")
            st.write(f"Total nasabah: {len(df_filtered)} orang")
            
            if not df_filtered.empty:
                st.dataframe(df_filtered)
                
                # Download sebagai CSV (lebih ringan)
                csv = df_filtered.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download hasil sebagai CSV",
                    data=csv,
                    file_name=f"nasabah_perpanjang.csv",
                    mime="text/csv"
                )
            else:
                st.info("Tidak ada nasabah yang perlu perpanjang di bulan yang dipilih.")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
else:
    st.info("Silakan upload file Excel yang berisi kolom 'dob' dan 'no_pelanggan'.")
    
    # Contoh format data
    st.subheader("📝 Format Data yang Diperlukan:")
    contoh_data = pd.DataFrame({
        'no_pelanggan': ['001', '002', '003'],
        'dob': ['1990-08-15', '1985-09-22', '1992-12-10']
    })
    st.dataframe(contoh_data)
