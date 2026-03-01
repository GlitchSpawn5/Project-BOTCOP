# 🛡️ Project BOTCOP: Autonomous AI-Native Enterprise Defense

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.95+-009688.svg)](https://fastapi.tiangolo.com/)

**Project BOTCOP** is an enterprise-grade cybersecurity platform that moves beyond traditional reactive monitoring toward **Autonomous Threat Governance**. Powered by a self-hosted **Mistral 7B LLM** and **Behavioral Graph Intelligence**, BOTCOP detects, reasons, and neutralizes multi-stage attacks in milliseconds.

---

## 🚀 Core Features

### 1. Behavioral Graph Intelligence (D3.js)
A live, high-fidelity relationship map of every user and asset in your cloud. It detects anomalies in user-to-service flows and highlights lateral movement before it becomes a breach.

### 2. Autonomous Mitigation Engine
Stop threats at machine speed. BOTCOP's Policy Engine allows SOC teams to define confidence thresholds for automated response, including:
- **Instant Container Isolation**
- **Decoy Credential Generation** (Honeypots)
- **Granular Token Revocation**

### 3. Phantom Sanitizer (LLM Defense)
A dedicated defensive layer for Gen-AI applications. It performs real-time semantic analysis to identify and block **Prompt Injection**, **Jailbreaks**, and **Data Exfiltration** attempts.

### 4. Contextual Threat Reasoning (Mistral 7B)
Unlike rule-based systems, BOTCOP uses local LLM inference to generate human-readable explanations of complex attack chains, giving your SOC analysts a "Co-Pilot" for threat hunting.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Tailwind CSS (Glassmorphism), D3.js (Graph Engine), Lucide Icons.
- **Backend API**: FastAPI, Pydantic-Settings, SQLAlchemy, Neo4j.
- **ML Pipeline**: Mistral 7B (Inference), Isolation Forest (Anomaly Detection).
- **Infrastructure**: Docker Compose, Kubernetes (GKE), Terraform (GCP).
- **Data Layer**: PostgreSQL (Events/Incidents), Neo4j (Graph Topology).

---

## 🏁 Getting Started (Local Development)

### Prerequisites
- Python 3.9+
- Node.js (Optional, served via Python for demo)
- Docker (Optional, for full stack)

### 1. Clone & Setup
```bash
git clone https://github.com/your-repo/botcop.git
cd botcop
pip install -r backend/requirements.txt
```

### 2. Configure Environment
Copy the example environment file and update your keys.
```bash
cp .env.example .env
```

### 3. Launch Services (Manual Mode)
Run each component in a separate terminal:

**Terminal 1: ML Inference Server**
```bash
$env:PYTHONPATH="."  # (Windows PowerShell)
python ml_pipeline/inference_server/main.py
```

**Terminal 2: Backend API**
```bash
python backend/main.py
```

**Terminal 3: SOC Dashboard (Frontend)**
```bash
python -m http.server 3000 --directory frontend
```

**Terminal 4: Simulation Engine (The Data Source)**
```bash
python simulator/runner.py
```

---

## 🐳 Docker Deployment (Recommended)
Launch the entire stack including databases and AI models with a single command:
```bash
docker-compose up --build
```

---

## ☁️ Cloud Deployment (GCP + GKE)
BOTCOP is pre-configured for Google Cloud Platform.
1. **Infrastructure**: `terraform init && terraform apply` (See `infrastructure/terraform`)
2. **Kubernetes**: `kubectl apply -f infrastructure/kubernetes/`

---

## � SOC Dashboard Guide
- **Dashboard Tab**: Monitor global system health and live log ingestion.
- **Prompt Lab**: Stress-test the defensive sanitizer against malicious AI prompts.
- **Graph Intelligence**: Explore the live topology of your cloud entities.
- **Policies**: Configure autonomous action thresholds for the AI Analyst.

---

## � License
Project BOTCOP is licensed under the MIT License. See [LICENSE](LICENSE) for details.

> *Built for the 2026 International AI-Security Hackathon.*

