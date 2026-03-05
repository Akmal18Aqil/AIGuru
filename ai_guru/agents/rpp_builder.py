import json
import os
from ai_guru.config.llm_manager import LLMFactory
from langchain_core.messages import HumanMessage
from ai_guru.state import AgentState
from ai_guru.utils.prompts import PROMPT_RPP_GENERATOR

# Initialize LLM inside function to allow dynamic API key setting
from ai_guru.utils.helpers import extract_json
from ai_guru.utils.logger import get_logger

logger = get_logger(__name__)

def build_rpp(state: AgentState) -> AgentState:
    """
    Node to generate RPP based on the topic.
    """
    try:
        # RPP generation typically takes ~30-60s
        llm = LLMFactory.get_llm(temperature=0.3, timeout=90.0)

        logger.info(f"Generating RPP for: {state.get('topic', 'Unknown')}")
        
        prompt = PROMPT_RPP_GENERATOR.format(
            topic=state.get('topic', ''),
            grade_level=state.get('grade_level', ''),
            subject=state.get('subject', '')
        )
        
        response = llm.invoke([HumanMessage(content=prompt)])
        
        if not response or not response.content:
            logger.error("RPP Generation returned empty response.")
            state['logs'].append("Error: AI returned empty response.")
            return state

        rpp_data = extract_json(response.content)
        state['rpp'] = rpp_data
        state['logs'].append("RPP Generated Successfully.")
        logger.info("RPP Generated Successfully.")
        
    except Exception as e:
        logger.exception(f"Unexpected error in build_rpp: {str(e)}")
        state['logs'].append(f"Error generating RPP: {str(e)}")
    
    return state
