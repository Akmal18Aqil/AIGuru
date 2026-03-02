# 📚 Panduan Setup SiGURU untuk Admin IT

## Daftar Isi
1. [Persiapan](#persiapan)
2. [Mendapatkan Google API Key](#mendapatkan-google-api-key)
3. [Setup Aplikasi](#setup-aplikasi)
4. [Verifikasi](#verifikasi)
5. [Troubleshooting](#troubleshooting)

---

## Persiapan

### Sistem Requirement:
- Windows 7 atau lebih baru
- Python 3.9 atau lebih baru
- Koneksi internet (untuk API Google)
- Minimal 2GB RAM

### Yang Dibutuhkan:
✅ Akun Google (gratis)  
✅ Google API Key (gratis untuk quota standar)  
✅ 10-15 menit waktu setup

---

## Mendapatkan Google API Key

> **PENTING:** API Key ini gratis, dan cukup untuk penggunaan normal sekolah. Anda hanya perlu membuat sekali.

### Langkah-langkah:

#### 1. Buka Google AI Studio
- Kunjungi: https://aistudio.google.com/apikey
- Login dengan akun Google sekolah/pribadi Anda

#### 2. Create API Key
- Klik tombol **"Create API Key"**
- Pilih **"Create API key in new project"** (untuk setup baru)
- Google akan generate API key untuk Anda

#### 3. Copy API Key
- Klik tombol **Copy** atau select dan copy manual
- API key berbentuk seperti: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
- **PENTING:** Simpan di tempat aman (jangan share ke orang lain!)

---

## Setup Aplikasi

### Opsi 1: Menggunakan Setup Wizard (REKOMENDASI)

#### Langkah 1: Jalankan Aplikasi
```bash
cd d:\01. Punya Anggota\Akmal\AGENT\AI_Guru_Assistant
streamlit run ui/app.py
```

#### Langkah 2: Setup Wizard akan Muncul Otomatis
- Aplikasi akan mendeteksi bahwa ini instalasi baru
- Anda akan diarahkan ke Setup Wizard

#### Langkah 3: Pilih Tipe Deployment
- Pilih **"Lisensi Organisasi"**
- Klik **"Lanjutkan"**

#### Langkah 4: Masukkan Informasi
- **Nama Sekolah/Lembaga**: Contoh `SDN 01 Jakarta`
- **Google API Key**: Paste API key yang sudah di-copy tadi
- Klik **"Test & Simpan"**

#### Langkah 5: Tunggu Validasi
- Aplikasi akan test koneksi ke Google API (5-10 detik)
- Jika berhasil, Anda akan melihat halaman sukses ✅

#### Langkah 6: Selesai!
- Klik **"Mulai Menggunakan SiGURU"**
- Aplikasi siap digunakan oleh semua guru

---

### Opsi 2: Setup Manual (Untuk yang sudah familiar)

#### 1. Copy Template .env
```bash
cp .env.example .env
```

#### 2. Edit File .env
Buka file `.env` dengan text editor, lalu isi:
```
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX
ORGANIZATION_NAME=Nama Sekolah Anda
```

#### 3. Buat config.json
Buat file `config.json` di root folder dengan isi:
```json
{
  "deployment_type": "organization",
  "organization_name": "Nama Sekolah Anda",
  "setup_completed": true,
  "setup_date": "2026-02-17T15:00:00+07:00",
  "api_key_source": "env"
}
```

#### 4. Jalankan Aplikasi
```bash
streamlit run ui/app.py
```

---

## Verifikasi

### Checklist Setelah Setup:

✅ **File terbuat:**
- [ ] `.env` (berisi API key)
- [ ] `config.json` (konfigurasi aplikasi)

✅ **Status di aplikasi:**
- [ ] Sidebar menampilkan "✅ Lisensi [Nama Sekolah]"
- [ ] Tidak ada warning API key

✅ **Functional test:**
- [ ] Bisa generate RPP di halaman Modul Ajar
- [ ] Bisa generate Jadwal di halaman Smart Scheduler

---

## Troubleshooting

### ❌ "API Key tidak valid"

**Penyebab:**
- API key salah atau tidak lengkap
- Ada spasi/karakter tambahan saat copy-paste
- API key belum aktif

**Solusi:**
1. Periksa kembali API key di Google AI Studio
2. Copy ulang dengan hati-hati ( jangan ada spasi)
3. Paste ulang di Setup Wizard
4. Atau edit langsung file `.env`

---

### ❌ "Konfigurasi API key belum selesai"

**Penyebab:**
- File `config.json` tidak terbuat
- File `.env` tidak ada atau kosong

**Solusi:**
1. Hapus file `config.json` (jika ada)
2. Restart aplikasi
3. Ulangi Setup Wizard dari awal

---

### ❌ "Setup Wizard tidak muncul"

**Penyebab:**
- Sudah pernah setup sebelumnya
- File `config.json` sudah ada

**Solusi:**
1. Hapus file `config.json`
2. Restart aplikasi
3. Setup Wizard akan muncul kembali

---

### ⚠️ "Quota exceeded" atau "Rate limit"

**Penyebab:**
- Sudah mencapai batas free quota Google API
- Terlalu banyak request dalam waktu singkat

**Solusi:**
1. Tunggu beberapa jam (quota akan reset)
2. Untuk quota lebih besar, upgrade ke Google Cloud billing account
3. Hubungi admin Google Cloud untuk increase quota

---

## Distribusi ke Guru-Guru Lain

Setelah setup selesai, **guru lain tidak perlu setup lagi!**

### Cara 1: Shared Installation
- Install aplikasi di 1 komputer lab/kantor
- Semua guru akses dari komputer yang sama
- Sudah siap pakai tanpa setup

### Cara 2: Individual Installation
- Copy folder aplikasi ke komputer masing-masing guru
- Termasuk file `.env` dan `config.json`
- Langsung bisa pakai tanpa input API key

> **CATATAN KEAMANAN:** File `.env` berisi API key yang sensitif. Jangan dibagikan ke luar lembaga!

---

## Best Practices

### ✅ DO:
- Simpan backup API key di tempat aman
- Monitor usage quota secara berkala
- Update aplikasi saat ada versi baru
- Laporkan bug/error ke support

### ❌ DON'T:
- Share API key ke orang luar
- Commit file `.env` ke Git (sudah otomatis di-ignore)
- Gunakan API key untuk aplikasi lain
- Hapus file `config.json` sembarangan

---

## Kontak Support

Jika mengalami kendala:
- 📧 Email: support@siguru.app (placeholder)
- 📱 WhatsApp: +62-XXX-XXXX-XXXX (placeholder)
- 📚 Dokumentasi lengkap: [Link](placeholder)

---

**Terakhir diupdate:** 17 Februari 2026  
**Versi Dokumen:** 1.0  
**Untuk SiGURU:** v1.0.0
