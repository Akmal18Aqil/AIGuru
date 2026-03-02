from typing import List, Dict, TypedDict, Optional, Any
import os
import json

class Question(TypedDict):
    id: int
    type: str  # 'pilihan_ganda', 'isian', 'uraian'
    question: str
    options: Optional[List[str]]  # For multiple choice
    answer_key: str
    taxonomy: str  # 'C1' to 'C6'

class RPPData(TypedDict):
    tujuan_pembelajaran: List[str]
    langkah_kegiatan: str  # Markdown/Text
    asesmen: str

class JadwalEntry(TypedDict):
    hari: str           # Senin, Selasa, ...
    jam_ke: int         # 1-8
    waktu: str          # 07:00-07:45
    kelas: str          # VII-A, VIII-B
    mata_pelajaran: str
    guru: str
    durasi_menit: int

class TeacherData(TypedDict):
    nama: str
    mata_pelajaran: List[str]
    jam_per_minggu: int

class ClassData(TypedDict):
    nama: str           # VII-A
    jumlah_siswa: int

class AgentState(TypedDict):
    topic: str
    grade_level: str # 'SD', 'SMP', 'SMA'
    subject: str     # 'Matematika', 'IPA', etc.
    
    # Administrative Data
    admin_data: Dict[str, str] # {guru, sekolah, nip, kepsek, tahun_ajar}
    
    # RAG Inputs
    source_text: Optional[str] # Text from uploaded PDF/Docx
    use_rag: bool
    
    # Configuration
    generation_mode: str # 'all', 'rpp_only', 'soal_only'
    num_questions: Optional[int]   # Number of questions to generate
    question_types: Optional[List[str]] # List of chosen question types

    # Generated Outputs
    rpp: Optional[RPPData]
    questions: List[Question]
    
    # ===== JADWAL FIELDS (all optional) =====
    jadwal_mode: Optional[bool]
    jadwal_teachers: Optional[List[Any]]
    jadwal_classes: Optional[List[Any]]
    jadwal_time_slots: Optional[str]
    jadwal_constraints: Optional[str]
    jadwal_result: Optional[List[Any]]
    jadwal_conflicts: Optional[Dict[str, Any]]
    
    # Metadata
    status: Optional[str]
    logs: List[str]

def save_api_key(api_key: str, file_path: str = "api_key.json"):
    """Save the API key to a local JSON file."""
    with open(file_path, "w") as f:
        json.dump({"api_key": api_key}, f)
    print(f"API key saved to {file_path}.")

def load_api_key(file_path: str = "api_key.json") -> str:
    """Load the API key from a local JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("api_key", "")
    print(f"No API key found at {file_path}.")
    return ""

