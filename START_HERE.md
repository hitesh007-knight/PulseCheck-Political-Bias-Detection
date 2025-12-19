# Quick Start Guide - Step by Step

## Step 1: Check Setup
Run this to see what's installed:
```bash
python test_setup.py
```

## Step 2: Train the Model (ONE TIME ONLY)
```bash
python train.py
```
Wait for it to finish (takes 2-5 minutes). You'll see "Artifacts saved" when done.
**You only need to do this once!**

## Step 3: Start the Backend (Terminal 1)
Open a terminal/command prompt in this folder:
```bash
python app.py
```
**LOOK FOR THIS MESSAGE:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```
**KEEP THIS TERMINAL OPEN!** Don't close it.

## Step 4: Start the Frontend (Terminal 2 - NEW WINDOW)
Open a **NEW** terminal window in the same folder:
```bash
streamlit run streamlit_app.py
```
**LOOK FOR THIS MESSAGE:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```
**Your browser should open automatically!**

## Step 5: Test It!
1. Browser opens to http://localhost:8501
2. Paste a news article URL (try: https://www.bbc.com/news)
3. Click "Analyze Article"
4. See the results!

## How to Check if It's Running:

### Backend (Flask) - Terminal 1:
- Should show: "Running on http://127.0.0.1:5000"
- No red error messages
- Test: Open browser to http://localhost:5000/health
  - Should see: {"status":"ok"}

### Frontend (Streamlit) - Terminal 2:
- Should show: "You can now view your Streamlit app"
- Browser opens automatically
- You see the PulseCheck dashboard with input box

## To Stop:
- Press `Ctrl+C` in each terminal window
- Or just close the terminal windows

