# 📄 Panduan Edit Template Dokumen (SiGURU)

Selamat datang! Panduan ini akan membantu Anda mengubah tampilan dokumen (RPP dan Soal) yang dihasilkan oleh SiGURU sesuai dengan keinginan Anda (misal: menambah logo sekolah atau mengubah jenis huruf).

---

## 🚀 Langkah Cepat Mengedit
1.  **Buka File**: Masuk ke folder `templates` dan buka file `template_rpp.docx` (untuk RPP) atau `template_soal.docx` (untuk Soal) menggunakan **Microsoft Word**.
2.  **Desain Sesuka Hati**: Anda bebas mengubah font, warna, ukuran kertas, atau menambahkan gambar/logo sekolah.
3.  **Gunakan "Kode Ajaib"**: Di dalam dokumen, terdapat teks seperti `{{ guru }}`. Ini adalah "kode" yang akan diganti otomatis oleh AI dengan nama guru yang Anda ketik di aplikasi.
4.  **Simpan**: Setelah selesai, cukup klik **Save** (Simpan). Pastikan formatnya tetap `.docx`.

---

## 🔠 Daftar "Kode Ajaib" (Variabel)
Anda bisa salin-tempel kode di bawah ini ke dalam dokumen Word Anda. Pastikan tanda kurungnya lengkap `{{ ... }}`.

### 📚 Untuk RPP (`template_rpp.docx`)
| Kode | Akan Berubah Menjadi... |
| :--- | :--- |
| `{{ topic }}` | Topik atau Materi Pelajaran |
| `{{ subject }}` | Mata Pelajaran (IPA, IPS, dll) |
| `{{ grade }}` | Jenjang (SD, SMP, SMA, Kuliah) |
| `{{ class_level }}` | **(Baru!)** Kelas atau Semester |
| `{{ guru }}` | Nama Anda sebagai Guru |
| `{{ sekolah }}` | Nama Sekolah Anda |
| `{{ tahun }}` | Tahun Ajaran |
| `{{ rpp_tujuan }}` | Daftar Tujuan Pembelajaran |
| `{{ rpp_kegiatan }}` | Langkah-langkah Kegiatan Belajar |
| `{{ rpp_asesmen }}` | Cara Penilaian / Asesmen |

### 📝 Untuk Soal (`template_soal.docx`)
| Kode | Akan Berubah Menjadi... |
| :--- | :--- |
| `{{ topic }}` | Judul atau Topik Ujian |
| `{{ grade }}` | Jenjang Pendidikan |
| `{{ class_level }}` | **(Baru!)** Kelas atau Semester |

---

## 📋 Cara Menampilkan Daftar Soal (Khusus Pengguna Lanjut)
Untuk menampilkan daftar soal secara otomatis, Anda harus menyertakan blok kode berikut di file `template_soal.docx`. **Copy-paste persis seperti ini:**

**1. Untuk Daftar Pertanyaan:**
```text
{% for q in questions %}
{{ q.id }}. {{ q.question }}
   Opsi: {{ q.options }}
{% endfor %}
```

**2. Untuk Kunci Jawaban:**
```text
{% for q in questions %}
{{ q.id }}. {{ q.answer_key }}
{% endfor %}
```

---

## ⚠️ Hal Penting (Agar Tidak Error)
*   **Jangan memotong kode**: Pastikan `{{` dan `}}` berada dalam satu baris dan tidak terpisah oleh enter/jarak yang jauh.
*   **Jangan hapus tanda kurung**: Jika Anda menghapus satu kurung saja, misal menjadi `{ guru }}`, maka sistem akan error.
*   **Gagal Template?**: Jika Anda melakukan kesalahan saat mengedit dan file tidak bisa terbuka, SiGURU akan otomatis menggunakan "format standar" yang sederhana agar tugas Anda tetap selesai.

---

## 💡 Tips Profesional
*   **Tambah Logo**: Klik *Insert > Picture* di Word untuk menambah logo sekolah di bagian header agar dokumen terlihat lebih resmi.
*   **Ganti Font**: Gunakan font seperti *Inter, Roboto,* atau *Arial* agar dokumen mudah dibaca oleh siswa.
*   **Tabel**: Anda bisa memasukkan kode `{{ ... }}` ke dalam tabel Word agar biodata sekolah terlihat lebih rapi.

---
*© 2024 SiGURU AI - Membantu Guru Menjadi Lebih Hebat!*
