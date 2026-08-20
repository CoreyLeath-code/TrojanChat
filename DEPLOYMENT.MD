# 🚀 TrojanChat Deployment Guide

This document covers local development, Docker, Render cloud deployment, and optional GPU acceleration.

---

## 🧱 Deployment Overview

TrojanChat is designed to be:
- Containerized with Docker
- Cloud-deployable on Render
- GPU-accelerated via NVIDIA CUDA (optional)
- Scalable with a stateless API design

---

## 🖥️ Local Development

### Requirements

- Python 3.12+
- Node.js 18+
- Docker (for Qdrant + Redis)

### Steps

```bash
git clone https://github.com/CoreyLeath-code/TrojanChat.git
cd TrojanChat
cp .env.example .env
# Edit .env with your API keys

# Start Qdrant + Redis
docker-compose up -d

# Backend
cd backend
pip install -r requirements.txt
uvicorn api:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 🐳 Docker Deployment

### Build image

```bash
docker build -t trojanchat .
```

### Run container

```bash
docker run -p 8000:8000 --env-file .env trojanchat
```

---

## ☁️ Render Deployment (Production)

### 1. Create a Render Web Service

- **Runtime**: Docker
- **Branch**: `main`
- **Region**: Oregon (recommended)
- **Instance Type**: Starter or Standard

### 2. Set Environment Variables

In the Render dashboard, add:

```
PORT=8000
GROQ_API_KEY=...
COHERE_API_KEY=...
QDRANT_HOST=...
QDRANT_PORT=6333
REDIS_URL=...
```

---

## ⚡ NVIDIA CUDA (GPU Acceleration)

TrojanChat supports GPU acceleration for local AI inference workloads.

### Requirements

- NVIDIA GPU (RTX 30xx+ recommended)
- NVIDIA Container Toolkit

### Build GPU image

```bash
docker build -f DockerFile.cuda -t trojanchat-gpu .
```

### Run with GPU

```bash
docker run --gpus all -p 8000:8000 --env-file .env trojanchat-gpu
```

---

## 📊 Monitoring & Logs

```bash
# Docker logs
docker logs <container_id>

# Prometheus metrics (when running)
curl http://localhost:8000/metrics
```
