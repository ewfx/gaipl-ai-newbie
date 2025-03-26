
from langchain_core.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample Knowledge Base (replace with your actual data)

@tool
def search_knowledge_base(query):
    """
     Searches a predefined knowledge base of frequently asked questions (FAQs) and their answers.

     This tool uses TF-IDF vectorization and cosine similarity to find the most relevant answer
     to a user's query. If a match is found, it returns the corresponding answer. If no
     relevant answer is found, it informs the user that an answer could not be located.

     Args:
         query (str): The user's question or query.

     Returns:
         str: The answer from the knowledge base, or a message indicating no answer was found.

     Example:
         User Input: "How do I reset my password?"
         Tool Output: "Knowledge base: To reset your password, go to the login page and click 'Forgot Password'."

         User Input: "What is the capital of Mars?"
         Tool Output: "Knowledge base: I couldn't find an answer to your question."
     """
    knowledge_base = {
        "What is the process for password reset?": "To reset your password, go to the http://reset.passw.com",
        "How do I install the VPN?": "Download the VPN installer from the company intranet and follow the installation instructions.",
        "What are the supported operating systems?": "We support Windows 10, macOS 11+, and Linux distributions.",
        "Troubleshooting slow application performance": "Check your internet connection, close unnecessary applications, and restart your computer.",
        "How to clear browser cache": "In your browser settings, find the option to clear browsing data or cache.",
        "Can you share Password reset URL?": "http://reset.passw.com",
    }
    # Prepare the documents for TF-IDF
    documents = list(knowledge_base.keys()) + [query] # add the query to the documents list

    # Vectorize the documents using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity between the query and the knowledge base documents
    query_vector = tfidf_matrix[-1]  # The last vector is the query vector
    document_vectors = tfidf_matrix[:-1] # All the other vectors are documents

    similarities = cosine_similarity(query_vector, document_vectors).flatten()

    # Find the most similar document
    if max(similarities) > 0.4: # Ensure there is some similarity
      best_match_index = similarities.argmax()
      best_match_question = list(knowledge_base.keys())[best_match_index]
      return knowledge_base[best_match_question]
    else:
      return "Knowledge base:"+"No Answer"


# Example usage



# user_query2 = "What OS is supported?"
# answer2 = search_knowledge_base(user_query2, knowledge_base)
# print(answer2)
#
# user_query3 = "What is the meaning of life?" #query that will not find a match
# answer3 = search_knowledge_base(user_query3, knowledge_base)
# print(answer3)