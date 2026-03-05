import json
import os
from typing import List
from ai_guru.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from ai_guru.state import AgentState, Question
from ai_guru.utils.prompts import PROMPT_QUESTION_GENERATOR

from ai_guru.utils.helpers import extract_json
from ai_guru.utils.logger import get_logger

logger = get_logger(__name__)

def build_questions(state: AgentState) -> AgentState:
    """
    Node to generate 50 questions in batches.
    """
    try:
        # Question generation in batches can take ~60-100s
        llm = LLMFactory.get_llm(temperature=0.4, timeout=120.0)

        num_q = max(1, state.get('num_questions', 50))
        question_types = state.get('question_types', ["Pilihan Ganda"])
        
        if not question_types:
            question_types = ["Pilihan Ganda"]
            
        logger.info(f"Generating {num_q} Questions for: {state.get('topic', 'Unknown')}")
        
        base_count = num_q // len(question_types)
        remainder = num_q % len(question_types)

        batches = []
        for i, q_type in enumerate(question_types):
            count = base_count + (1 if i < remainder else 0)
            if count > 0:
                batches.append({"type": q_type, "count": count})
        
        all_questions: List[Question] = []
        current_id = 1
        
        # Check if RPP exists
        goals = "Tidak spesifik"
        if state.get('rpp') and isinstance(state['rpp'], dict):
            tujuan = state['rpp'].get('tujuan_pembelajaran', [])
            if isinstance(tujuan, list) and tujuan:
                goals = ", ".join(tujuan)

        for batch in batches:
            prompt = PROMPT_QUESTION_GENERATOR.format(
                count=batch['count'],
                type=batch['type'],
                topic=state.get('topic', ''),
                grade_level=state.get('grade_level', ''),
                class_level=state.get('class_level', ''),
                goals=goals
            )
            
            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                if not response or not response.content:
                    logger.warning(f"Batch {batch['type']} returned empty response.")
                    continue

                questions_data = extract_json(response.content)
                
                if isinstance(questions_data, list):
                    for q in questions_data:
                        q['id'] = current_id
                        q['type'] = batch['type']
                        current_id += 1
                        all_questions.append(q)
                    logger.info(f"Batch {batch['type']} success: {len(questions_data)} questions.")
                else:
                    logger.error(f"Batch {batch['type']} invalid format: {type(questions_data)}")
                    
            except Exception as batch_err:
                logger.error(f"Error in batch {batch['type']}: {str(batch_err)}")
                state['logs'].append(f"Failed to generate {batch['type']}: AI error.")
        
        state['questions'] = all_questions
        state['logs'].append(f"Generated {len(all_questions)} questions.")
        logger.info(f"Total questions generated: {len(all_questions)}")
        
    except Exception as e:
        logger.exception(f"Critical error in build_questions: {str(e)}")
        state['logs'].append(f"Critical error in question builder.")
    
    return state
