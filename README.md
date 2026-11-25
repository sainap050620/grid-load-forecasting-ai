# ⚡ German Power Grid Load Forecasting API
![CI Pipeline](https://github.com/sainap050620/grid-load-forecasting-ai/actions/workflows/ci.yml/badge.svg)

**Live demo:** [https://grid-load-forecasting-ai.onrender.com/docs](https://grid-load-forecasting-ai.onrender.com/docs) (interactive API docs). It runs on a free instance, so the first request after idle can take up to a minute.


A containerised microservice that forecasts electricity grid demand (MW) from temperature and calendar features, the kind of short-term load estimate transmission system operators use for reserve balancing.

> The model is trained on **synthetic** data that mimics German load patterns (daily cycle, weekend dip, temperature and holiday effects). The focus of this project is the **production setup** around the model: validation, testing, CI and containerisation.

## 🏗️ Architecture

```
POST /predict ──► Pydantic schema validation ──► RandomForest model ──► predicted_load_mw
GET  /health  ──► service + model status
```

| Component | File | Role |
|---|---|---|
| Model training | `src/model.py` | Generates training data, fits a `RandomForestRegressor`, saves `model.joblib` |
| API | `src/app.py` | FastAPI app; loads (or trains) the model at startup |
| Input contract | `src/schemas.py` | Pydantic v2 models with strict value ranges |
| Tests | `tests/test_api.py` | Health check, successful prediction, rejection of invalid input |
| CI | `.github/workflows/ci.yml` | Trains the model and runs the tests on every push and PR |

## 🔒 Input Validation

Requests outside realistic ranges are rejected with HTTP `422` before they reach the model:

| Field | Type | Allowed range |
|---|---|---|
| `temperature_celsius` | float | −30 to 50 |
| `hour_of_day` | int | 0 to 23 |
| `day_of_week` | int | 0 (Mon) to 6 (Sun) |
| `is_holiday` | int | 0 or 1 |

## 🚀 Quickstart

### Local

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python -m src.model               # train and save the model
python -m pytest tests/           # run the test suite
uvicorn src.app:app --reload      # start the API on http://localhost:8000
```

### Docker

```bash
docker build -t grid-load-api .
docker run -p 8000:8000 grid-load-api
```

The model is trained during the image build, so the container starts ready to serve.

## 📡 Example Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature_celsius": 14.0, "hour_of_day": 12, "day_of_week": 2, "is_holiday": 0}'
```

```json
{"predicted_load_mw": 40094.9, "model_version": "random-forest-v1"}
```

Interactive API docs are available at `http://localhost:8000/docs`, or on the live service at https://grid-load-forecasting-ai.onrender.com/docs.

## 🛠️ Tech Stack

Python 3.11 · FastAPI · Pydantic v2 · scikit-learn · Pytest · Docker · GitHub Actions
