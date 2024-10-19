# Resume Analyzer

## Overview

The Resume Analyzer is a Kubernetes-based application that processes resumes in PDF and DOC/DOCX formats, providing analysis and improvement suggestions using the Gemini AI API.

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
   docker build -t resume-builder-5008 .
   ```

5. Apply Kubernetes configurations:
   ```
   kubectl apply -f resume-builder.yaml
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

## Technologies Used

- Python
- Flask
- Kubernetes
- Docker
- Gemini AI API
- PyPDF2 (for PDF processing)
- python-docx (for DOC/DOCX processing)