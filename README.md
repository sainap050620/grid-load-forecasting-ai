# ⚡ German Power Grid Load Forecasting API

An end-to-end containerized microservice that forecasts electricity grid demand (MW) to assist German Transmission System Operators (TSOs) with reserve balancing.

## 🛠️ Architecture & Tech Stack
* **Language & Frameworks:** Python 3.11, FastAPI, Scikit-Learn, Pandas
* **Data Validation:** Pydantic v2 (enforces strict schema boundaries at API entry)
* **Testing:** Pytest & FastAPI TestClient
* **Deployment:** Docker containerization

## 🚀 Quickstart

### 1. Local Run
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run automated tests
pytest tests/

# Launch API server
uvicorn src.app:app --reload