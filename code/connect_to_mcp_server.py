import requests
import json
import re

from langchain.tools import Tool
import ollama
from langchain_core.tools import tool

MCP_SERVER_URL = "http://localhost:8082/mcp"  # Replace with your MCP server's URL

def get_tools():
    """Retrieves tool definitions from the MCP server."""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/tools")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving tools: {e}")
        return None

def execute_action(tool_name, action_name, parameters):
    """Executes an action on a tool via the MCP server."""
    payload = {
        "tool": tool_name,
        "action": action_name,
        "parameters": parameters,
    }

    try:
        response = requests.post(f"{MCP_SERVER_URL}/execute", json=payload)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error executing action: {e}")
        return None

# Example usage

def derive_tool_action_parameters_ollama(user_query, available_tools):
    """
    Derives the tool action and parameters from a user query using LangChain's ZeroShotAgent with Ollama.

    Args:
        user_query (str): The user's natural language query.
        available_tools (dict): A dictionary of available tools and their definitions.

    Returns:
        dict: A dictionary containing the tool name, action name, and parameters, or None if no match is found.
    """

    try:
        # Convert available_tools to LangChain tool format.


        prompt = f"""
               Given the following user query and available tools, give output only in json format with only derived data tool, action, parameters

               User Query: {user_query}

               Available Tools:
               {json.dumps(available_tools, indent=4)}

               Output the result in JSON Object with below data. Do not include any surrounding text or code block markers.
               - "tool": The name of the tool.
               - "action": The name of the action.
               - "parameters": A dictionary of parameters.

               If no suitable tool or action is found, return null.
               """
        output = ollama.generate(
            #    model="deepseek-r1:7b",
            model='llama3.2',
            #    prompt=f"Using this data: {data}. Respond to this prompt: {input}"
            prompt=prompt
        )


        try:
            result = get_clean_json(output.response)
            return result
        except json.JSONDecodeError:
            print(f"LLM response was not valid JSON: {output.response}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_clean_json(llm_output):
    """Cleans up the LLM's output and returns a JSON object."""
    try:
        # Remove code block markers and surrounding text
        json_string = re.sub(r"```json|```", "", llm_output).strip()
        # Parse the JSON string
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


@tool
def response_from_mcp_server(user_message):
    """ Derives response from MCP servers"""
    tools = get_tools()
    result = derive_tool_action_parameters_ollama(user_message, tools)
    print(json.dumps(result, indent=4))
    toolResponse = execute_action(result["tool"], result["action"], result["parameters"])
    return toolResponse.text
