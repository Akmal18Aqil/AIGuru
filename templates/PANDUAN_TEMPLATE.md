# 📄 Panduan Mengedit Template DOCX

Template DOCX di folder ini digunakan oleh AI SiGURU untuk mencetak dokumen otomatis.
Sistem menggunakan **Jinja2 via `docxtpl`** untuk mengisi variabel di dalam template.

---

## 📁 Daftar Template

| File | Fungsi |
|---|---|
| `template_rpp.docx` | Template untuk Modul Ajar / RPP |
| `template_soal.docx` | Template untuk Bank Soal & Kunci Jawaban |

---

## ✏️ Cara Mengedit Template

1. Buka file `.docx` di **Microsoft Word**.
2. Temukan placeholder berupa `{{ variabel }}` atau blok `{% for ... %}`.
3. Edit teks, font, warna, atau layout sesuai kebutuhan.
4. **JANGAN** mengubah tanda kurung kurawal `{{ }}` atau syntax Jinja2.
5. Simpan kembali sebagai format `.docx`.

---

## 🔤 Variabel yang Tersedia

### Template RPP (`template_rpp.docx`)

| Variabel | Isi |
|---|---|
| `{{ topic }}` | Topik / Materi Pelajaran |
| `{{ subject }}` | Mata Pelajaran |
| `{{ grade }}` | Jenjang Kelas |
| `{{ sekolah }}` | Nama Sekolah |
| `{{ guru }}` | Nama Guru |
| `{{ nip }}` | NIP Guru |
| `{{ kepsek }}` | Nama Kepala Sekolah |
| `{{ tahun }}` | Tahun Ajaran |
| `{{ date }}` | Tanggal cetak |
| `{{ rpp_tujuan }}` | Tujuan Pembelajaran |
| `{{ rpp_kegiatan }}` | Langkah-langkah Kegiatan |
| `{{ rpp_asesmen }}` | Asesmen / Penilaian |

---

### Template Soal (`template_soal.docx`)

| Variabel | Isi |
|---|---|
| `{{ topic }}` | Topik / Judul Soal |
| `{{ subject }}` | Mata Pelajaran |
| `{{ grade }}` | Jenjang Kelas |
| `{{ sekolah }}` | Nama Sekolah |

#### Loop Soal (wajib ada persis seperti ini):

```
{% for q in questions %}
{{ q.id }}. {{ q.question }}
{% for opt in q.options %}
- {{ opt }}
{% endfor %}
{% endfor %}
```

#### Loop Kunci Jawaban:

```
{% for q in questions %}
{{ q.id }}. {{ q.answer_key }} (Taksonomi: {{ q.taxonomy }})
{% endfor %}
```

#### Properti Setiap Soal (`q`):

| Properti | Isi |
|---|---|
| `q.id` | Nomor soal |
| `q.question` | Pertanyaan |
| `q.type` | Jenis soal (Pilihan Ganda, Isian, dll) |
| `q.options` | Daftar opsi jawaban A, B, C, D (bisa kosong untuk non-PG) |
| `q.answer_key` | Kunci jawaban |
| `q.taxonomy` | Taksonomi Bloom (C1-C6) |
| `q.difficulty` | Tingkat kesulitan (Mudah/Sedang/Sulit) |

---

## ⚠️ Aturan Penting

> **WAJIB:** Jangan pisah-pisahkan tag Jinja ke baris atau paragraf terpisah yang tidak berurutan. Contoh yang **salah**:
> ```
> {% for q  (paragraf 1)
> in questions %}  (paragraf 2)
> ```
> Harus dalam **satu run/paragraf** yang sama di Word.

> **TIPS:** Gunakan fitur "Find & Replace" di Word (`Ctrl+H`) untuk melihat apakah ada tag yang terpotong secara tidak sengaja.

> **JIKA TEMPLATE GAGAL:** Sistem akan otomatis menggunakan fallback python-docx untuk tetap menghasilkan dokumen walau tampilannya lebih sederhana.

---

## 🛠️ Cara Membuat Template Baru dari Nol

1. Buat dokumen Word kosong baru.
2. Desain layout sesuai kebutuhan (header, footer, logo sekolah, dll).
3. Tambahkan placeholder variabel di posisi yang diinginkan, contoh: `{{ guru }}`.
4. Untuk soal, sisipkan blok loop `{% for q in questions %}` ... `{% endfor %}`.
5. Simpan sebagai `template_rpp.docx` atau `template_soal.docx` (ganti file yang lama).
6. Restart Streamlit agar template baru terbaca.
