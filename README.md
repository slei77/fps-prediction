# FPS Prediction System

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Live Demo](#live-demo)
4. [Demo Screenshots](#demo-screenshots)
5. [Features](#features)
6. [Model Details](#model-details)
    - More details: [RESULTS.md](RESULTS.md)
    - Notebooks (Colab and Databricks): [Notebooks](RESULTS.md#notebooks)
7. [Repository Structure](#repository-structure)
8. [Running Locally](#running-locally)
9. [API Usage](#api-usage)
10. [Deployment](#deployment)
11. [Limitations](#limitations)

## Project Overview

This project is an end-to-end machine learning system that predicts average FPS for a game based on GPU specifications, game metadata, and graphics settings.

It is deployed as:

- a FastAPI inference service (backend)
- a Streamlit web app (frontend)
- a trained XGBoost model
- containerized using Docker

## Tech Stack

**Backend**
- FastAPI
- XGBoost
- Scikit-learn

**Frontend**
- Streamlit

**Infrastructure**
- Docker
- REST APIs

## Architecture

```
Streamlit UI
    ↓
FastAPI (validation + preprocessing)
    ↓
Preprocessor (joblib)
    ↓
XGBoost ensemble (5-fold models)
    ↓
FPS prediction
```

## Live Demo

[Frontend](https://fps-prediction-r7f4c9dkchhcarhhr9qxc5.streamlit.app/)

[API](https://fps-prediction.onrender.com/)

## Demo Screenshots

### Streamlit Frontend

#### Default:

<img width="2560" height="1254" alt="image" src="https://github.com/user-attachments/assets/2b01a287-bbbb-4c14-8575-ae21a52c206d" />

#### Custom GPU:

<img width="2560" height="766" alt="image" src="https://github.com/user-attachments/assets/ed27a850-4b51-4b4b-afdd-ee55c94bb746" />

#### Custom Game and Resolution:

<img width="2560" height="918" alt="image" src="https://github.com/user-attachments/assets/d13e895d-9709-47ff-b7e2-bc785610681a" />

#### Prediction Example:

<img width="2558" height="1098" alt="image" src="https://github.com/user-attachments/assets/784316c8-4fd2-4ed7-be90-6a8dd426f338" />

### Render API

#### Swagger UI:

<img width="2560" height="770" alt="image" src="https://github.com/user-attachments/assets/07d83ff0-6445-4be5-a6ea-2c87b9a163ac" />

## Features

- Predict FPS for custom GPU + game configurations
- Supports resolution and graphics preset adjustments
- Fast inference via optimized XGBoost model
- Containerized deployment

## Model Details

Model: Final model is an XGBoost regressor trained using 5-fold cross-validation. Predictions are averaged across folds to form the final ensemble output. 

Input: GPU specs, game metadata, rendering settings

Output: Average FPS

## Repository Structure

```
fps-prediction
├── api/
│   ├── Dockerfile
│   ├── app/
│   │   └── main.py
│   ├── model/
│   │   ├── models.joblib
│   │   └── preprocessor.joblib
│   └── requirements.txt
├── web-app/
│   ├── Dockerfile
│   ├── app/
│   │   ├── constants.py
│   │   ├── game_metadata.json
│   │   ├── gpu_specs.json
│   │   └── main.py
│   └── requirements.txt
├── fps-prediction.code-workspace
├── README.md
└── RESULTS.md
```

## Running Locally

### Clone Repo

```Bash
git clone https://github.com/slei77/fps-prediction.git
cd fps-prediction
```

### Backend

```Bash
cd api
docker build --build-arg PORT=8000 -t fps-api .
docker run -p 8000:8000 fps-api
```

### Frontend

```Bash
cd web-app
docker build -t fps-ui .
docker run -p 8501:8501 fps-ui
```

## API Usage

### Endpoint: 

POST /predict

### Request Example

API expects mixed-case keys to align with dataset schema from Kaggle source. 

```JSON
{
  "Preset": "medium",
  "boostClock": 1777,
  "shaders": 3584,
  "tmus": 112,
  "rops": 48,
  "architecture": "Ampere",
  "memorySize": 12,
  "memoryBandwidth": 360,
  "Resolution": 2073600,
  "Release_Date": 2020,
  "Adventure": false,
  "Brawler": false,
  "Indie": false,
  "Puzzle": false,
  "RPG": false,
  "Racing": false,
  "Real Time Strategy": false,
  "Shooter": true,
  "Simulator": false,
  "Sport": false,
  "Strategy": false,
  "Tactical": true,
  "Turn Based Strategy": false
}
```

### Response Example

```JSON
{
  "prediction": 435.73
}
```

## Deployment

Backend: Render (Docker deployment)
Frontend: Streamlit Cloud / Render
Communication: REST API over HTTP

## Limitations
- Performance drops on unseen GPU architectures
- Limited dataset coverage for niche genres
- Generalization constrained by dataset imbalance
