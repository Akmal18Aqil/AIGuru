"""
Deterministic Conflict Detector untuk Jadwal Scheduler

Menggunakan algoritma hash map untuk detect conflicts dengan 100% accuracy.
Tidak bergantung pada LLM parsing.
"""

from typing import List, Dict, Any
from collections import defaultdict


def detect_hard_conflicts(jadwal_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detect hard conflicts (guru/kelas bentrok) secara deterministik
    
    Args:
        jadwal_list: List of schedule entries with keys:
            - hari: str (e.g., "Senin")
            - jam_ke: int (e.g., 1)
            - kelas: str (e.g., "VII-A")
            - mapel: str (e.g., "Matematika")
            - guru: str (e.g., "Pak Ahmad")
    
    Returns:
        {
            'has_conflict': bool,
            'conflicts': [
                {
                    'type': 'guru_bentrok',
                    'guru': 'Pak Ahmad',
                    'hari': 'Senin',
                    'jam_ke': 1,
                    'entries': [entry1, entry2]  # Conflicting entries
                },
                ...
            ]
        }
    """
    conflicts = []
    
    # === CHECK 1: Guru Bentrok ===
    # Build map: (hari, jam_ke, guru) -> [entries]
    guru_schedule = defaultdict(list)
    
    for entry in jadwal_list:
        key = (entry['hari'], entry['jam_ke'], entry['guru'])
        guru_schedule[key].append(entry)
    
    # Find conflicts where guru teaches >1 class at same time
    for (hari, jam_ke, guru), entries in guru_schedule.items():
        if len(entries) > 1:
            conflicts.append({
                'type': 'guru_bentrok',
                'guru': guru,
                'hari': hari,
                'jam_ke': jam_ke,
                'entries': entries,
                'kelas_1': entries[0]['kelas'],
                'kelas_2': entries[1]['kelas'],
                'mapel_1': entries[0]['mapel'],
                'mapel_2': entries[1]['mapel']
            })
    
    # === CHECK 2: Kelas Bentrok ===
    # Build map: (hari, jam_ke, kelas) -> [entries]
    kelas_schedule = defaultdict(list)
    
    for entry in jadwal_list:
        key = (entry['hari'], entry['jam_ke'], entry['kelas'])
        kelas_schedule[key].append(entry)
    
    # Find conflicts where class has >1 teacher at same time
    for (hari, jam_ke, kelas), entries in kelas_schedule.items():
        if len(entries) > 1:
            conflicts.append({
                'type': 'kelas_bentrok',
                'kelas': kelas,
                'hari': hari,
                'jam_ke': jam_ke,
                'entries': entries,
                'guru_1': entries[0]['guru'],
                'guru_2': entries[1]['guru'],
                'mapel_1': entries[0]['mapel'],
                'mapel_2': entries[1]['mapel']
            })
    
    return {
        'has_conflict': len(conflicts) > 0,
        'conflicts': conflicts,
        'total_conflicts': len(conflicts)
    }


def find_conflicting_entries(jadwal_list: List[Dict[str, Any]], hari: str, jam_ke: int, guru: str = None, kelas: str = None) -> List[Dict[str, Any]]:
    """
    Find all entries that conflict with given slot
    
    Args:
        jadwal_list: Schedule entries
        hari: Day
        jam_ke: Period number
        guru: Teacher name (optional)
        kelas: Class name (optional)
    
    Returns:
        List of conflicting entries
    """
    conflicts = []
    
    for entry in jadwal_list:
        if entry['hari'] == hari and entry['jam_ke'] == jam_ke:
            if guru and entry['guru'] == guru:
                conflicts.append(entry)
            if kelas and entry['kelas'] == kelas:
                conflicts.append(entry)
    
    return conflicts


def validate_fix(jadwal_list: List[Dict[str, Any]], proposed_fix: Dict[str, Any]) -> bool:
    """
    Validate if proposed fix creates new conflicts
    
    Args:
        jadwal_list: Current schedule
        proposed_fix: {
            'hari': new day,
            'jam_ke': new period,
            'guru': teacher,
            'kelas': class
        }
    
    Returns:
        True if valid (no conflicts), False if creates new conflict
    """
    # Check if the proposed slot is already taken by this guru or class
    conflicting = find_conflicting_entries(
        jadwal_list,
        proposed_fix['hari'],
        proposed_fix['jam_ke'],
        guru=proposed_fix.get('guru'),
        kelas=proposed_fix.get('kelas')
    )
    
    return len(conflicting) == 0
