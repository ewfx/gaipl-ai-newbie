INTENT_PROMPT="""
    You are an intent classifier. Your task is to analyze the user's query and determine the most relevant intent from the following list:

    {intents}

    User Query: {query}

    Based on the query, which intent is most appropriate? Respond with only the intent name. Do not respond If no intent is applicable, respond with "unknown".
    """