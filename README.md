# ShopWave – Cloud Native E-Commerce Platform

## Project Overview

ShopWave is a cloud-native microservices-based e-commerce platform designed and deployed using modern DevOps and cloud technologies. The project demonstrates scalable architecture, containerized deployment, Kubernetes orchestration, Infrastructure as Code (IaC), and CI/CD automation.

The platform provides features such as user authentication, product management, order processing, payment handling, notifications, and responsive frontend interfaces.

This project was built to gain hands-on experience with:

* Microservices Architecture
* Docker Containerization
* Kubernetes Orchestration
* AWS Cloud Deployment
* Terraform Infrastructure Provisioning
* Jenkins CI/CD Automation
* MongoDB Atlas Integration
* API Gateway Routing
* React Frontend Development
* Flask Backend Services

---

# Architecture

```text
User
 ↓
React Frontend
 ↓
AWS Load Balancer
 ↓
API Gateway
 ↓
Microservices
 ├── Auth Service
 ├── Product Service
 ├── Order Service
 ├── Payment Service
 └── Notification Service
 ↓
MongoDB Atlas
```

---

# Features

## Frontend Features

* Modern React-based UI
* Product listing page
* Product filtering and sorting
* Search functionality
* Shopping cart UI
* Responsive design
* Order management page

## Backend Features

* RESTful APIs
* JWT Authentication
* User Registration & Login
* Product Management APIs
* Order APIs
* Payment APIs
* Notification Service
* API Gateway Routing

## DevOps Features

* Dockerized microservices
* Kubernetes deployments
* AWS EKS deployment
* Terraform infrastructure setup
* Jenkins CI/CD pipeline
* MongoDB Atlas cloud database
* AWS Load Balancer integration

---

# Tech Stack

## Frontend

* React
* Material UI
* Axios
* React Router
* Zustand
* React Query

## Backend

* Python
* Flask
* JWT Authentication
* REST APIs

## Database

* MongoDB Atlas

## DevOps & Cloud

* Docker
* Kubernetes
* AWS EKS
* Terraform
* Jenkins
* NGINX
* AWS EC2
* AWS Load Balancer

---

# Project Structure

```bash
shopwave/
│
├── frontend/
├── auth/
├── product/
├── order/
├── payment/
├── notification/
├── api-gateway/
├── terraform/
├── k8s/
├── Jenkinsfile
└── README.md
```

---

# Microservices

## 1. Auth Service

Handles:

* User registration
* User login
* JWT token generation
* Authentication validation

### API Endpoints

```http
POST /api/users/register
POST /api/users/login
```

---

## 2. Product Service

Handles:

* Product listing
* Product filtering
* Product details
* Product categories

### API Endpoints

```http
GET /api/products
GET /api/products/:id
```

---

## 3. Order Service

Handles:

* Order creation
* Order management
* Order tracking

---

## 4. Payment Service

Handles:

* Payment processing
* Payment validation

---

## 5. Notification Service

Handles:

* User notifications
* Order confirmation alerts

---

# Frontend Workflow

```text
User Opens Frontend
        ↓
React Application Loads
        ↓
Frontend Sends API Requests
        ↓
API Gateway Routes Request
        ↓
Microservice Processes Request
        ↓
MongoDB Stores/Retrieves Data
        ↓
Response Sent Back to Frontend
```

---

# Docker Workflow

Each microservice contains a Dockerfile.

## Build Docker Image

```bash
docker build -t auth-service .
```

## Run Container

```bash
docker run -p 5000:5000 auth-service
```

---

# Kubernetes Deployment

Kubernetes is used to orchestrate all services.

## Features

* Pod management
* Auto-restart
* Service discovery
* Scaling
* Load balancing

## Deploy Application

```bash
kubectl apply -f k8s/
```

## Check Pods

```bash
kubectl get pods -n shopwave
```

---

# Terraform Infrastructure

Terraform provisions AWS infrastructure automatically.

## Infrastructure Includes

* VPC
* Public & Private Subnets
* EKS Cluster
* Worker Nodes
* Security Groups
* IAM Roles

## Terraform Commands

### Initialize Terraform

```bash
terraform init
```

### Plan Infrastructure

```bash
terraform plan
```

### Apply Infrastructure

```bash
terraform apply
```

---

# Jenkins CI/CD Pipeline

Jenkins automates:

* Source code pull from GitHub
* Docker image build
* Docker image push
* Kubernetes deployment
* Automated updates

## Pipeline Flow

```text
GitHub Push
     ↓
Jenkins Trigger
     ↓
Build Docker Images
     ↓
Push Images
     ↓
Deploy to Kubernetes
```

---

# MongoDB Atlas Integration

MongoDB Atlas is used as the cloud database.

## Collections

* users
* products
* orders
* tokens

---

# API Testing

## Register User

```bash
curl -Method POST "http://<LOAD_BALANCER>/api/users/register" \
-ContentType "application/json" \
-Body '{"name":"Varun","email":"varun@shopwave.co","password":"varun123"}'
```

---

## Login User

```bash
curl -Method POST "http://<LOAD_BALANCER>/api/users/login" \
-ContentType "application/json" \
-Body '{"email":"varun@shopwave.co","password":"varun123"}'
```

---

## Get Products

```bash
curl "http://<LOAD_BALANCER>/api/products?limit=30"
```

---

# Deployment Screenshots

The project includes:

* Kubernetes pod deployment
* Jenkins pipeline setup
* MongoDB Atlas collections
* API testing screenshots
* React frontend deployment

---

# Security Features

* JWT-based authentication
* Secure API access
* Kubernetes namespace isolation
* Cloud-managed database

---

# Future Enhancements

* Helm Charts
* Prometheus Monitoring
* Grafana Dashboards
* ArgoCD GitOps
* HTTPS with TLS
* Redis Caching
* RabbitMQ / Kafka
* Horizontal Pod Autoscaling
* GitHub Actions
* Payment Gateway Integration

---

# Learning Outcomes

This project helped in understanding:

* Real-world microservices architecture
* Kubernetes orchestration
* Cloud-native deployments
* Infrastructure as Code
* CI/CD automation
* Containerized application deployment
* API Gateway routing
* Production-style deployment workflows

---

# How to Run the Project

## Clone Repository

```bash
git clone https://github.com/varunjavali/shopwave.git
cd shopwave
```

---

## Run Frontend

```bash
cd frontend
npm install
npm start
```

---

## Run Backend Service

```bash
cd auth
pip install -r requirements.txt
python app.py
```

---

## Deploy Using Kubernetes

```bash
kubectl apply -f k8s/
```

---

# Author

## Varun Kumar J A

MCA Student | DevOps & Cloud Enthusiast

Skills:

* AWS
* Docker
* Kubernetes
* Terraform
* Jenkins
* Python
* React
* Flask
* MongoDB

GitHub:
[https://github.com/varunjavali](https://github.com/varunjavali)

---

# Conclusion

ShopWave demonstrates a modern cloud-native e-commerce platform built using industry-standard DevOps and cloud technologies. The project showcases practical implementation of microservices, container orchestration, CI/CD automation, and scalable cloud infrastructure deployment using AWS and Kubernetes.
# Screenshots

## User Registration API

![User Registration](screenshots/Screenshot%20(254).png)

---

## User Login API

![User Login](screenshots/Screenshot%20(255).png)

---

## Product API Response

![Products API](screenshots/Screenshot%20(256).png)

---

## ShopWave Home Page

![Home Page](screenshots/Screenshot%20(257).png)

---

## Products Page

![Products Page](screenshots/Screenshot%20(258).png)

---

## MongoDB Atlas Database

![MongoDB Atlas](screenshots/Screenshot%20(259).png)

---

## Kubernetes Pods Running

![Kubernetes Pods](screenshots/Screenshot%20(260).png)

---

## Jenkins Credentials Setup

![Jenkins Credentials](screenshots/Screenshot%20(265).png)

---

## Jenkins Pipeline Configuration

![Jenkins Pipeline](screenshots/Screenshot%20(262)(1).png)
