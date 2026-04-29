# 🔍 PulseCheck — Political Bias Detection

A multilingual political bias detection system that analyzes news articles for bias, sentiment, topics, and named entities. Built with Python, Flask, Streamlit, and NLP/ML models.

> **B.Tech Final Year Project**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Political Bias Detection** | SVM + Transformer (RoBERTa/BERT) classifiers — Left / Center / Right |
| **Multilingual Support** | Auto-detects 40+ languages, translates to English for analysis |
| **Sentiment Analysis** | Polarity and subjectivity scoring via TextBlob |
| **Topic Extraction** | LDA-based topic modeling with keyword extraction |
| **Named Entity Recognition** | Multilingual NER (people, organizations, places) using BERT |
| **Article Summarization** | Extractive summarization of article content |
| **Web Scraping** | Extracts article text from any URL via Trafilatura |
| **Direct Text Input** | Paste article text in any language for instant analysis |

---

## 📁 Project Structure

```
PulseCheck/
├── app.py                      # Flask backend API server
├── streamlit_app.py            # Streamlit frontend dashboard
├── run.py                      # CLI interface
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku deployment
├── render.yaml                 # Render deployment config
├── runtime.txt                 # Python version spec
│
├── pulsecheck/                 # Core analysis package
│   ├── __init__.py
│   ├── config.py               # Paths & configuration
│   ├── artifacts.py            # Model loader
│   ├── pipeline.py             # Main analysis pipeline
│   ├── language.py             # Language detection & translation
│   ├── scraper.py              # Web article scraper
│   ├── bias_predictor.py       # SVM bias classifier
│   ├── transformer_bias_predictor.py  # Transformer bias classifier
│   ├── sentiment.py            # Sentiment analysis
│   ├── topic_modeler.py        # Topic extraction (LDA)
│   ├── entities.py             # Named entity recognition
│   └── summarizer.py           # Text summarization
│
├── models/                     # Trained model artifacts
│   ├── vectorizer.pkl          # TF-IDF vectorizer
│   ├── classifier.pkl          # SVM classifier
│   ├── label_encoder.pkl       # Label encoder
│   └── transformer/            # BERT/RoBERTa model files
│
├── data/                       # Training dataset
│   └── improved_political_dataset.csv
│
├── scripts/                    # Training & utility scripts
│   ├── train.py                # Train SVM model
│   ├── train_transformer.py    # Train transformer model
│   ├── setup_bert_model.py     # Download pre-trained BERT
│   ├── START_APP.bat           # Windows: start Flask
│   └── START_STREAMLIT.bat     # Windows: start Streamlit
│
├── tests/                      # Test suite
│   ├── test_setup.py           # Dependency checker
│   └── test_transformer_smoke.py  # Transformer smoke test
│
└── docs/                       # Documentation
    ├── PROJECT_REPORT.md       # Full project report
    ├── DIAGRAMS.md             # Architecture diagrams
    ├── DEPLOYMENT.md           # Deployment guide
    ├── DEPLOYMENT_CHECKLIST.md # Deployment checklist
    └── DEMO_GUIDE_FOR_SUPERVISOR.md  # Demo walkthrough
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the SVM model (one-time)

```bash
python scripts/train.py
```

### 3. Run the application

**Terminal 1 — Backend:**
```bash
python app.py
```

**Terminal 2 — Frontend:**
```bash
streamlit run streamlit_app.py
```

**Or on Windows — double-click:**
- `scripts/START_APP.bat`
- `scripts/START_STREAMLIT.bat`

### 4. Open in browser

Navigate to **http://localhost:8501** and enter a news article URL or paste text in any language.

---

## 🌐 Multilingual Support

PulseCheck supports **40+ languages** including:

Hindi, Spanish, French, German, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Italian, Dutch, Turkish, Polish, Ukrainian, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Persian, Hebrew, and more.

**How it works:**
1. Article text is scraped (or pasted directly)
2. Language is auto-detected using `langdetect`
3. Non-English text is translated to English via Google Translate
4. Bias, sentiment, and topics are analyzed on the English text
5. Named entities are extracted from the *original* text using a multilingual BERT NER model

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze` | Analyze article (accepts `url` or `text`, optional `language_override`) |
| `GET`  | `/languages` | List all supported languages |
| `GET`  | `/health` | Health check |

### Example — Analyze by URL

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/example", "summarize": true}'
```

### Example — Analyze Hindi text directly

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "भारत सरकार ने आज एक नई नीति की घोषणा की...", "language_override": "hi"}'
```

---

## 🧠 Model Training

### SVM (default)
```bash
python scripts/train.py
```

### Transformer (RoBERTa/BERT)
```bash
# Quick prototype
python scripts/train_transformer.py --train_samples 12000 --eval_samples 3000 --epochs 1

# Full training
python scripts/train_transformer.py --epochs 3
```

---

## 📦 Tech Stack

- **Backend:** Flask, Gunicorn
- **Frontend:** Streamlit, Plotly
- **ML/NLP:** scikit-learn, HuggingFace Transformers, TextBlob
- **Language:** langdetect, deep-translator
- **Scraping:** Trafilatura
- **NER:** Multilingual BERT (`Davlan/bert-base-multilingual-cased-ner-hrl`)

---

## 📄 License

This project was developed as a B.Tech final year project.
