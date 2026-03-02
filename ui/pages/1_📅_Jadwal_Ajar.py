"""
📅 Jadwal Ajar - School-Wide Schedule Generator
"""
import streamlit as st
import sys
import os
import json
import io
from dotenv import load_dotenv, set_key

load_dotenv()

# Add src to pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ai_guru.agents.jadwal_builder import build_jadwal
from ai_guru.utils.jadwal_exporter import export_jadwal_to_excel, jadwal_to_dataframe

st.set_page_config(page_title="📅 Jadwal Ajar", layout="wide")

# Check auth from main app
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Silakan login di halaman utama terlebih dahulu.")
    st.stop()

st.title("📅 Jadwal Ajar: Generator Jadwal Sekolah")
st.markdown("Buat jadwal pelajaran untuk **seluruh sekolah** dengan AI.")

# --- SIDEBAR: INPUT DATA ---
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    # API Key Persistence
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    current_key = os.getenv("GOOGLE_API_KEY", "")
    
    api_key = st.text_input("Google API Key", value=current_key, type="password")
    
    if api_key and api_key != current_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        # Save to .env (create if not exists)
        if not os.path.exists(env_path):
            with open(env_path, 'w') as f: f.write("")
        set_key(env_path, "GOOGLE_API_KEY", api_key)
        st.success("API Key tersimpan!")
        st.rerun()

    st.divider()
    school_name = st.text_input("Nama Sekolah", "SMPN 1 Jakarta")
    semester = st.text_input("Semester", "Ganjil 2024/2025")
    
    st.divider()
    if st.button("🗑️ Reset Data Jadwal", type="secondary", help="Hapus hasil generate jadwal"):
        if 'jadwal_result' in st.session_state:
            del st.session_state['jadwal_result']
        if 'jadwal_conflicts' in st.session_state:
            del st.session_state['jadwal_conflicts']
        st.rerun()

# --- MAIN CONTENT ---
tab1, tab2, tab3 = st.tabs(["📝 Input Data", "📊 Hasil Jadwal", "⚠️ Konflik"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍🏫 Data Guru")
        st.markdown("Format: Satu guru per baris")
        
        teacher_text = st.text_area(
            "Daftar Guru (Nama | Mapel | Jam/Minggu)",
            """Pak Ahmad | Matematika | 24
Bu Siti | IPA | 20
Pak Budi | B. Indonesia | 22
Bu Rina | B. Inggris | 20
Pak Joko | IPS | 18""",
            height=200
        )
        
    with col2:
        st.subheader("🏫 Data Kelas")
        st.markdown("Format: Satu kelas per baris")
        
        class_text = st.text_area(
            "Daftar Kelas",
            """VII-A
VII-B
VIII-A
VIII-B
IX-A
IX-B""",
            height=200
        )

    st.divider()
    
    st.subheader("⏰ Jam Pelajaran")
    time_slots = st.text_area(
        "Jam Pelajaran Sekolah",
        """Jam 1: 07:00-07:45
Jam 2: 07:45-08:30
Jam 3: 08:30-09:15
Istirahat: 09:15-09:30
Jam 4: 09:30-10:15
Jam 5: 10:15-11:00
Jam 6: 11:00-11:45
Istirahat: 11:45-12:15
Jam 7: 12:15-13:00
Jam 8: 13:00-13:45""",
        height=150
    )
    
    st.divider()
    st.subheader("📋 Ketersediaan Guru (Opsional)")
    st.caption("Format: `Nama Guru | tidak_hadir: Hari` atau `Nama Guru | hanya_hadir: Hari1, Hari2`")
    
    availability_text = st.text_area(
        "Atur Ketersediaan Guru",
        """Pak Joko | tidak_hadir: Rabu
Bu Siti | hanya_hadir: Rabu, Kamis""",
        height=100,
        help="Contoh: 'Pak Ahmad | tidak_hadir: Senin, Jumat' atau 'Bu Rina | hanya_hadir: Selasa, Rabu, Kamis'"
    )
    
    st.divider()
    constraints = st.text_area(
        "Constraint Lainnya (Opsional)",
        "Jumat hanya sampai jam ke-6. Matematika jangan di jam terakhir.",
        height=80
    )
    
    generate_btn = st.button("🚀 Generate Jadwal", type="primary", use_container_width=True)

# --- PROCESSING ---
if generate_btn:
    if not os.environ.get("GOOGLE_API_KEY"):
        st.error("Masukkan Google API Key terlebih dahulu!")
    else:
        # Parse teacher data
        teachers = []
        for line in teacher_text.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                teachers.append({
                    "nama": parts[0],
                    "mata_pelajaran": [parts[1]],
                    "jam_per_minggu": int(parts[2])
                })
        
        # Parse class data
        classes = [{"nama": c.strip(), "jumlah_siswa": 30} for c in class_text.strip().split('\n')]
        
        # Parse availability constraints
        availability_constraints = []
        for line in availability_text.strip().split('\n'):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    nama = parts[0]
                    rule = parts[1]
                    if 'tidak_hadir:' in rule:
                        hari = rule.replace('tidak_hadir:', '').strip()
                        availability_constraints.append(f"{nama} TIDAK BOLEH mengajar di hari {hari}")
                    elif 'hanya_hadir:' in rule:
                        hari = rule.replace('hanya_hadir:', '').strip()
                        availability_constraints.append(f"{nama} HANYA BOLEH mengajar di hari {hari}")
        
        # Combine all constraints
        all_constraints = constraints
        if availability_constraints:
            all_constraints += "\n\n## Ketersediaan Guru:\n" + "\n".join(f"- {c}" for c in availability_constraints)
        
        with st.spinner("🧠 AI sedang menyusun jadwal... (1-2 menit)"):
            # Build state
            state = {
                "jadwal_mode": True,
                "jadwal_teachers": teachers,
                "jadwal_classes": classes,
                "jadwal_time_slots": time_slots,
                "jadwal_constraints": all_constraints,
                "jadwal_result": [],
                "jadwal_conflicts": None,
                "logs": [],
                # Required fields for AgentState compatibility
                "topic": "", "grade_level": "", "subject": "",
                "admin_data": {"sekolah": school_name},
                "source_text": None, "use_rag": False,
                "generation_mode": "jadwal",
                "rpp": None, "questions": [], "status": "Running"
            }
            
            # Run agent
            result = build_jadwal(state)
            
            # Store in session
            st.session_state['jadwal_result'] = result.get('jadwal_result', [])
            st.session_state['jadwal_conflicts'] = result.get('jadwal_conflicts', {})
            st.session_state['jadwal_logs'] = result.get('logs', [])
            st.session_state['school_name'] = school_name
            st.session_state['semester'] = semester
            
        st.success("✅ Jadwal berhasil dibuat! Lihat tab 'Hasil Jadwal'.")

with tab2:
    if 'jadwal_result' in st.session_state and st.session_state['jadwal_result']:
        jadwal = st.session_state['jadwal_result']
        
        st.subheader(f"📊 Jadwal {st.session_state.get('school_name', 'Sekolah')}")
        
        # Convert to DataFrame
        df = jadwal_to_dataframe(jadwal)
        
        if df is not None:
             # --- JADWAL PER GURU (NEW FEATURE) ---
            st.divider()
            col_filter, col_view = st.columns([1, 3])
            
            with col_filter:
                st.subheader("👤 Filter Guru")
                teacher_list = sorted(list(set(df['guru'].unique())))
                selected_teacher = st.selectbox("Pilih Guru:", ["Semua Guru"] + teacher_list)
                
            with col_view:
                if selected_teacher != "Semua Guru":
                    st.write(f"**Jadwal: {selected_teacher}**")
                    df_view = df[df['guru'] == selected_teacher].sort_values(['hari', 'jam_ke'])
                else:
                    st.write("**Semua Jadwal**")
                    df_view = df
                
                st.dataframe(df_view, use_container_width=True, height=500)

            # --- EXPORT LOGIC (FIXED) ---
            st.divider()
            
            # Prepare Export Buffer (In Memory)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                # 1. Master Sheet
                df.to_excel(writer, index=False, sheet_name='Semua Jadwal')
                
                # 2. Sheet per Days
                if 'hari' in df.columns:
                    days = df['hari'].unique()
                    for day in days:
                        df_day = df[df['hari'] == day].sort_values('jam_ke')
                        df_day.to_excel(writer, index=False, sheet_name=str(day)[:31])
                        
                # 3. Sheet per Teacher
                for teacher in teacher_list:
                    df_t = df[df['guru'] == teacher].sort_values(['hari', 'jam_ke'])
                    safe_name = str(teacher).replace(":", "").replace("/", "")[:31]
                    df_t.to_excel(writer, index=False, sheet_name=safe_name)

            col_dl, col_stat = st.columns([1, 1])
            with col_dl:
                st.download_button(
                    label="� Download Excel Lengkap (Per Guru)",
                    data=buffer.getvalue(),
                    file_name=f"Jadwal_{st.session_state.get('school_name', 'Sekolah')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )
                
            with col_stat:
                st.metric("Total Slot", len(jadwal), delta="Generated by AI")

        else:
            st.json(jadwal)
            
    else:
        st.info("Belum ada jadwal. Generate terlebih dahulu di tab 'Input Data'.")

with tab3:
    if 'jadwal_conflicts' in st.session_state and st.session_state['jadwal_conflicts']:
        conflicts = st.session_state['jadwal_conflicts']
        
        if conflicts.get('has_conflict'):
            st.error(f"⚠️ Ditemukan {len(conflicts.get('conflicts', []))} konflik!")
            
            for i, c in enumerate(conflicts.get('conflicts', []), 1):
                with st.expander(f"Konflik #{i}: {c.get('type', 'Unknown')}"):
                    st.write(f"**Detail:** {c.get('detail', '-')}")
                    st.write(f"**Saran:** {c.get('suggestion', '-')}")
            
            if conflicts.get('warnings'):
                st.warning("Peringatan:")
                for w in conflicts['warnings']:
                    st.write(f"- {w}")
        else:
            st.success("✅ Tidak ada konflik terdeteksi!")
    else:
        st.info("Belum ada data konflik. Generate jadwal terlebih dahulu.")

# Logs
with st.expander("📋 Log Proses"):
    if 'jadwal_logs' in st.session_state:
        for log in st.session_state['jadwal_logs']:
            st.write(f"- {log}")
