# ✅ Deployment Checklist

Use this checklist to ensure everything is ready for deployment.

## Pre-Deployment

- [ ] All code is committed to Git repository
- [ ] `requirements.txt` includes all dependencies (including `gunicorn`)
- [ ] `Procfile` exists and is correct
- [ ] `runtime.txt` specifies Python version
- [ ] Model artifacts (`artifacts/` folder) are committed to repository
- [ ] Tested locally - both backend and frontend work together
- [ ] Backend health endpoint (`/health`) works

## Backend Deployment (Render.com)

- [ ] Created Render.com account
- [ ] Connected GitHub repository
- [ ] Created new Web Service
- [ ] Set build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- [ ] Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
- [ ] Deployment successful
- [ ] Backend URL copied (e.g., `https://pulsecheck-backend.onrender.com`)
- [ ] Tested `/health` endpoint - returns `{"status":"ok"}`

## Frontend Deployment

### Option A: Streamlit Cloud
- [ ] Created Streamlit Cloud account (via GitHub)
- [ ] Created new app
- [ ] Selected repository and `streamlit_app.py`
- [ ] Added secret: `BACKEND_URL` = backend URL from above
- [ ] Deployment successful
- [ ] Frontend URL copied

### Option B: Render.com
- [ ] Created new Web Service in Render
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- [ ] Added environment variable: `BACKEND_URL` = backend URL
- [ ] Deployment successful

## Post-Deployment Testing

- [ ] Frontend loads without errors
- [ ] Can enter article URL in frontend
- [ ] "Analyze Article" button works
- [ ] Backend receives requests (check backend logs)
- [ ] Analysis results display correctly
- [ ] All visualizations render properly
- [ ] No CORS errors in browser console

## Final Steps

- [ ] Share your public URLs with others!
- [ ] Bookmark your deployment URLs
- [ ] Monitor logs for any errors
- [ ] Consider setting up custom domain (optional)

## Quick Test URLs

Test with these article URLs:
- `https://www.bbc.com/news`
- `https://www.reuters.com/world/`
- `https://www.cnn.com/`

---

**Deployment Complete! 🎉**

Your app is now live and accessible to everyone!


