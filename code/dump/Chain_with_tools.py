import ollama
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM

from connect_to_mcp_server import get_response_from_mcp_server
from find_rca import find_rca_with_llm
from infer_from_static_data import get_static_data_df, query_dataframe_static_data
from query_observablity_metrics import query_dataframe
from read_from_knowledge_base import search_knowledge_base


import os



def get_answer(user_message):


    llm = OllamaLLM(model="llama3.2",temperature=0)  # Temperature 0 for more deterministic output
    #llm = ChatGoogleGenerativeAI(model="gemini-flash", google_api_key="AIzaSyBd8zXrMYEyu1-j_TJLjrIqxAwLO-LlwLQ")
    tools = [search_knowledge_base, query_dataframe_static_data,query_dataframe,get_response_from_mcp_server]
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run(user_message)
