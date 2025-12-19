"""Streamlit frontend dashboard for PulseCheck."""

import os
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="PulseCheck - Political Bias Detection", layout="wide")

st.title("🔍 PulseCheck - Political Bias Detection")
st.markdown("Analyze news articles for political bias, sentiment, topics, and entities")

# Sidebar
st.sidebar.header("Configuration")
# Get backend URL from environment variable or use default
default_backend_url = os.getenv("BACKEND_URL", "http://localhost:5000")
backend_url = st.sidebar.text_input("Backend URL", value=default_backend_url)
summarize = st.sidebar.checkbox("Include Summary", value=False)

# Main input
url = st.text_input("Enter News Article URL", placeholder="https://example.com/article")

if st.button("Analyze Article", type="primary"):
    if not url:
        st.error("Please enter a URL")
    else:
        with st.spinner("Analyzing article..."):
            try:
                response = requests.post(
                    f"{backend_url}/analyze",
                    json={"url": url, "summarize": summarize},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state["result"] = result
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")

# Display results
if "result" in st.session_state:
    result = st.session_state["result"]
    
    # Header info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Source", result.get("source", "Unknown"))
    with col2:
        st.metric("Bias", result.get("bias", "Unknown").upper())
    with col3:
        st.metric("Confidence", f"{result.get('confidence', 0):.1%}")
    
    # Explanation tooltip
    with st.expander("ℹ️ What do these metrics mean?"):
        st.markdown("""
        **Bias Confidence (36.3%)**: How confident the model is that the article is RIGHT-leaning.
        - This is the ML model's prediction confidence for political bias (left/center/right)
        - Lower confidence (30-40%) means the model is less certain
        
        **Sentiment (Neutral)**: Emotional tone of the writing (positive/negative/neutral)
        - Different from bias! An article can be neutral in tone but still have political bias
        - Example: A neutral news report can still lean left or right in its framing
        
        **Subjectivity (31%)**: How opinionated vs factual the text is
        - 0% = Very factual/objective
        - 100% = Very opinionated/subjective
        - Different from confidence! Subjectivity measures opinion vs fact, not prediction certainty
        """)
    
    if result.get("headline"):
        st.subheader(result["headline"])
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Bias Probability")
        bias_labels = ["left", "center", "right"]
        # Create probability distribution (simplified - using confidence)
        bias_probs = [0.0, 0.0, 0.0]
        predicted_bias = result.get("bias", "center").lower()
        confidence = result.get("confidence", 0.5)
        
        bias_idx = bias_labels.index(predicted_bias) if predicted_bias in bias_labels else 1
        bias_probs[bias_idx] = confidence
        # Distribute remaining probability
        remaining = (1 - confidence) / 2
        for i in range(3):
            if i != bias_idx:
                bias_probs[i] = remaining
        
        fig_bias = px.bar(
            x=[l.upper() for l in bias_labels],
            y=bias_probs,
            labels={"x": "Bias", "y": "Probability"},
            color=bias_labels,
            color_discrete_map={"left": "#3498db", "center": "#95a5a6", "right": "#e74c3c"}
        )
        fig_bias.update_layout(showlegend=False, yaxis_range=[0, 1])
        st.plotly_chart(fig_bias, use_container_width=True)
    
    with col2:
        st.subheader("😊 Sentiment Gauge")
        sentiment = result.get("sentiment", "neutral")
        polarity = result.get("polarity", 0.0)
        
        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=polarity * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Sentiment"},
            gauge={
                "axis": {"range": [-100, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [-100, -33], "color": "lightcoral"},
                    {"range": [-33, 33], "color": "lightgray"},
                    {"range": [33, 100], "color": "lightgreen"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 0
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(f"Sentiment: {sentiment.upper()} | Subjectivity: {result.get('subjectivity', 0):.2%}")
    
    st.divider()
    
    # Topics
    st.subheader("📝 Topics & Keywords")
    topics = result.get("topics", [])
    if topics:
        for topic in topics:
            keywords = ", ".join(topic.get("keywords", []))
            st.write(f"**Topic {topic.get('topic_id', 0) + 1}:** {keywords}")
    else:
        st.info("No topics extracted")
    
    st.divider()
    
    # Entities
    st.subheader("👥 Key Entities")
    entities = result.get("entities", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**People**")
        people = entities.get("people", [])
        if people:
            for person in people:
                st.write(f"• {person}")
        else:
            st.write("*None found*")
    
    with col2:
        st.write("**Organizations**")
        orgs = entities.get("organizations", [])
        if orgs:
            for org in orgs:
                st.write(f"• {org}")
        else:
            st.write("*None found*")
    
    with col3:
        st.write("**Places**")
        places = entities.get("places", [])
        if places:
            for place in places:
                st.write(f"• {place}")
        else:
            st.write("*None found*")
    
    st.divider()
    
    # Summary
    if "summary" in result:
        st.subheader("📄 Summary")
        st.write(result["summary"])
    
    # Full text preview
    with st.expander("View Full Article Text"):
        st.text(result.get("text", ""))

