import pandas as pd

def find_available_slots(df: pd.DataFrame, teacher: str, kelas: str, all_days=None, max_slots=8):
    """
    Finds available time slots (Hari, Jam Ke) where BOTH the teacher and the class are free.
    
    Args:
        df: The schedule DataFrame.
        teacher: Name of the teacher.
        kelas: Name of the class (e.g., 'VII-A').
        all_days: List of days to consider (default: ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']).
        max_slots: Maximum number of slots per day.

    Returns:
        List of tuples: [('Senin', 1), ('Selasa', 3), ...] representing free slots.
    """
    if all_days is None:
        all_days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']

    # 1. Identify Busy Slots for Teacher
    teacher_busy = set()
    if 'guru' in df.columns:
        teacher_schedule = df[df['guru'] == teacher]
        for _, row in teacher_schedule.iterrows():
            teacher_busy.add((row['hari'], row['jam_ke']))

    # 2. Identify Busy Slots for Class
    class_busy = set()
    if 'kelas' in df.columns:
        class_schedule = df[df['kelas'] == kelas]
        for _, row in class_schedule.iterrows():
            class_busy.add((row['hari'], row['jam_ke']))

    # 3. Find Free Slots
    free_slots = []
    for day in all_days:
        for jam in range(1, max_slots + 1):
            slot = (day, jam)
            # If neither teacher nor class is busy, it's a valid candidate
            if slot not in teacher_busy and slot not in class_busy:
                free_slots.append(slot)

    return free_slots
