from flask import Flask, jsonify, request
import requests
import json
app = Flask(__name__)
playbooks = {
    "start_web_server": {"file": "restart_web.yml", "vars": ["environment"]},
    "restart_db_service": {"file": "restart_db.yml", "vars": []},
    "stop_web_server": {"file": "stop_web.yml", "vars": ["environment"]},

}
inventory = {
    "production": {"hosts": ["webserver1", "webserver2"]},
    "application_servers": {"hosts": ["appserver1", "appserver2", "appserver3"]},
}

# Example tool definitions (replace with your actual definitions)
tools = {
    "health_check_engine": {
        "description": "Finds the health check of application or webserver",
        "actions": {
            "healthCheck": {
                "description": "Performs a health check.",
                "parameters": {"query": {"app_name": "string", "description": "The application or webserver name"}},
                "output": {"type": "string", "description": "The health check results."},
            }
        },
    },
    "ansible_automation": {
        "description": "Executes an Ansible command to START or STOP server",
        "actions": {
            "restart_web_server": {
                "description": "Restart a application or webserver",
                "parameters": {"query": {"app_name": "string", "description": "The application or webserver name"}},
                "output": {"type": "string", "description": "The Restart results."},
            },
            "stop_web_server": {
                "description": "stops a application or webserver",
                "parameters": {"query": {"app_name": "string", "description": "The application or webserver name"}},
                "output": {"type": "string", "description": "The stop server results."},
            }
            
        },
    },
}

def restartWebServer(app_name):

    return "Playbook"+playbooks["start_web_server"]["file"]+ " is executed to restrt server"
        # runner = ansible_runner.run(
        #     playbook=playbooks["deploy_web_config"]["file"],
        #     inventory=inventory[env]["hosts"],
        #     extravars={"environment": env},
        # )


def stop_web_server(app_name):
        if(app_name is None):
            app_name = 'web-server-1'
        return "Playbook" + playbooks["stop_web_server"]["file"] + "is executed"
        # runner = ansible_runner.run(
        #     playbook=playbooks["deploy_web_config"]["file"],
        #     inventory=inventory[env]["hosts"],
        #     extravars={"environment": env},

@app.route("/mcp/tools", methods=["GET"])
def get_tools():
    """Returns the tool definitions."""
    return jsonify(tools)


        # )


@app.route("/mcp/execute", methods=["POST"])
def execute_action():
    """Executes a tool action."""
    data = request.get_json()
    tool_name = data["tool"]
    action_name = data["action"]
    parameters = data["parameters"]

    if tool_name not in tools or action_name not in tools[tool_name]["actions"]:
        return jsonify({"error": "Invalid tool or action."}), 400

    # Replace this with your actual tool execution logic
    if tool_name == "health_check_engine" and action_name == "healthCheck":
        if parameters.get("app_name") is None:
            parameters["app_name"]= 'web-server-1'
        result = get_app_health(parameters["app_name"]) #Example result.
    elif tool_name == "ansible_automation" and action_name == "restart_web_server":
        if parameters.get("app_name") is None:
            parameters["app_name"] = 'web-server-1'
        result = restartWebServer(parameters["app_name"])  # Example result.
    elif tool_name == "ansible_automation" and action_name == "stop_web_server":
        result = stop_web_server(parameters["app_name"])  # Example result.
    else:
        result = "Action executed."

    return result

def get_app_health(appName):
    if appName is None:
        app_name = 'web-server-1'
    base_url = "http://localhost:8080/health?appName="+appName

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082) #Make the server accessible from any IP on the network, and allow debugging.