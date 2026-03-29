# NeuralBrief -> Text Insight MLOps Pipeline

> Fine-tuned PEGASUS on SAMSum · Mistral AI integration · End-to-end MLOps from raw data to live inference

---

## What It Does

Takes a dialogue or story, runs it through a PEGASUS transformer fine-tuned on 14.7K real conversations, and returns a concise abstractive summary. Mistral AI generates test inputs on-demand and evaluates summary quality in real-time — no manual test data needed.

---

**ROUGE-1: 0.44 · ROUGE-2: 0.23 · Dataset: SAMSum (14.7K samples)**

---

## My Workflow

Every stage follows the same pattern — config first, then code:

1. Update `config.yaml`
2. Update `params.yaml`
3. Define config entity
4. Update Configuration Manager
5. Build the component — Data Ingestion → Data Validation → Data Transformation → Model Trainer → Model Evaluation
6. Wire up the pipeline — Training Pipeline, Prediction Pipeline
7. Ship the frontend — Prediction API, Training API, Batch Prediction API

---

## Stack

| Layer | Tech |
|---|---|
| Model | `google/pegasus-cnn_dailymail` fine-tuned on SAMSum |
| Framework | HuggingFace Transformers + PyTorch |
| Evaluation | ROUGE via `evaluate` library |
| Backend | FastAPI + Uvicorn |
| AI Integration | Mistral AI (`mistral-small-latest`) |
| Infra | Docker · GitHub Actions CI/CD |

---

## Quickstart

```bash
git clone https://github.com/ZeroCipherX/text-insight-mlops-pipeline
cd text-insight-mlops-pipeline

python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# Add your Mistral API key
echo MISTRAL_API_KEY=your_key_here > .env

# Train (skips automatically if model already exists)
python main.py

# Serve
python app.py
# → http://localhost:8080
```

---

## Project Structure

```
├── src/TextInsightMlopsPipeline/
│   ├── components/      # Data ingestion, transformation, training, evaluation
│   ├── pipeline/        # Stage pipelines + prediction
│   ├── config/          # Configuration manager
│   └── entity/          # Config dataclasses
├── config/config.yaml   # All paths and model config
├── params.yaml          # Training hyperparameters
├── research/            # Jupyter notebooks (one per stage)
├── templates/index.html # Web UI
└── app.py               # FastAPI server
```
