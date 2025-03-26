import json


from langchain.llms import Ollama  # Or ChatOpenAI, etc.
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool


@tool
def find_rca_with_llm(user_query):
    """
    Finds root cause analysis information from log data using an LLM.
    """

    related_logs = []

    with open('../data/application_logs.txt', 'r') as f:
        for line in f:
            log_entry = json.loads(line)
            related_logs.append(log_entry)

    if not related_logs:
        return "No related logs found."

    # Prepare input for LLM
    log_string = json.dumps(log_entry, indent=2)

    llm = Ollama(model="llama2") #Or ChatOpenAI()

    prompt = PromptTemplate(
        input_variables=["log_string"],
        template="""
        Analyze the following logs and provide a root cause analysis (RCA).
        Identify any patterns, correlations, or anomalies that could explain the errors.
        Consider the correlation IDs, user IDs, and timestamps to understand the sequence of events.
        
        return data within 100 words
        

        Logs:
        {log_string}

        RCA:
        """,
    )

    chain = prompt | llm

    try:
        rca = chain.invoke({"log_string": log_string})
        return rca
    except Exception as e:
        return f"An error occurred during LLM processing: {e}"
