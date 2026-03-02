import json
import os
from typing import List
from src.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from src.state import AgentState, Question
from src.utils.prompts import PROMPT_QUESTION_GENERATOR

from src.utils.helpers import extract_json

def build_questions(state: AgentState) -> AgentState:
    """
    Node to generate 50 questions in batches.
    """
    llm = LLMFactory.get_llm(temperature=0.4)  # Optimized: balanced creativity & consistency

    num_q = max(1, state.get('num_questions', 50))
    question_types = state.get('question_types', ["Pilihan Ganda"])
    
    # Fallback if somehow empty
    if not question_types:
        question_types = ["Pilihan Ganda"]
        
    print(f"Generating {num_q} Questions of types {question_types} for: {state['topic']}")
    
    # Distribute questions evenly among selected types
    base_count = num_q // len(question_types)
    remainder = num_q % len(question_types)

    batches = []
    for i, q_type in enumerate(question_types):
        count = base_count + (1 if i < remainder else 0)
        if count > 0:
            batches.append({"type": q_type, "count": count})
    
    all_questions: List[Question] = []
    current_id = 1
    
    # Check if RPP exists, otherwise use default
    if state.get('rpp') and 'tujuan_pembelajaran' in state['rpp']:
        goals = ", ".join(state['rpp']['tujuan_pembelajaran'])
    else:
        goals = "Tidak spesifik"

    for batch in batches:
        prompt = PROMPT_QUESTION_GENERATOR.format(
            count=batch['count'],
            type=batch['type'],
            topic=state['topic'],
            grade_level=state['grade_level'],
            goals=goals
        )
        
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            questions_data = extract_json(response.content)
            
            # Post-process to ensure IDs and structure
            if isinstance(questions_data, list):
                for q in questions_data:
                    q['id'] = current_id
                    q['type'] = batch['type'] # Ensure type is robust
                    current_id += 1
                    all_questions.append(q)
            else:
                 print(f"Warning: Batch {batch['type']} returned invalid format (not a list).")
                
        except Exception as e:
            print(f"Error in batch {batch['type']}: {e}")
            print(f"RAW QUESTION RESPONSE: {response.content}")
            state['logs'].append(f"Failed to generate {batch['type']}: {str(e)}")
    
    state['questions'] = all_questions
    state['logs'].append(f"Generated {len(all_questions)} questions.")
    
    return state
