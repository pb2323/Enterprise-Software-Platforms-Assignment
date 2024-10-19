# Resume Analyzer

## Overview

The Resume Analyzer is a Kubernetes-based application that processes resumes in PDF and DOC/DOCX formats, providing analysis and improvement suggestions using the Gemini AI API. This project demonstrates the transition from a monolithic architecture to a microservices architecture, showcasing scalability and maintainability improvements.

## Architecture

### Monolithic Architecture

Initially, the application was deployed as a single unit in a Kubernetes cluster:

```
+----------------------------------+
|           Kubernetes             |
|  +----------------------------+  |
|  |    Resume Analyzer Pod     |  |
|  |  +----------------------+  |  |
|  |  |   Flask Application  |  |  |
|  |  |   - PDF Processing   |  |  |
|  |  |   - DOC Processing   |  |  |
|  |  |   - Text Analysis    |  |  |
|  |  +----------------------+  |  |
|  |           |  ^             |  |
|  +-----------|--|-------------+  |
|              |  |                |
+--------------|--|----------------+
               |  |
               v  |
        +----------------+
        |     User       |
        +----------------+
```

### Microservices Architecture

The application was then refactored into a microservices architecture:

```
+-------------------------------------------------------+
|                      Kubernetes                       |
|  +-----------------+    +-----------------------+     |
|  | Frontend Service|<-->|        Ingress        |     |
|  +-----------------+    +-----------------------+     |
|    |             ^                   ^                |
|    v             |                   |                |
|  +-----------------+    +-----------------+           |
|  |   PDF Service   |    |   DOC Service   |           |
|  +-----------------+    +-----------------+           |
|    |                      |                           |
+----|-----------------------|---------------------------+
     |                       |
     v                       v
+---------------------------------------------+
|               Gemini AI API                 |
+---------------------------------------------+
                     ^
                     |
            +----------------+
            |      User      |
            +----------------+
```

## Setup and Deployment

### Prerequisites

- Minikube
- kubectl
- Docker

### Deployment Steps

1. Start Minikube:
   ```
   minikube start --vm-driver=docker
   ```

2. Set up Minikube's Docker environment:
   ```
   eval $(minikube docker-env)
   ```

3. Build Docker images for each service:
   ```
   docker build -t frontend-service ./frontend-service
   docker build -t pdf-service ./pdf-service
   docker build -t doc-service ./doc-service
   ```

4. Create a secret for the Gemini API key:
   ```
   kubectl create secret generic gemini-api-secret --from-literal=api-key=your_api_key_here
   ```

5. Apply Kubernetes configurations:
   ```
   kubectl apply -f kubernetes/
   ```

6. Verify the deployments:
   ```
   kubectl get pods
   kubectl get services
   kubectl get ingress
   ```

7. Access the application:
   ```
   minikube service frontend-service
   ```

## Project Structure

```
resume-analyzer/
├── frontend-service/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
├── pdf-service/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── doc-service/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
|
│─── resume-analyzer-secret.yaml
|─── resume-analyzer.yaml
│
└── README.md
```

## Technologies Used

- Python
- Flask
- Kubernetes
- Docker
- Gemini AI API
- PyPDF2 (for PDF processing)
- python-docx (for DOC/DOCX processing)