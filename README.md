# Chabot-HyperionDev

# LangGraph AI Agent (Full-Stack)

A production-ready AI chat application with FastAPI backend and Streamlit frontend, deployed on Render.

![Architecture Diagram](https://i.imgur.com/your-screenshot.png) *Replace with actual diagram*

## 🚀 Live Deployment
**[View Live App](https://chabot-hyperiondev-12.onrender.com/)**

## ✨ Features
- **AI Agent**: Powered by Groq's LLM with LangGraph orchestration
- **Caching**: Redis for response caching (1-hour TTL)
- **History**: MongoDB chat history persistence
- **Production-Ready**:
  - Docker containerization
  - NGINX reverse proxy
  - MLflow monitoring

## 🛠 Tech Stack
| Component       | Technology |
|-----------------|------------|
| Backend         | FastAPI (Python) |
| Frontend        | Streamlit |
| Database        | MongoDB Atlas |
| Cache           | Redis |
| Deployment      | Render |
| Infrastructure  | Docker, NGINX |

## 📦 Repository Structure


## 🖥 Local Development
1. Clone repo:
   ```bash
   git clone https://github.com/RelebohileMotaung/Chabot-HyperionDev.git
   cd your-repo
   ```

   ```
2. docker build -t langgraph-agent .
   docker run -p 8501:8501 -p 8000:8000 langgraph-agent
   ```