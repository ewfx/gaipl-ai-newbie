from flask import Flask, jsonify, request
import requests
import json
from flask_cors import CORS
from langchain_core.prompts import PromptTemplate
import ollama

from langchain_ollama import OllamaLLM

from connect_to_mcp_server import response_from_mcp_server
from read_from_knowledge_base import search_knowledge_base

import pandas as pd

from supervisor_langGraph import get_answer

app = Flask(__name__)
CORS(app)

def get_answers_mcp(user_message):
    print(user_message)

    prompt = """ Respond to user message :{user_message} with tools :{tools}"""

    output = ollama.generate(
        #    model="deepseek-r1:7b",
        model='llama3.2',
        #    prompt=f"Using this data: {data}. Respond to this prompt: {input}"
        prompt=f"Respond to this prompt {user_message}"
    )

    output = response_from_mcp_server(user_message)
    return output["result"]

@app.route("/chat", methods=["POST"])
def execute_chat():

    data = request.get_json()
    user_message = data["message"]
    # if "advice#" in user_message:
    #     parts = user_message.split("advice#")
    #     if len(parts) > 1:
    #         incident_id = parts[1].strip()  # Remove leading/trailing whitespace
    #         # Optional: Add more robust validation here if needed
    #         if incident_id.lower().startswith("inc"):  # basic validation that incident ID begins with inc.
    #             advice(incident_id)
    #         else:
    #             return "No incident id "  # returns none if it does not begin with inc.


    import asyncio
    response = asyncio.run(get_answer(user_message))

    print(response)
    bot_response = {"response": response.get("answer")}
    return jsonify(bot_response)

@app.route("/incidents", methods=["GET"])
def get_incidents():
    """
        Iterates through incidents in a CSV file and returns incidents with status 't0_do' as JSON.

        Args:
            csv_file_path (str): The path to the CSV file.

        Returns:
            str: A JSON string containing the 't0_do' incidents, or an error message.
        """
    try:
        df = pd.read_csv('../data/incident_data.csv')

        # Filter for incidents with status 't0_do'
        todo_incidents = df[df['Status'] == 'Open']

        # Convert to JSON
        json_result = todo_incidents.to_json(orient='records', indent=4)  # indent for readability

        return json_result

    except FileNotFoundError:
        return json.dumps({"error": f"File not found: {'data/incident_data.csv'}"})
    except KeyError:
        return json.dumps({"error": "CSV file missing 'status' column."})
    except Exception as e:
        return json.dumps({"error": f"An error occurred: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',
            port=8081)  # Make the server accessible from any IP on the network, and allow debugging.

