#!/bin/sh

# Determine Streamlit port from $PORT environment variable or default to 8501
STREAMLIT_PORT=${PORT:-8501}

echo "Starting FastAPI backend on 0.0.0.0:8000"
uvicorn app:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit frontend on 0.0.0.0:${STREAMLIT_PORT}"
streamlit run ui.py --server.port ${STREAMLIT_PORT} --server.address 0.0.0.0 > streamlit.log 2>&1 &

echo "Starting nginx"
nginx -g "daemon off;"
