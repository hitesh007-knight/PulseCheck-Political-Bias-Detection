# System Diagrams for PulseCheck Project

## Diagram 1: System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                    (Streamlit Frontend)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • URL Input Form                                        │  │
│  │  • Results Visualization                                 │  │
│  │  • Interactive Charts                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                    HTTP/REST API
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    FLASK BACKEND API                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                              │  │
│  │  • POST /analyze                                         │  │
│  │  • GET /health                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                    Pipeline Execution
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    ML ANALYSIS PIPELINE                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Scraper    │  │ Bias Predictor│  │  Sentiment   │        │
│  │  (Trafilatura)│  │  (TF-IDF+SVM)│  │  (TextBlob)  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │Topic Modeler │  │   Entities   │  │ Summarizer   │        │
│  │    (LDA)     │  │   (spaCy)    │  │ (Extractive) │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                    Model Artifacts
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    MODEL STORAGE                                │
│  • vectorizer.pkl                                               │
│  • classifier.pkl                                               │
│  • label_encoder.pkl                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagram 2: Data Flow Diagram

```
┌─────────┐
│  USER   │
│  INPUT  │
└────┬────┘
     │ Article URL
     │
     ▼
┌──────────────────┐
│  Streamlit UI    │
│  (Frontend)      │
└────┬─────────────┘
     │ POST Request
     │ {url, summarize}
     │
     ▼
┌──────────────────┐
│  Flask API       │
│  /analyze        │
└────┬─────────────┘
     │
     │ Fetch Article
     ▼
┌──────────────────┐
│  Web Scraper     │
│  (Trafilatura)   │
└────┬─────────────┘
     │ Extracted Text
     │
     ▼
┌─────────────────────────────────────────┐
│     PARALLEL PROCESSING PIPELINE        │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │   Bias   │  │Sentiment │  │ Topics ││
│  │ Predict  │  │ Analyze  │  │Extract ││
│  └────┬─────┘  └────┬─────┘  └───┬────┘│
│       │            │            │      │
│  ┌────▼─────┐  ┌───▼────┐  ┌────▼────┐│
│  │Entities  │  │Summary │  │   ...   ││
│  │Extract   │  │Generate│  │         ││
│  └──────────┘  └────────┘  └─────────┘│
└────────────────────┬────────────────────┘
                     │
                     │ Aggregated Results
                     ▼
┌──────────────────┐
│  JSON Response   │
│  {bias, sentiment│
│  topics, entities│
│  ...}            │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│  Frontend Display│
│  • Metrics       │
│  • Charts        │
│  • Visualizations│
└──────────────────┘
```

---

## Diagram 3: ML Pipeline Flowchart

```
                    START
                     │
                     ▼
            ┌────────────────┐
            │  Load Dataset  │
            │  (CSV File)    │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  Preprocessing │
            │  • Lowercase   │
            │  • Clean       │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  Label Encoding│
            │  (left/center/ │
            │   right)       │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Train-Test     │
            │ Split (80-20)  │
            └────┬───────┬───┘
                 │       │
        ┌────────┘       └────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│ Training Set │          │   Test Set   │
│   (80%)      │          │    (20%)     │
└──────┬───────┘          └──────────────┘
       │
       ▼
┌──────────────┐
│ TF-IDF       │
│ Vectorization│
│ • 5000 feats │
│ • Bigrams    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Train Linear │
│ SVC Model    │
│ • max_iter=  │
│   2000       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Save Artifacts│
│ • vectorizer │
│ • classifier │
│ • encoder    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Evaluate on  │
│ Test Set     │
│ • Accuracy   │
│ • F1-Score   │
└──────────────┘
       │
       ▼
      END
```

---

## Diagram 4: Component Interaction Diagram

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. Enter URL
       ▼
┌─────────────────────┐
│  streamlit_app.py   │
│  (Frontend)         │
│                     │
│  • UI Components    │
│  • Visualization    │
│  • User Input       │
└──────┬──────────────┘
       │
       │ 2. HTTP POST /analyze
       │    {url, summarize}
       ▼
┌─────────────────────┐
│      app.py         │
│  (Flask Backend)    │
│                     │
│  • Route Handler    │
│  • Request Validation│
│  • Error Handling   │
└──────┬──────────────┘
       │
       │ 3. Call Pipeline
       ▼
┌─────────────────────┐
│   pipeline.py       │
│  (Orchestrator)     │
│                     │
│  • Coordinates all  │
│    modules          │
│  • Aggregates       │
│    results          │
└──────┬──────────────┘
       │
       │ 4. Sequential Calls
       ▼
┌──────────────────────────────────────┐
│        Module Components             │
│                                      │
│  ┌──────────┐  ┌──────────┐        │
│  │ scraper  │  │  bias_   │        │
│  │  .py     │  │ predictor│        │
│  └────┬─────┘  └────┬─────┘        │
│       │            │                │
│  ┌────▼─────┐  ┌───▼─────┐        │
│  │sentiment │  │ entities│        │
│  │  .py     │  │  .py    │        │
│  └──────────┘  └─────────┘        │
│                                      │
│  ┌──────────┐  ┌──────────┐        │
│  │  topic_  │  │ summarizer│       │
│  │ modeler  │  │   .py    │        │
│  └──────────┘  └──────────┘        │
└──────────────────────────────────────┘
       │
       │ 5. Return Results
       ▼
┌─────────────────────┐
│  JSON Response      │
│  {bias, sentiment,  │
│  topics, entities,  │
│  ...}               │
└──────┬──────────────┘
       │
       │ 6. Display Results
       ▼
┌─────────────────────┐
│   Frontend Display  │
│  • Charts           │
│  • Metrics          │
│  • Visualizations   │
└─────────────────────┘
```

---

## Diagram 5: Frontend-Backend Communication Flow

```
┌────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                    │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  1. User enters URL in input field                   │ │
│  │  2. User clicks "Analyze Article" button             │ │
│  │  3. Frontend validates input                         │ │
│  └──────────────────┬───────────────────────────────────┘ │
│                     │                                     │
│                     │ HTTP POST Request                   │
│                     │ {                                    │
│                     │   "url": "https://...",            │
│                     │   "summarize": false               │
│                     │ }                                   │
│                     ▼                                     │
└────────────────────────────────────────────────────────────┘
                         │
                         │ Network (HTTP/REST)
                         │
┌─────────────────────────▼────────────────────────────────────┐
│                  BACKEND (Flask API)                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  4. Receive POST request at /analyze endpoint          │ │
│  │  5. Validate request payload                           │ │
│  │  6. Extract URL and summarize flag                     │ │
│  └──────────────────┬─────────────────────────────────────┘ │
│                     │                                       │
│                     │ Call analyze() function               │
│                     ▼                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  7. Process article through ML pipeline                │ │
│  │     - Scrape article                                   │ │
│  │     - Predict bias                                     │ │
│  │     - Analyze sentiment                                │ │
│  │     - Extract topics                                   │ │
│  │     - Extract entities                                 │ │
│  │     - Generate summary (if requested)                  │ │
│  └──────────────────┬─────────────────────────────────────┘ │
│                     │                                       │
│                     │ Return dictionary with results        │
│                     ▼                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  8. Convert to JSON response                           │ │
│  │  9. Return HTTP 200 with JSON payload                  │ │
│  └──────────────────┬─────────────────────────────────────┘ │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      │ HTTP Response (200 OK)
                      │ {
                      │   "bias": "center",
                      │   "confidence": 0.75,
                      │   "sentiment": "neutral",
                      │   ...
                      │ }
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  FRONTEND (Streamlit)                       │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │  10. Receive JSON response                             ││
│  │  11. Parse response data                               ││
│  │  12. Store in session state                            ││
│  └──────────────────┬─────────────────────────────────────┘│
│                     │                                      │
│                     ▼                                      │
│  ┌────────────────────────────────────────────────────────┐│
│  │  13. Render visualizations                             ││
│  │      - Bias probability chart                          ││
│  │      - Sentiment gauge                                 ││
│  │      - Topics display                                  ││
│  │      - Entities list                                   ││
│  │  14. Display metrics and results                       ││
│  └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 6: Bias Classification Process Flow

```
                    INPUT TEXT
                     │
                     ▼
            ┌────────────────┐
            │ Text           │
            │ Preprocessing  │
            │ • Tokenize     │
            │ • Lowercase    │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Load TF-IDF    │
            │ Vectorizer     │
            │ (Pre-trained)  │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Transform Text │
            │ to TF-IDF      │
            │ Vector         │
            │ (5000 dims)    │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Load SVM       │
            │ Classifier     │
            │ (Pre-trained)  │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Predict Class  │
            │ • Decision     │
            │   Function     │
            │ • Probability  │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Load Label     │
            │ Encoder        │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Decode Label   │
            │ (left/center/  │
            │  right)        │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Calculate      │
            │ Confidence     │
            │ Score (0-1)    │
            └────────┬───────┘
                     │
                     ▼
              OUTPUT RESULT
            {
              "label": "center",
              "confidence": 0.75
            }
```

---

## Diagram 7: Deployment Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    INTERNET / USERS                          │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ HTTPS
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌───────────────┐
│ Streamlit     │         │  Render.com   │
│ Cloud         │         │  (Backend)    │
│               │         │               │
│ Frontend URL: │         │ Backend URL:  │
│ *.streamlit.  │         │ *.onrender.   │
│   app         │◄────────┤   com         │
│               │  HTTP   │               │
│ • UI Rendering│  REST   │ • Flask API   │
│ • Visualizations         │ • ML Pipeline │
│ • User Input  │         │ • Processing  │
└───────────────┘         └───────┬───────┘
                                  │
                                  │ Model Loading
                                  ▼
                        ┌──────────────────┐
                        │  GitHub Repo     │
                        │                  │
                        │  • Source Code   │
                        │  • Model         │
                        │    Artifacts     │
                        │  • Config Files  │
                        └──────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Model Files: │         │ Dependencies:│         │ Config:      │
│ • vectorizer │         │ requirements │         │ • Procfile   │
│ • classifier │         │    .txt      │         │ • runtime.txt│
│ • encoder    │         │              │         │ • render.yaml│
└──────────────┘         └──────────────┘         └──────────────┘
```

---

## Notes for Diagrams

1. **Diagram 1 (System Architecture)**: Shows high-level system components and their relationships
2. **Diagram 2 (Data Flow)**: Illustrates how data flows through the system from input to output
3. **Diagram 3 (ML Pipeline)**: Details the machine learning model training process
4. **Diagram 4 (Component Interaction)**: Shows how different modules interact with each other
5. **Diagram 5 (Communication Flow)**: Details the request-response cycle between frontend and backend
6. **Diagram 6 (Bias Classification)**: Step-by-step process of bias prediction
7. **Diagram 7 (Deployment)**: Cloud deployment architecture showing platform distribution

These diagrams can be recreated using tools like:
- Draw.io / diagrams.net
- Microsoft Visio
- Lucidchart
- PlantUML
- Mermaid (for markdown-based diagrams)

