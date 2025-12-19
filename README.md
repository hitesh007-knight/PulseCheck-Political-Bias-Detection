# PulseCheck

Political bias detection system for news articles with Flask backend and Streamlit frontend. Analyzes articles for bias (left/center/right), sentiment, topics, and entities.

## Setup
```bash
pip install -r requirements.txt

# Download spaCy English model (for entity extraction)
python -m spacy download en_core_web_sm
```

## Train Model
```bash
python train.py
```
Trains on `improved_political_dataset.csv` and saves artifacts to `artifacts/` folder.

## Usage Options

### 1. CLI (Simple)
```bash
python run.py --url "https://example.com/article"
```

### 2. Flask Backend + Streamlit Frontend (Full Dashboard)
```bash
# Terminal 1: Start Flask backend
python app.py

# Terminal 2: Start Streamlit frontend
streamlit run streamlit_app.py
```
Then open http://localhost:8501 in your browser.

### 3. Programmatic Use
```python
from pulsecheck import analyze

result = analyze("https://example.com/article")
print(result["bias"], result["confidence"])
print(result["sentiment"])
print(result["topics"])
print(result["entities"])
```

## Features
- **Bias Detection**: TF-IDF + SVM classifier (left/center/right)
- **Sentiment Analysis**: TextBlob for polarity and subjectivity
- **Topic Modeling**: LDA for topic extraction
- **Entity Extraction**: spaCy for people, organizations, places
- **Visualizations**: Interactive charts in Streamlit dashboard
