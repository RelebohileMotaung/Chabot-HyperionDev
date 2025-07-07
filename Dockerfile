FROM python:3.10-slim

# Install system dependencies for building packages
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . /app/

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start FastAPI in the background and Streamlit as the main process
RUN chmod +x start_app.sh

CMD ["./start_app.sh"]
