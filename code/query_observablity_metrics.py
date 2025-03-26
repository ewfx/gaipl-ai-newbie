import pandas as pd

import ollama
from langchain_core.tools import tool


@tool
def query_dataframe(user_query):
    """ Get query on Observablity Metrics"""
    data = pd.read_csv("../data/observability_data.csv")
    df = pd.DataFrame(data)
    df_str = df.to_string()
    prompt = f"""
            f"Using this data frame data in string format: {df_str}. Respond to this prompt in single sentence: {user_query} 
    """

    try:

        output = ollama.generate(
            #    model="deepseek-r1:7b",
            model='llama3.2',
            #    prompt=f"Using this data: {data}. Respond to this prompt: {input}"
            prompt=prompt
        )

        return output.response

    except Exception as e:
        return f"An error occurred: {e}"







