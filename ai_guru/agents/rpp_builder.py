import json
import os
from ai_guru.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from ai_guru.state import AgentState
from ai_guru.utils.prompts import PROMPT_RPP_GENERATOR

# Initialize LLM inside function to allow dynamic API key setting
from ai_guru.utils.helpers import extract_json

def build_rpp(state: AgentState) -> AgentState:
    """
    Node to generate RPP based on the topic.
    """
    llm = LLMFactory.get_llm(temperature=0.3)  # Optimized: lower temp for consistent JSON

    print(f"Generating RPP for: {state['topic']}")
    
    prompt = PROMPT_RPP_GENERATOR.format(
        topic=state['topic'],
        grade_level=state['grade_level'],
        subject=state['subject']
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        rpp_data = extract_json(response.content)
        state['rpp'] = rpp_data
        state['logs'].append("RPP Generated Successfully.")
    except Exception as e:
        state['logs'].append(f"Error generating RPP: {str(e)}")
        print(f"RAW RPP RESPONSE: {response.content}")
    
    return state
