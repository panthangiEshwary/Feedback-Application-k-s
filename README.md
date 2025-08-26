<img width="1366" height="515" alt="image" src="https://github.com/user-attachments/assets/c4e66549-d936-47fb-a39d-dc8430c4592d" />Project Name: Feedback Application (Three-Tier Kubernetes Deployment)

Objective: Collect, manage, and display user feedback in real-time using a containerized, scalable architecture.

Key Features:

Submit feedback through a web interface
Real-time updates via WebSocket (Socket.IO)
Persistent storage in MySQL
Deployment and orchestration using Kubernetes

Project Architecture

Three-Tier Architecture:

Frontend:
Files: frontend/app.js, index.html, styles.css
Handles user interaction and sends feedback to backend APIs
Dockerized with frontend/Dockerfile

Backend:

Files: backend/app.py, gunicorn.conf.py, requirements.txt
Flask + Socket.IO API server
Handles feedback storage and real-time updates
Dockerized with backend/Dockerfile

Database:

MySQL StatefulSet in Kubernetes (k8s/03-mysql-statefulset.yaml)
Initialization via k8s/07-initdb-configmap.yaml

Kubernetes Layer:

Namespace: k8s/00-namespace.yaml
Secrets: k8s/01-secrets.yaml
ConfigMaps: k8s/02-configmap.yaml
Backend Deployment: k8s/04-backend-deploy.yaml
Frontend Deployment: k8s/frontend-deployment.yaml
Ingress for external access: k8s/06-ingress.yaml


Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Python Flask + Socket.IO
Database: MySQL
Containerization: Docker
Orchestration: Kubernetes (Deployments, Services, ConfigMaps, StatefulSets, Ingress)

System Workflow

User submits feedback via frontend UI.
Frontend sends the feedback data to backend via REST API.
Backend processes data and stores it in MySQL.
Backend pushes real-time updates to all connected clients via WebSocket.
Frontend updates feedback list dynamically.
<img width="1366" height="468" alt="image" src="https://github.com/user-attachments/assets/e4ef9a63-bedd-49dd-955f-f34d606726fe" />
<img width="1366" height="334" alt="image" src="https://github.com/user-attachments/assets/1bdfc081-b207-4f77-aa54-169ee5f74eae" />



Deployment Steps:

Build Docker Images:
# Backend
docker build -t feedback-backend ./backend

# Frontend
docker build -t feedback-frontend ./frontend

Deploy to Kubernetes:
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-secrets.yaml
kubectl apply -f k8s/02-configmap.yaml
kubectl apply -f k8s/03-mysql-statefulset.yaml
kubectl apply -f k8s/07-initdb-configmap.yaml
kubectl apply -f k8s/04-backend-deploy.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/06-ingress.yaml

Verify Deployments:
kubectl get pods -n feedback
kubectl get svc -n feedback
kubectl get ingress -n feedback

Current Status

Feedback submission is functional
Real-time updates via WebSocket are working
Kubernetes deployment tested on Minikube

