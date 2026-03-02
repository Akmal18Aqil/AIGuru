import json
import os
from ai_guru.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from ai_guru.state import AgentState
from ai_guru.utils.jadwal_prompts import PROMPT_JADWAL_BUILDER, PROMPT_CONFLICT_CHECKER
from ai_guru.utils.helpers import extract_json


def build_jadwal(state: AgentState) -> AgentState:
    """
    Node to generate school-wide teaching schedule.
    Uses constraint satisfaction approach via LLM.
    """
    if not state.get('jadwal_mode'):
        print("Skipping Jadwal Builder (Not requested)")
        return state

    print("Generating School Schedule...")

    llm = LLMFactory.get_llm(temperature=0.15)  # Optimized for consistency

    # Format input data for prompt
    teacher_data = json.dumps(state.get('jadwal_teachers', []), indent=2, ensure_ascii=False)
    class_data = json.dumps(state.get('jadwal_classes', []), indent=2, ensure_ascii=False)
    time_slots = state.get('jadwal_time_slots', "Jam 1-8: 07:00-14:00")
    constraints = state.get('jadwal_constraints', "Tidak ada constraint khusus")

    prompt = PROMPT_JADWAL_BUILDER.format(
        teacher_data=teacher_data,
        class_data=class_data,
        time_slots=time_slots,
        constraints=constraints
    )

    try:
        # Internal monologue for better reasoning
        print("[DEBUG] Analyzing constraints and preparing draft schedule...")
        response = llm.invoke([HumanMessage(content=prompt)])
        jadwal_data = extract_json(response.content)

        if isinstance(jadwal_data, list):
            state['jadwal_result'] = jadwal_data
            state['logs'].append(f"Generated {len(jadwal_data)} jadwal entries.")

            # Auto-check conflicts
            state = check_conflicts(state, llm)
        else:
            state['logs'].append("Jadwal generation returned invalid format.")
    except Exception as e:
        state['logs'].append(f"Error in Jadwal Builder: {str(e)}")

    return state


def check_conflicts(state: AgentState, llm) -> AgentState:
    """
    Sub-function to verify generated schedule for conflicts.
    Uses hybrid approach: Deterministic + LLM
    """
    if not state.get('jadwal_result'):
        return state
    
    print("Checking for schedule conflicts...")
    
    # === LAYER 1: Deterministic Hard Conflict Detection ===
    from ai_guru.utils.conflict_detector import detect_hard_conflicts
    hard_conflicts_result = detect_hard_conflicts(state['jadwal_result'])
    
    # === LAYER 2: LLM Soft Conflict Detection ===
    jadwal_json = json.dumps(state['jadwal_result'], indent=2, ensure_ascii=False)
    prompt = PROMPT_CONFLICT_CHECKER.format(jadwal_json=jadwal_json)
    
    soft_conflicts = []
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        llm_result = extract_json(response.content)
        soft_conflicts = llm_result.get('warnings', [])
    except Exception as e:
        print(f"LLM conflict check failed: {e}")
        soft_conflicts = []
    
    # === MERGE RESULTS ===
    merged_conflicts = {
        'has_conflict': hard_conflicts_result['has_conflict'],
        'hard_conflicts': hard_conflicts_result['conflicts'],
        'soft_conflicts': soft_conflicts,
        'total_hard': len(hard_conflicts_result['conflicts']),
        'total_soft': len(soft_conflicts)
    }
    
    state['jadwal_conflicts'] = merged_conflicts
    
    if hard_conflicts_result['has_conflict']:
        state['logs'].append(f"🚨 Found {len(hard_conflicts_result['conflicts'])} HARD conflicts (must fix)!")
    if soft_conflicts:
        state['logs'].append(f"⚠️ Found {len(soft_conflicts)} soft warnings")
    if not hard_conflicts_result['has_conflict'] and not soft_conflicts:
        state['logs'].append("✅ No conflicts detected.")
    
    return state

