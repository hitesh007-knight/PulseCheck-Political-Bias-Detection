# 🚀 Deployment Guide for PulseCheck

This guide will help you deploy your PulseCheck application (Flask backend + Streamlit frontend) to make it publicly accessible.

## 📋 Table of Contents
1. [Overview](#overview)
2. [Recommended Deployment Strategy](#recommended-deployment-strategy)
3. [Option 1: Render.com (Recommended)](#option-1-rendercom-recommended)
4. [Option 2: Streamlit Cloud + Render.com](#option-2-streamlit-cloud--rendercom)
5. [Option 3: Railway.app](#option-3-railwayapp)
6. [Post-Deployment Steps](#post-deployment-steps)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Your application consists of:
- **Backend**: Flask API (`app.py`) - handles article analysis
- **Frontend**: Streamlit dashboard (`streamlit_app.py`) - user interface

**Important Note**: Netlify is designed for static sites and serverless functions. For Python applications like yours, you'll need platforms that support Python runtime environments.

---

## Recommended Deployment Strategy

**Best Option**: Deploy backend to Render.com and frontend to Streamlit Cloud (free and easy)

**Alternative**: Deploy both to Render.com using the provided `render.yaml` configuration

---

## Option 1: Render.com (Recommended)

Render.com offers free hosting for both Flask and Streamlit applications.

### Prerequisites
1. Create a free account at [render.com](https://render.com)
2. Connect your GitHub account (or use GitLab/Bitbucket)
3. Push your code to a Git repository

### Step 1: Prepare Your Repository

1. **Ensure all files are committed**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Verify these files exist**:
   - `requirements.txt` ✅
   - `Procfile` ✅
   - `runtime.txt` ✅
   - `render.yaml` ✅ (optional, for automated setup)

### Step 2: Deploy Backend (Flask API)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure the service:
   - **Name**: `pulsecheck-backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```
   - **Instance Type**: Free (or paid for better performance)
5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. **Copy the service URL** (e.g., `https://pulsecheck-backend.onrender.com`)

### Step 3: Deploy Frontend (Streamlit)

**Option A: Deploy to Streamlit Cloud (Easiest)**

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository
5. Configure:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: `3.11`
   - **Advanced settings** → **Secrets**:
     ```
     BACKEND_URL=https://your-backend-url.onrender.com
     ```
6. Click **"Deploy"**
7. Your app will be live at `https://your-app-name.streamlit.app`

**Option B: Deploy to Render.com**

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect the same repository
3. Configure:
   - **Name**: `pulsecheck-frontend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment Variables**:
     - `BACKEND_URL`: `https://your-backend-url.onrender.com`
4. Click **"Create Web Service"**

---

## Option 2: Streamlit Cloud + Render.com

This is the **easiest and most cost-effective** option:

1. **Backend**: Deploy Flask API to Render.com (free tier available)
2. **Frontend**: Deploy Streamlit app to Streamlit Cloud (completely free)

### Steps:

1. **Deploy Backend to Render.com** (follow Step 2 from Option 1)
2. **Deploy Frontend to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **"New app"**
   - Select repository and `streamlit_app.py`
   - Add secret: `BACKEND_URL` = your Render backend URL
   - Deploy!

---

## Option 3: Railway.app

Railway.app offers simple deployment with automatic detection.

### Steps:

1. Go to [railway.app](https://railway.app) and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect your Flask app
5. Add environment variable: `PORT` (Railway sets this automatically)
6. For the frontend, create a second service:
   - Add new service from same repo
   - Set start command: `streamlit run streamlit_app.py --server.port $PORT`
   - Add environment variable: `BACKEND_URL` = your backend Railway URL

---

## Post-Deployment Steps

### 1. Update Frontend Backend URL

After deploying the backend, update the frontend's backend URL:

**If using Streamlit Cloud:**
- Go to app settings → Secrets
- Add/update: `BACKEND_URL=https://your-backend-url.onrender.com`

**If using Render.com:**
- Go to service settings → Environment
- Add: `BACKEND_URL=https://your-backend-url.onrender.com`

### 2. Test Your Deployment

1. **Test Backend Health**:
   ```
   https://your-backend-url.onrender.com/health
   ```
   Should return: `{"status":"ok"}`

2. **Test Frontend**:
   - Open your Streamlit app URL
   - Enter a test article URL
   - Click "Analyze Article"
   - Verify it connects to the backend

### 3. Enable CORS (if needed)

The Flask app already has CORS enabled, but if you encounter CORS errors:

```python
# In app.py, ensure CORS is configured:
CORS(app, resources={r"/*": {"origins": ["*"]}})
```

---

## Troubleshooting

### Backend Issues

**Problem**: Backend fails to start
- **Solution**: Check logs in Render dashboard. Common issues:
  - Missing dependencies in `requirements.txt`
  - spaCy model not downloaded (add to build command)
  - Port configuration (use `$PORT` environment variable)

**Problem**: Backend times out
- **Solution**: Increase timeout in Procfile:
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300
  ```

**Problem**: Model artifacts not found
- **Solution**: Ensure `artifacts/` folder is committed to Git repository

### Frontend Issues

**Problem**: Frontend can't connect to backend
- **Solution**: 
  1. Verify backend URL is correct
  2. Check backend is running (test `/health` endpoint)
  3. Ensure CORS is enabled on backend
  4. Check environment variable `BACKEND_URL` is set correctly

**Problem**: Streamlit app shows errors
- **Solution**: Check Streamlit Cloud logs for Python errors

### General Issues

**Problem**: Free tier limitations
- Render.com free tier: Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading to paid tier for always-on service

**Problem**: Build fails
- **Solution**: 
  - Check all dependencies in `requirements.txt`
  - Verify Python version in `runtime.txt` matches platform support
  - Check build logs for specific error messages

---

## Quick Reference: Environment Variables

### Backend (Flask)
- `PORT`: Automatically set by platform
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `False`

### Frontend (Streamlit)
- `BACKEND_URL`: Your deployed backend URL (e.g., `https://pulsecheck-backend.onrender.com`)

---

## Cost Comparison

| Platform | Backend | Frontend | Free Tier |
|----------|---------|----------|-----------|
| **Render.com** | ✅ | ✅ | Yes (with limitations) |
| **Streamlit Cloud** | ❌ | ✅ | Yes (unlimited) |
| **Railway.app** | ✅ | ✅ | Yes (with credits) |
| **Heroku** | ✅ | ✅ | No (paid only) |

**Recommended**: Use **Streamlit Cloud** (free) for frontend + **Render.com** (free) for backend

---

## Next Steps

1. ✅ Deploy backend to Render.com
2. ✅ Deploy frontend to Streamlit Cloud
3. ✅ Test both services
4. ✅ Share your public URLs!

Your app will be accessible to anyone with the URL! 🎉

---

## Support

If you encounter issues:
1. Check platform-specific documentation
2. Review deployment logs
3. Verify all configuration files are correct
4. Test locally first to ensure everything works

Good luck with your deployment! 🚀



