# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Integrated Platform tool for Support is project which helps network or application support ssistant to help his day to day job easier.
It gives single point of console/ chat window which helps in querying CI data dependencies, health check, ansible automation, observablity, RCA


## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
This is a very Real problem, and there are many complexities involved like connectingto different knowledge base system 
and external data sources.
For its Use also its a very Real problem that Support Engineer will face on daily basis. 


## ⚙️ What It Does
Explain the key features and functionalities of your project.

It provides a unified console or chat window offering a single point of access to crucial support functionalities, including:

* **Querying CI data and dependencies**
* **Performing health checks**
* **Executing Ansible automation**
* **Integrating with observability tools**
* **Facilitating Root Cause Analysis (RCA)**

## 🛠️ How We Built It

  UI : HTML, CSS, js
  Python 3.0
      Ollama(model = ""llama3.2") - Local LLM 
      Lang Chain : chaining prompts
      Lang Graph : to construct Workflows
      MCP servers, Agents , Tools, vector store - sin/cosign 
  
  Based on the feature, 
  FAQ and all static contents are stored in knowledge base vector db.
      Health Check and ansible automation are external systm which are wrapped as MCP  and exposed as a server
      health check are obtained by connecting to external servers
      Observablity Data is exposed as tool to query at real time
      Incidents and CI data and dependencies are near real time and hence saved as static files and read from there
      
   
      

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.
   Non Technical: Main Challenges is to actually understand Support system use cases and the data they will be dealing on day to day basis
   Technical challenges are many: 
       new to Python , and new to AI  and LLM concepts
       Largely faced issue while making individual tools/ agents work together as workflow.
       Tried orchestration with multiple method (dumped in "dump" folder :)) but finally was able to do using lang graph.
       still finding the intent of user query was difficult.
   

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/gaipl-ai-newbie.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   Run servers in Flask  (code in /server directory)
     run mcp_server.py : MCP server : Supports MCP to connect to external sources like health check information, execute ansible scripts
                         exposed /getTools to get all tools , /execute_action to execute action in request
     run chat_server.py : server to read chats entered 
                        exposed /chats to read Users message from UI, 
     run health_check.py : Health check server just to mimic MCP tool can connect to external seervers
   
   Open UI : 
       index.html from /UI directory
      Enter queries like "How to reset Password?"
            How many incidents are open
   ```

## 🏗️ Tech Stack
- UI : HTML, CSS, js
  Python 3.0
  Ollama(model = ""llama3.2") - Local LLM
  Lang Chain : chaining prompts
  Lang Graph : to construct Workflows
  MCP servers, Agents , Tools, vector store - sin/cosign

## 👥 Team
- **Pratibha Hegde** - [GitHub](#) | [LinkedIn](#)

