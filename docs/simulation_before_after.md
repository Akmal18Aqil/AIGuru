# Simulation: Before vs After

## Jadwal Builder

### **Before**
```json
{
  "hari": "Senin",
  "jam_ke": 1,
  "kelas": "VIIA",
  "mapel": "Matematika",
  "guru": "Budi"
}
```
*Penjelasan tambahan: Jadwal sudah optimal.*

### **After**
```json
{
  "hari": "Senin",
  "jam_ke": 1,
  "kelas": "VIIA",
  "mapel": "Matematika",
  "guru": "Budi"
}
```
*Hanya JSON, tanpa penjelasan tambahan.*

---

## Soal Remixer

### **Before**
```json
{
  "type": "Pilihan Ganda",
  "question": "Apa ibu kota Indonesia?",
  "options": ["A. Jakarta", "B. Bandung", "C. Surabaya"],
  "answer_key": "A"
}
```
*Penjelasan tambahan: Soal berhasil diekstrak.*

### **After**
```json
{
  "type": "Pilihan Ganda",
  "question": "Apa ibu kota Indonesia?",
  "options": ["A. Jakarta", "B. Bandung", "C. Surabaya"],
  "answer_key": "A"
}
```
*Hanya JSON, tanpa penjelasan tambahan.*