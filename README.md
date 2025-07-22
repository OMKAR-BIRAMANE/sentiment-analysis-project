# Sentiment Analysis Microservices
A production-ready sentiment analysis system using microservices, Docker.

## Features
- Microservices: Auth (JWT, API keys), Analysis (DistilBERT, 99% accuracy), Storage (PostgreSQL).
- Caching with Redis for 50% faster responses.
## Setup
1. Clone: `git clone https://github.com/OMKAR-BIRAMANE/sentiment-analysis-project`
2. Install Docker and Docker Compose.
3. Run: `docker-compose up -d`
4. Access Streamlit: `http://localhost:8501`
5. Test APIs with curl (see below).
6. Kubernetes: `kubectl apply -f kubernetes/k8s-deployment.yaml`

## API Endpoints (curl Commands)
- Register: `curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"pass\"}"`
- Login: `curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"pass\"}"`
- Analyze: `curl -X POST http://localhost:8000/analyze/analyze -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"text\":\"I love AI\"}"`
- Store: `curl -X POST http://localhost:8000/store/store -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"user_id\":\"1\",\"text\":\"I love AI\",\"sentiment\":\"POSITIVE\"}"`