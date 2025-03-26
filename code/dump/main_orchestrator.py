import ollama
from langchain.chains.llm import LLMChain
from langchain.chains.router import MultiPromptChain, LLMRouterChain
from langchain.chains.router.llm_router import RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate, BasePromptTemplate
from langchain_ollama import OllamaLLM

from connect_to_mcp_server import response_from_mcp_server
from find_rca import find_rca_with_llm
from infer_from_static_data import query_dataframe
from prompts.intent_prompt import INTENT_PROMPT
from prompts.prompt_router import GET_INTENT_ROUTER
import pandas as pd

from read_from_knowledge_base import search_knowledge_base


#data_observablity = pd.read_csv("data/observability_data.csv")
#df_observablity = pd.DataFrame(data_observablity)
#
# data_ci_data = pd.read_csv("data/cmdb_data.csv")
# df_cmdb = pd.DataFrame(data_ci_data)

global user_messag
def get_answer( user_message):
    user_messag = user_message

    default_prompt = PromptTemplate( template ="You are general ChatBot.",input_variables=["user_message"])
    MCP_prompt = PromptTemplate( template ="You are helpful assistant who can  check aqnd answer health of application , and start the web server and stop the web server", input_variables=["user_message"])
    knowledge_prompt = PromptTemplate(template="You are support person who can check content in knowledge base for quick troubleshooting",input_variables=["user_message"])
    df_ci_data_prompt= PromptTemplate(template="You are support person who may check configurable items data use dataframes: {df_cmdb}",input_variables=["user_message"])
    df_rca_data_prompt = PromptTemplate(template="You are support person who wants to know RCA for given issue",
                                       input_variables=["user_message"])
    df_observablity_data_prompt = PromptTemplate(template="You are support person who can answer query on observablity telemetrics. use dataframes: {df_observablity}",
                                       input_variables=["user_message"])

    MCP_chain = LLMChain(llm = OllamaLLM(model="llama3.2"), prompt=MCP_prompt)
    knowledge_chain = LLMChain(llm=OllamaLLM(model="llama3.2"), prompt=knowledge_prompt)
    ci_data_chain = LLMChain(llm=OllamaLLM(model="llama3.2"), prompt=df_ci_data_prompt)
    rca_data_chain = LLMChain(llm=OllamaLLM(model="llama3.2"), prompt=df_rca_data_prompt)
    observablity_data_chain = LLMChain(llm=OllamaLLM(model="llama3.2"), prompt=df_observablity_data_prompt)
    default_chain = LLMChain(llm=OllamaLLM(model="llama3.2"), prompt=default_prompt)

    #destinations = ["mcp", "knowldge", "CI", "RCA", "Observablity", "Default"]
    destination_chains = {
        "mcp": MCP_chain,
        "knowledge": knowledge_chain,
        "configurable_items": ci_data_chain,
        "RCA": rca_data_chain,
        "Observablity": observablity_data_chain,
        "default": default_chain,
    }

    destination_names = list(destination_chains.keys())

    router_template = INTENT_PROMPT.format(intents=destination_names, query=
                                                          user_message)
    prompt = PromptTemplate(
        input_variables=["intents", "query"],
        template=router_template,
    )

    chain = LLMChain(llm=OllamaLLM(model="llama3.2"), prompt=prompt)

    # Format the possible intents for the prompt
    formatted_intents = "\n".join(destination_names)

    destination = chain.run(intents=formatted_intents, query=user_message).strip().lower()  # remove whitespace and make lowercase

    process_destination(destination)

def handle_mcp():
        print("Handling MCP destination...")
        response_from_mcp_server(user_messag)
        # Add your MCP-specific logic here

def handle_knowledge():
        print("Handling Knowledge destination...")
        search_knowledge_base(user_messag)
        # Add your Knowledge-specific logic here

def handle_ci():
        print("Handling CI destination...")
        query_dataframe(user_messag)
        # Add your CI-specific logic here

def handle_rca():
        print("Handling RCA destination...")
        # Add your RCA-specific logic here
        find_rca_with_llm()

def handle_observability():
        print("Handling Observability destination...")
        # Add your Observability-specific logic here

def handle_default():
        print("Handling Default destination...")
        # Add your default logic here

def process_destination(destination):
        """Processes a destination using a switch-like structure."""

        destinations = ["mcp", "knowledge", "ci", "rca", "observability", "default"]

        destination_map = {
            "mcp": handle_mcp,
            "knowledge": handle_knowledge,
            "ci": handle_ci,
            "rca": handle_rca,
            "observability": handle_observability,
            "default": handle_default,
        }

        if destination.lower() in destination_map:
            return destination_map[destination.lower()]()  # Call the corresponding function
        else:
            print(f"Unknown destination: {destination}")




