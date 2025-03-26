"""Prompt for the router chain in the multi-retrieval qa chain."""

GET_INTENT_ROUTER = """\
Given a query, find the intent in single word out of specified candidate prompts.
You will be given the names of the available systems and description 

For Example: 
Query: what is health check of app1 
Answer : "mcp"

Query: How many servers available in US west 
Answer : "CI"

<< FORMATTING >>
{{{{
    "destination": string \\ name of the question answering system to use or "DEFAULT"

}}}}

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR \
it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.


<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT >>
"""
