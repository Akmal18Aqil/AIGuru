import json
import os
from ai_guru.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from ai_guru.state import AgentState
from ai_guru.utils.jadwal_prompts import PROMPT_JADWAL_BUILDER, PROMPT_CONFLICT_CHECKER
from ai_guru.utils.helpers import extract_json
from ai_guru.utils.logger import get_logger

logger = get_logger(__name__)

def build_jadwal(state: AgentState) -> AgentState:
    """
    Node to generate school-wide teaching schedule.
    """
    if not state.get('jadwal_mode'):
        return state

    try:
        logger.info("Generating School Schedule...")
        # Jadwal generation is complex — large JSON arrays need more time than default 30s
        llm = LLMFactory.get_llm(temperature=0.15, timeout=120.0)


        # Format input data
        teacher_data = json.dumps(state.get('jadwal_teachers', []), indent=2, ensure_ascii=False)
        class_data = json.dumps(state.get('jadwal_classes', []), indent=2, ensure_ascii=False)
        time_slots = state.get('jadwal_time_slots', "Jam 1-8")
        constraints = state.get('jadwal_constraints', "None")

        prompt = PROMPT_JADWAL_BUILDER.format(
            teacher_data=teacher_data,
            class_data=class_data,
            time_slots=time_slots,
            constraints=constraints
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        
        if not response or not response.content:
            logger.error("Jadwal Builder returned empty response.")
            state['logs'].append("Error: AI scheduler returned no result.")
            return state

        jadwal_data = extract_json(response.content)

        if isinstance(jadwal_data, list):
            state['jadwal_result'] = jadwal_data
            state['logs'].append(f"Successfully generated {len(jadwal_data)} entries.")
            logger.info(f"Jadwal success: {len(jadwal_data)} entries.")
            # Auto-check conflicts
            state = check_conflicts(state, llm)
        else:
            logger.error(f"Jadwal failed: Invalid AI output format.")
            state['logs'].append("Error: AI scheduler output was malformed.")
            
    except ValueError as ve:
        # extract_json raised a user-friendly ValueError — show it in logs
        err_msg = str(ve)
        logger.error(f"JSON parsing failed in build_jadwal: {err_msg}")
        state['logs'].append(f"Error: {err_msg}")
        
    except Exception as e:
        logger.exception(f"Unexpected error in build_jadwal: {str(e)}")
        state['logs'].append(f"Critical error in schedule builder: {str(e)}")

    return state



def check_conflicts(state: AgentState, llm) -> AgentState:
    """
    Sub-function to verify generated schedule for conflicts.
    """
    if not state.get('jadwal_result'):
        return state
    
    try:
        logger.info("Starting conflict detection...")
        
        # 1. Deterministic Check
        from ai_guru.utils.conflict_detector import detect_hard_conflicts
        hard_conflicts_result = detect_hard_conflicts(state['jadwal_result'])
        
        # 2. LLM Soft Check
        jadwal_json = json.dumps(state['jadwal_result'], indent=2, ensure_ascii=False)
        prompt = PROMPT_CONFLICT_CHECKER.format(jadwal_json=jadwal_json)
        
        soft_conflicts = []
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_result = extract_json(response.content)
            soft_conflicts = llm_result.get('warnings', [])
        except Exception as llm_err:
            logger.error(f"Soft conflict check failed: {str(llm_err)}")
        
        # Merge
        merged_conflicts = {
            'has_conflict': hard_conflicts_result.get('has_conflict', False),
            'hard_conflicts': hard_conflicts_result.get('conflicts', []),
            'soft_conflicts': soft_conflicts,
            'total_hard': len(hard_conflicts_result.get('conflicts', [])),
            'total_soft': len(soft_conflicts)
        }
        
        state['jadwal_conflicts'] = merged_conflicts
        
        if merged_conflicts['total_hard'] > 0:
            logger.warning(f"Jadwal has {merged_conflicts['total_hard']} hard conflicts.")
        else:
            logger.info("Jadwal is conflict-free.")
            
    except Exception as e:
        logger.exception(f"Error in check_conflicts: {str(e)}")
    
    return state

