import os
from langchain.agents import Tool, AgentExecutor, ZeroShotAgent
from langchain import LLMChain
# from langchain.llms import OpenAI
import requests
import json

from langchain_ollama import OllamaLLM



def get_app_health(app_name):
    base_url = "http://localhost:8080/health?appName="+app_name

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        health_status_respone = response.text
        return health_status_respone
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"

def app_health_tool(app_name):
    health_data = get_app_health(app_name)
    return health_data

if __name__ == "__main__":
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Replace with your OpenAI API key.
    # llm = OpenAI(temperature=0) #Zero temperature for more deterministic results.

    llm = OllamaLLM(model="llama3.2")

    tools = [
        Tool(
            name="Get App Health",
            func=app_health_tool,
            description="Get App Health given the name of the app name.",
        )
    ]

    prefix = """Answer the following questions as best you can. You have access to the following tools:"""
    suffix = """Begin! Remember to answer in full sentences. {input}"""
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input"],
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True) #verbose=True for debugging.
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    app_name = "app1"
    question = f"What is health check of {app_name}?"

    response = agent_chain.run(question)
    print(response)

    app_name = "app2"
    question2 = f"Get App Health {app_name}"
    response2 = agent_chain.run(question2)
    print(response2)