from langgraph.graph import StateGraph, END
from ai_guru.state import AgentState
from ai_guru.agents.rpp_builder import build_rpp
from ai_guru.agents.soal_builder import build_questions
from ai_guru.agents.doc_formatter import format_document
from ai_guru.agents.jadwal_builder import build_jadwal # Imported
from dotenv import load_dotenv

load_dotenv()

from ai_guru.agents.soal_remixer import remix_questions

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("rpp_builder", build_rpp)
workflow.add_node("soal_builder", build_questions)
workflow.add_node("soal_remixer", remix_questions)
workflow.add_node("doc_formatter", format_document)
workflow.add_node("jadwal_builder", build_jadwal) # Added node

# --- Conditional Logic ---

def route_start(state):
    # Check for Jadwal Mode first
    if state.get("jadwal_mode"):
        return "jadwal_builder"

    mode = state.get("generation_mode", "all")
    
    if mode == "soal_only":
        # Skip RPP, go straight to Soal
        if state.get("use_rag") and state.get("source_text"):
            return "soal_remixer"
        return "soal_builder"
    
    # Default: Start with RPP
    return "rpp_builder"

def route_after_rpp(state):
    mode = state.get("generation_mode", "all")
    
    if mode == "rpp_only":
        return "doc_formatter" # Skip Soal
        
    # Proceed to Soal Generation
    if state.get("use_rag") and state.get("source_text"):
        return "soal_remixer"
    return "soal_builder"

# --- Edge Definitions ---

# Start Routing
workflow.set_conditional_entry_point(
    route_start,
    {
        "rpp_builder": "rpp_builder",
        "soal_builder": "soal_builder",
        "soal_remixer": "soal_remixer",
        "jadwal_builder": "jadwal_builder"
    }
)

# After RPP Builder
workflow.add_conditional_edges(
    "rpp_builder",
    route_after_rpp,
    {
        "doc_formatter": "doc_formatter",
        "soal_builder": "soal_builder", 
        "soal_remixer": "soal_remixer"
    }
)

workflow.add_edge("soal_builder", "doc_formatter")
workflow.add_edge("soal_remixer", "doc_formatter")
workflow.add_edge("doc_formatter", END)
workflow.add_edge("jadwal_builder", END) # End after jadwal

# Compile
app_graph = workflow.compile()
