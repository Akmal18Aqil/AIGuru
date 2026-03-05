# SiGURU AI Assistant

SiGURU adalah asisten AI desktop premium yang dirancang khusus untuk guru di Indonesia. Aplikasi ini membantu otomatisasi pembuatan Modul Ajar (RPP) Kurikulum Merdeka, pembuatan bank soal, dan penyusunan jadwal pelajaran sekolah tanpa bentrok.

## 🚀 Panduan Instalasi di Komputer Baru

### OPSI A: Cara Termudah (Untuk Guru)
1. Pastikan sudah terinstall **Python** (dari python.org).
2. Download/Copy folder ini ke komputer.
3. Klik 2x file **`MULA_SIGURU.bat`**. 
   - *Aplikasi akan otomatis menginstall kelengkapan dan langsung terbuka.*

### OPSI C: Versi Portabel (.EXE) (Paling Mudah)
Jika Anda ingin memberikan aplikasi ke guru dalam bentuk file tunggal `.exe`:
1. Buka Terminal di komputer Anda (yang sudah ada Python).
2. Jalankan perintah: `python build_exe.py`.
3. Tunggu hingga selesai, lalu ambil file di folder **`dist/SiGURU_AI.exe`**.
   - *Guru cukup klik file tersebut tanpa perlu install apapun lagi.*

### OPSI B: Manual (Untuk Developer)
1. Buka Terminal di folder project.
2. Jalankan:
```bash
pip install -r requirements.txt
streamlit run ui/app.py
```

## 🛡️ Fitur Keamanan & Produksi
- **API Key Encryption**: Kunci API disimpan secara terenkripsi (AES-128) di file `.env`.
- **Structured Logging**: Semua aktivitas sistem dicatat di folder `logs/siguru.log`.
- **Auto-Retry**: Sistem secara otomatis mencoba ulang koneksi AI jika terjadi gangguan jaringan.

## 👤 Dukungan & Lisensi
Untuk mendapatkan Lisensi Produksi atau bantuan teknis:
- **Email**: support@siguru.app
- **WhatsApp**: +62-XXX-XXXX-XXXX
