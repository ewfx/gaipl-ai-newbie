import pandas as pd

import ollama

def query_dataframe(df, user_query):
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

# Example Usage
data = pd.read_csv("../data/cmdb_data.csv")

df = pd.DataFrame(data)

user_query1 = "How many load balancers are there in US-West region?"
result1 = query_dataframe(df, user_query1)
print(result1)

user_query1 = "How many load balancers are there in US-West region?"
result1 = query_dataframe(df, user_query1)
print(result1)



