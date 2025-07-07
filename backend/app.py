import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

import mlflow
import time
from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from langchain_community.tools.tavily_search import TavilySearchResults
import redis
import hashlib
import json
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory


# Initialize MongoDBChatMessageHistory for chat history storage
chat_message_history = MongoDBChatMessageHistory(
    session_id="test_session",
    connection_string=os.getenv("MONGODB_CONNECTION_STRING", "mongodb+srv://:@cluster0.2hv7u.mongodb.net/"),
    database_name=os.getenv("MONGODB_DATABASE_NAME", "hyperiondev_db"),
    collection_name=os.getenv("MONGODB_COLLECTION_NAME", "chat_histories"),
)

# Initialize Redis client using REDIS_URL environment variable
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("REDIS_URL environment variable not set")
redis_client = redis.from_url(redis_url)

# Retrieve and set API keys for external tools and services
groq_api_key = ''
os.environ["TAVILY_API_KEY"] = ''

# Predefined list of supported model names
MODEL_NAMES = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "mistral-saba-24b"
]

# Initialize the TavilySearchResults tool with a specified maximum number of results.
tool_tavily = TavilySearchResults(max_results=2)

# Combine the TavilySearchResults and ExecPython tools into a list.
tools = [tool_tavily, ]

# FastAPI application setup with a title
app = FastAPI(title='LangGraph AI Agent')

@app.get("/")
def root():
    return {"message": "LangGraph AI Agent backend is running."}

# Define the request schema using Pydantic's BaseModel
class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]

# User model for registration
class User(BaseModel):
    username: str
    password: str

# Token model for response
class Token(BaseModel):
    access_token: str
    token_type: str

def generate_cache_key(request: RequestState) -> str:
    # Create a unique cache key based on model_name, system_prompt, and messages
    key_data = {
        "model_name": request.model_name,
        "system_prompt": request.system_prompt,
        "messages": request.messages
    }
    key_str = json.dumps(key_data, sort_keys=True)
    return hashlib.sha256(key_str.encode('utf-8')).hexdigest()

@app.post("/chat")
def chat_endpoint(request: RequestState):
    start_time = time.time()
    try:
        if request.model_name not in MODEL_NAMES:
            mlflow.log_metric("chat_success", 0)
            return {"error": "Invalid model name. Please select a valid model."}

        cache_key = generate_cache_key(request)
        cached_response = redis_client.get(cache_key)
        if cached_response:
            # Return cached response if available
            mlflow.log_metric("chat_success", 1)
            mlflow.log_metric("cache_hit", 1)
            mlflow.log_metric("response_time", time.time() - start_time)
            return json.loads(cached_response)

        for msg in request.messages:
            chat_message_history.add_user_message(msg)

        llm = ChatGroq(groq_api_key=groq_api_key, model_name=request.model_name)
        agent = create_react_agent(llm, tools=tools)
        state = {"messages": request.messages}
        result = agent.invoke(state)

        ai_messages = [msg.content for msg in result.get("messages", []) if getattr(msg, "type", None) == "ai"]
        for ai_msg in ai_messages:
            chat_message_history.add_ai_message(ai_msg)

        # Cache the result in Redis with a TTL of 1 hour (3600 seconds)
        # Convert result to a JSON-serializable format before caching
        serializable_result = {
            "messages": [
                {
                    "content": msg.content,
                    "type": getattr(msg, "type", None)
                }
                for msg in result.get("messages", [])
            ]
        }
        redis_client.setex(cache_key, 3600, json.dumps(serializable_result))

        # Log mlflow metrics and artifacts
        mlflow.log_metric("chat_success", 1)
        mlflow.log_metric("cache_hit", 0)
        mlflow.log_metric("response_time", time.time() - start_time)
        mlflow.log_param("model_name", request.model_name)
        mlflow.log_param("system_prompt", request.system_prompt)
        mlflow.log_artifact("app.py")  # Log the current app.py as an artifact for reference

        # Log input messages and AI responses as artifacts
        with open("input_messages.json", "w") as f:
            json.dump(request.messages, f)
        mlflow.log_artifact("input_messages.json")

        with open("ai_responses.json", "w") as f:
            json.dump(ai_messages, f)
        mlflow.log_artifact("ai_responses.json")

        return result
    except Exception as e:
        mlflow.log_metric("chat_success", 0)
        mlflow.log_metric("response_time", time.time() - start_time)
        return {"error": f"Internal server error: {str(e)}"}

@app.get("/chat_history")
def get_chat_history(session_id: str = Query(default="test_session", description="Session ID to retrieve chat history for")):
    history = chat_message_history.get_messages(session_id=session_id)
    return {"session_id": session_id, "chat_history": history}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
