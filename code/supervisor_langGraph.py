from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Union
from langgraph.graph import StateGraph, END
from connect_to_mcp_server import response_from_mcp_server
from find_rca import find_rca_with_llm
from infer_from_static_data import query_dataframe_static_data
from query_observablity_metrics import query_dataframe
from read_from_knowledge_base import search_knowledge_base


# 1. Define the state
@dataclass
class AgentState:
    query: str
    knowledge_base_answer: str = field(default=None)
    is_good_answer: bool = field(default=False)
    static_data_tool_output: str = field(default=None)
    mcp_server_tool_output: str = field(default=None)
    rca_tool_output: str = field(default=None)
    observability_tool_output: str = field(default=None)
    answer: str = field(default=None)  #

# 2. Define the nodes

async def check_knowledge_base(state: AgentState) -> Dict[str, Any]:
    """checking a knowledge base."""
    print("Checking Knowledge Base...")
    answerfromkb = search_knowledge_base(state.query)

    if not "No Answer" in answerfromkb:
        answer = answerfromkb
        is_good = True
    else:
        answer = None
        is_good = False
    return {**state.__dict__, "knowledge_base_answer": answer, "is_good_answer": is_good}

async def run_mcp_server_tool(state: AgentState) -> Dict[str, Any]:
    """running the MCP Server Tool."""
    print("Running MCP Server Tool...")
    output =  response_from_mcp_server(state.query)
    print(output)
    return {**state.__dict__,"mcp_server_tool_output": output}

async def run_rca_tool(state: AgentState) -> Dict[str, Any]:
    """Simulates running the RCA Tool."""
    print("Running RCA Tool...")

    output = f"RCA Tool analysis for '{state.query}':"+ find_rca_with_llm(state.query)
    print(output)
    return {**state.__dict__,"rca_tool_output": output}
async def run_static(state: AgentState) -> Dict[str, Any]:
    """Simulates running the static content"""
    print("Running static...")

    output = query_dataframe_static_data(state.query)
    print(output)
    return {**state.__dict__,"static_data_tool_output": output}

async def run_observability_tool(state: AgentState) -> Dict[str, Any]:
    """Simulates running the Observability Tool."""
    print("Running Observability Tool...")

    output = query_dataframe(state.query)
    return {**state.__dict__,"observability_tool_output": output}

async def final_output(state: AgentState) -> Dict[str, Any]:
    """Displays the final output."""
    print("\n--- Final Output ---")
    answer = 'Sorry can not answer your question'
    if state.knowledge_base_answer:
        print(f"Knowledge Base Answer: {state.knowledge_base_answer}")
        answer = state.knowledge_base_answer
    if state.mcp_server_tool_output:
        print(f"MCP Server Tool Output: {state.mcp_server_tool_output}")
        answer =  state.mcp_server_tool_output
    if state.rca_tool_output:
        print(f"RCA Tool Output: {state.rca_tool_output}")
        answer = state.rca_tool_output
    if state.observability_tool_output:
        print(f"Observability Tool Output: {state.observability_tool_output}")
        answer = state.observability_tool_output
    if state.static_data_tool_output:
        answer = state.static_data_tool_output

    return {**state.__dict__ , "answer": answer}

# 3. Define the supervisor logic (conditional function)
def should_end_or_invoke_tool(state: AgentState) -> str:
    """Supervisor logic to decide whether to end or invoke a tool."""
    print("Supervisor checking the knowledge base answer...")
    query = state.query
    if state.is_good_answer:
        print("Knowledge base provided a good answer. Ending.")
        return "end"
    elif "health" in query.lower() or "stop" in query.lower() or "restart" in query.lower() or "start" in query.lower() or "up" in query.lower() or "down" in query.lower() or "running" in query.lower() :
        print("Knowledge base answer not good. Query suggests using MCP Server Tool.")
        return "mcp_server_tool"
    elif "rca" in query.lower():
        print("Knowledge base answer not good. Query suggests using RCA Tool.")
        return "rca_tool"
    elif "memory" in query.lower() or "observability" in query.lower():
        print("Knowledge base answer not good. Query suggests using Observability Tool.")
        return "observability_tool"
    elif "incident" in query.lower() or "resources" in query.lower() or "dependencies" in query.lower() :
        print("Knowledge base answer not good. Query suggests using MCP Server Tool.")
        return "static_data"
    else:
        print("Knowledge base answer not good. No specific tool suggested in the query. Ending.")
        return "static_data" # Or you could have a default tool or another path


# 4. Create the LangGraph
workflow = StateGraph(AgentState)

# 5. Add the nodes
workflow.add_node("check_kb", check_knowledge_base)
workflow.add_node("static_data", run_static)
workflow.add_node("mcp_server_tool", run_mcp_server_tool)
workflow.add_node("rca_tool", run_rca_tool)
workflow.add_node("observability_tool", run_observability_tool)
workflow.add_node("final_output", final_output)

# 6. Add the conditional edge (supervisor logic)
workflow.add_conditional_edges(
    "check_kb",
    should_end_or_invoke_tool,
    {
        "end": "final_output",
        "mcp_server_tool": "mcp_server_tool",
        "rca_tool": "rca_tool",
        "observability_tool": "observability_tool",
        "static_data": "static_data"
    }

)

# 7. Add edges from the tool nodes to the final output
workflow.add_edge("mcp_server_tool", "final_output")
workflow.add_edge("rca_tool", "final_output")
workflow.add_edge("observability_tool", "final_output")
workflow.add_edge("static_data", "final_output")
workflow.set_entry_point("check_kb")

graph = workflow.compile()




async def get_answer(user_query):
     return await graph.ainvoke({"query": user_query})


