import json
import random
import os
from ai_guru.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from ai_guru.state import AgentState, Question
from ai_guru.utils.rag_prompts import PROMPT_EXTRACT_QUESTIONS
from ai_guru.utils.helpers import extract_json
from ai_guru.utils.bank_soal import BankSoalService

def remix_questions(state: AgentState) -> AgentState:
    """
    Node to extract questions from uploaded text and remix them.
    Or fetch from Bank Soal if no text provided but RAG is requested (future feature).
    """
    if not state.get('use_rag') or not state.get('source_text'):
        print("Skipping RAG Remixer (Not requested or no text)")
        return state

    print(f"Remixing Questions from Source Text...")

    # RAG extraction and remixing takes ~45-70s
    llm = LLMFactory.get_llm(temperature=0.35, timeout=90.0)


    # 1. Extract Questions from Text
    source_text = state['source_text'][:500000]  # Truncate text if too long

    prompt = PROMPT_EXTRACT_QUESTIONS.format(text=source_text)

    try:
        # Internal monologue for better reasoning
        print("[DEBUG] Cleaning and validating extracted questions...")
        response = llm.invoke([HumanMessage(content=prompt)])
        extracted_data = extract_json(response.content)

        if not extracted_data:
            state['logs'].append("RAG Extraction returned empty.")
            return state

        state['remixed_questions'] = extracted_data
        state['logs'].append(f"Extracted {len(extracted_data)} questions.")

    except Exception as e:
        state['logs'].append(f"Error in Soal Remixer: {str(e)}")

    return state
