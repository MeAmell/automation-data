import streamlit as st
import pandas as pd
import io

st.title("📅 Cek Nasabah Perlu Perpanjang")

# Upload file
uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Baca file
    df = pd.read_excel(uploaded_file)
    
    # Tampilkan preview data
    st.subheader("📊 Preview Data:")
    st.dataframe(df.head())
    
    # Pastikan kolom dob ada
    if 'dob' not in df.columns:
        st.error("Kolom 'dob' tidak ditemukan dalam file. Pastikan file Excel memiliki kolom 'dob'.")
        st.stop()
    
    # Ubah kolom dob ke datetime
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
    
    # Hapus baris yang dob-nya tidak valid
    df = df.dropna(subset=['dob'])
    
    if df.empty:
        st.error("Tidak ada data valid setelah konversi tanggal.")
        st.stop()
    
    # Ekstrak bulan dari dob
    df['bulan_lahir'] = df['dob'].dt.month
    df['nama_bulan'] = df['dob'].dt.strftime('%B')
    
    # Mapping bulan Indonesia (opsional)
    bulan_mapping = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
        'April': 'April', 'May': 'Mei', 'June': 'Juni',
        'July': 'Juli', 'August': 'Agustus', 'September': 'September',
        'October': 'Oktober', 'November': 'November', 'December': 'Desember'
    }
    
    # Tampilkan statistik bulan
    st.subheader("📈 Statistik Bulan Lahir:")
    bulan_count = df['nama_bulan'].value_counts()
    st.bar_chart(bulan_count)
    
    # Pilih bulan yang ingin difilter
    bulan_dipilih = st.multiselect(
        "Pilih bulan untuk pengecekan perpanjangan:",
        options=sorted(df['nama_bulan'].unique()),
        default=["August", "September"] if "August" in df['nama_bulan'].unique() else []
    )
    
    if bulan_dipilih:
        # Filter berdasarkan bulan yang dipilih
        df_filtered = df[df['nama_bulan'].isin(bulan_dipilih)]
        
        # Tampilkan hasil
        st.subheader("📋 Daftar Nasabah Perlu Perpanjang:")
        st.write(f"Total nasabah: {len(df_filtered)} orang")
        
        if not df_filtered.empty:
            # Tampilkan tabel
            st.dataframe(df_filtered)
            
            # Siapkan data untuk download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Nasabah_Perpanjang')
            output.seek(0)
            
            # Download button
            st.download_button(
                label="⬇️ Download hasil sebagai Excel",
                data=output,
                file_name=f"nasabah_perpanjang_{'-'.join(bulan_dipilih)}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Tidak ada nasabah yang perlu perpanjang di bulan yang dipilih.")
    else:
        st.info("Silakan pilih bulan untuk melihat daftar nasabah yang perlu perpanjang.")

else:
    st.info("Silakan upload file Excel yang berisi data nasabah dengan kolom 'dob' (date of birth) dan 'no_pelanggan'.")
    
    # Tampilkan contoh format data
    st.subheader("📝 Format Data yang Diperlukan:")
    contoh_data = pd.DataFrame({
        'no_pelanggan': ['001', '002', '003'],
        'dob': ['1990-08-15', '1985-09-22', '1992-12-10'],
        'nama': ['John Doe', 'Jane Smith', 'Bob Johnson']  # kolom opsional
    })
    st.dataframe(contoh_data)