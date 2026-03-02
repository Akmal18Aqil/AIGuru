import os
from typing import List, Dict, Optional
from supabase import create_client, Client
import json

class BankSoalService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client: Optional[Client] = None
        
        if url and key:
            try:
                self.client = create_client(url, key)
            except Exception as e:
                print(f"Supabase init failed: {e}")

    def save_questions(self, questions: List[Dict], metadata: Dict) -> bool:
        """
        Saves a batch of extracted questions to the bank.
        """
        if not self.client:
            print("No Supabase client available.")
            return False

        records = []
        for q in questions:
            records.append({
                "subject": metadata.get("subject", "Umum"),
                "grade": metadata.get("grade", "Umum"),
                "topic": metadata.get("topic", "Umum"),
                "question_type": q.get("type", "Unknown"),
                "question_text": q.get("question"),
                "options": q.get("options"), # logic to ensure it's JSON serializable
                "answer_key": q.get("answer_key"),
                "taxonomy": q.get("taxonomy", "C?"),
                "source_file": metadata.get("source_file", "Generated")
            })
            
        try:
            self.client.table("question_bank").insert(records).execute()
            return True
        except Exception as e:
            print(f"Error saving to Bank Soal: {e}")
            return False

    def get_random_questions(self, subject: str, grade: str, count: int = 5) -> List[Dict]:
        """
        Retrieves random questions from the bank for remixing.
        """
        if not self.client:
            return []

        try:
            # Note: Supabase/Postgres random ordering usually requires a stored procedure or 
            # fetching more and shuffling in python if the dataset is small.
            # For this MVP, we fetch a larger batch and shuffle in Python.
            
            response = self.client.table("question_bank") \
                .select("*") \
                .eq("subject", subject) \
                .eq("grade", grade) \
                .limit(50) \
                .execute()
            
            data = response.data
            if not data:
                return []
                
            import random
            random.shuffle(data)
            return data[:count]
            
        except Exception as e:
            print(f"Error getting random questions: {e}")
            return []
