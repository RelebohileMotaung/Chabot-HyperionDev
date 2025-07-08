# Chabot-HyperionDev

# LangGraph AI Agent (Full-Stack)

A production-ready AI chat application with FastAPI backend and Streamlit frontend, deployed on Render.

![Architecture Diagram](https://i.imgur.com/your-screenshot.png)

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
   ```
   ```
   docker run -p 8501:8501 -p 8000:8000 langgraph-agent
   ```
   
   # Build image
   ```
   docker build -t yourusername/langgraph-agent .
   ```

   # Tag and push
   ```
   docker tag yourusername/langgraph-agent:latest yourusername/langgraph-agent:v1.0
   ```
   ```
   docker push yourusername/langgraph-agent:v1.0
   ```


   # LangGraph AI Agent (Full-Stack)

![Deployment Pipeline](https://i.imgur.com/pipeline-diagram.png)  
*Docker Hub → Render deployment workflow*

## 🚀 Live Deployment
**[Production App on Render](https://chabot-hyperiondev-12.onrender.com/)**  
*Deployed from Docker Hub image*

## 📦 Deployment Architecture
1. **Development**  
   `Dockerfile` → Local testing
2. **Registry**  
   `docker push` → [Docker Hub](https://hub.docker.com/r/yourusername/your-image)
3. **Production**  
   Render pulls from Docker Hub

```mermaid
graph LR
    A[Local Docker Build] --> B[Docker Hub]
    B --> C[Render Service]
    C --> D[(MongoDB Atlas)]
    C --> E[(Redis)]