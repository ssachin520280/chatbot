import streamlit as st
import requests

base_url = "https://flask-hello-world-neon-nu.vercel.app"

def send_query(user_query):
    # response = requests.get("http://localhost:8000/query?" + user_query)
    response = requests.get(base_url + "/query?query=" + user_query)
    if response.status_code == 200:
        response_text = response.json().get("response", "No response")
    else:
        response_text = f"Error: {response.status_code}"
    return response_text

# Function to send a query to the backend server and get the response
def send_query_with_history(user_query, chat_history):
    if chat_history.__len__() > 0:
        combined_query = user_query + " Chat History: " + " ".join([f"{message['sender']}: {message['text']}" for message in chat_history[-5:-1]])
    else:
        combined_query = user_query
    # TODO: correct this to use GET
    response = requests.post("http://localhost:8000/query", json={"query": combined_query})
    if response.status_code == 200:
        response_text = response.json().get("response", "No response")
    else:
        response_text = f"Error: {response.status_code}"
    return response_text

# Streamlit app
st.title("Chat Interface")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input for user query
user_query = st.text_input("Type your query:")

# Button to send the query
if st.button("Send"):
    if user_query:
        # Add user query to chat history
        st.session_state.chat_history.append({"sender": "You", "text": user_query})
        
        # Get response from backend server
        # response_text = send_query_with_history(user_query, st.session_state.chat_history)
        response_text = send_query(user_query)
        
        # Add response to chat history
        st.session_state.chat_history.append({"sender": "Bot", "text": response_text})

# Display chat history
for message in st.session_state.chat_history:
    st.write(f"**{message['sender']}**: {message['text']}")