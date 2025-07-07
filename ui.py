import streamlit as st
import requests

# Streamlit App Configuration
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")

API_URL = "http://localhost:8000"

def main_app():
    st.title("LangGraph Chatbot Agent")
    st.write("Interact with the LangGraph-based agent using this interface.")

    given_system_prompt = st.text_area("Define your AI Agent:", height=68, placeholder="Type your system prompt here...")

    MODEL_NAMES = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "mistral-saba-24b"
    ]

    selected_model = st.selectbox("Select Model:", MODEL_NAMES)

    user_input = st.text_area("Enter your message(s):", height=150, placeholder="Type your message here...")

    if st.button("Submit"):
        if user_input.strip():
            try:
                payload = {"messages": [user_input], "model_name": selected_model, "system_prompt": given_system_prompt}
                response = requests.post(f"{API_URL}/chat", json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if "error" in response_data:
                        st.error(response_data["error"])
                    else:
                        ai_responses = [
                            message.get("content", "")
                            for message in response_data.get("messages", [])
                            if message.get("type") == "ai"
                        ]
                        if ai_responses:
                            st.subheader("Agent Response:")
                            st.markdown(f"**Final Response:** {ai_responses[-1]}")
                        else:
                            st.warning("No AI response found in the agent output.")
                else:
                    st.error(f"Request failed with status code {response.status_code}.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a message before clicking 'Submit'.")

main_app()
