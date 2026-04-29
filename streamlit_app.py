"""Streamlit frontend dashboard for PulseCheck."""

import os
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="PulseCheck - Political Bias Detection", layout="wide")

st.title("🔍 PulseCheck - Political Bias Detection")
st.markdown("Analyze news articles for political bias, sentiment, topics, and entities — **in any language**")

# ── Sidebar ──────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuration")
# Get backend URL from environment variable or use default
default_backend_url = os.getenv("BACKEND_URL", "http://localhost:5000")
backend_url = st.sidebar.text_input("Backend URL", value=default_backend_url)
summarize = st.sidebar.checkbox("Include Summary", value=False)
model_choice = st.sidebar.selectbox(
    "Bias Model",
    options=["svm (current)", "transformer (RoBERTa/BERT)"],
    index=0,
)

# ── Language settings (sidebar) ──────────────────────────────────────
st.sidebar.divider()
st.sidebar.header("🌐 Language Settings")

# Build language list for the dropdown
_LANGUAGE_OPTIONS = [
    ("Auto-detect", None),
    ("English", "en"), ("Hindi — हिन्दी", "hi"),
    ("Spanish — Español", "es"), ("French — Français", "fr"),
    ("German — Deutsch", "de"), ("Portuguese", "pt"),
    ("Russian — Русский", "ru"), ("Chinese — 中文", "zh-cn"),
    ("Japanese — 日本語", "ja"), ("Korean — 한국어", "ko"),
    ("Arabic — العربية", "ar"), ("Italian", "it"),
    ("Dutch", "nl"), ("Turkish", "tr"), ("Polish", "pl"),
    ("Ukrainian — Українська", "uk"), ("Swedish", "sv"),
    ("Danish", "da"), ("Norwegian", "no"), ("Finnish", "fi"),
    ("Greek — Ελληνικά", "el"), ("Czech", "cs"),
    ("Romanian", "ro"), ("Hungarian", "hu"),
    ("Thai — ไทย", "th"), ("Vietnamese", "vi"),
    ("Indonesian", "id"), ("Malay", "ms"),
    ("Tamil — தமிழ்", "ta"), ("Telugu — తెలుగు", "te"),
    ("Bengali — বাংলা", "bn"), ("Marathi — मराठी", "mr"),
    ("Gujarati — ગુજરાતી", "gu"), ("Kannada — ಕನ್ನಡ", "kn"),
    ("Malayalam — മലയാളം", "ml"), ("Punjabi — ਪੰਜਾਬੀ", "pa"),
    ("Urdu — اردو", "ur"), ("Persian — فارسی", "fa"),
    ("Hebrew — עברית", "he"), ("Swahili", "sw"),
]

lang_display = [f"{name}" for name, _ in _LANGUAGE_OPTIONS]
selected_lang_idx = st.sidebar.selectbox(
    "Article Language",
    options=range(len(_LANGUAGE_OPTIONS)),
    format_func=lambda i: lang_display[i],
    index=0,
    help="Auto-detect works for most articles. Use manual override if detection is wrong.",
)
language_override = _LANGUAGE_OPTIONS[selected_lang_idx][1]  # None means auto-detect

st.sidebar.caption(
    "PulseCheck supports **40+ languages**. Non-English articles are "
    "automatically translated to English for bias & sentiment analysis."
)

# ── Main Input — Tabs for URL vs Paste Text ──────────────────────────
tab_url, tab_text = st.tabs(["🔗 Enter URL", "📝 Paste Article Text"])

with tab_url:
    url_input = st.text_input(
        "News Article URL",
        placeholder="https://example.com/article",
        key="url_input",
    )

with tab_text:
    text_input = st.text_area(
        "Paste article text in any language",
        height=200,
        placeholder="Paste the full article text here (Hindi, Spanish, French, Arabic, etc.)…",
        key="text_input",
    )

if st.button("🔍 Analyze Article", type="primary", use_container_width=True):
    has_url = url_input and url_input.strip()
    has_text = text_input and text_input.strip()

    if not has_url and not has_text:
        st.error("Please enter a URL **or** paste article text.")
    else:
        with st.spinner("Analyzing article…"):
            try:
                payload = {
                    "summarize": summarize,
                    "bias_model": "transformer" if model_choice.startswith("transformer") else "svm",
                }
                if language_override:
                    payload["language_override"] = language_override

                # Prefer URL if both are provided
                if has_url:
                    payload["url"] = url_input.strip()
                else:
                    payload["text"] = text_input.strip()

                response = requests.post(
                    f"{backend_url}/analyze",
                    json=payload,
                    timeout=180,
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state["result"] = result
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")

# ── Display results ──────────────────────────────────────────────────
if "result" in st.session_state:
    result = st.session_state["result"]
    
    # Header info — 4 metric columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Source", result.get("source", "Unknown"))
    with col2:
        st.metric("Bias", result.get("bias", "Unknown").upper())
    with col3:
        st.metric("Confidence", f"{result.get('confidence', 0):.1%}")
    with col4:
        lang_name = result.get("language", "English")
        lang_flag = result.get("language_flag", "🌍" if result.get("is_translated") else "🇺🇸")
        st.metric("Language", f"{lang_flag} {lang_name}")

    st.caption(f"Bias model: {result.get('bias_model', 'svm')}")

    # ── Multilingual banner ──────────────────────────────────────────
    if result.get("is_translated"):
        native = result.get("language_native_name", "")
        conf_label = result.get("language_confidence", "")
        conf_score = result.get("language_confidence_score", 0)

        banner_parts = [
            f"🌐 **Multilingual Analysis:** This article was detected as "
            f"**{result.get('language', 'Unknown')}**",
        ]
        if native and native != result.get("language", ""):
            banner_parts[0] += f" ({native})"

        banner_parts[0] += (
            f" with **{conf_label}** confidence ({conf_score:.0%}), "
            f"and automatically translated to English for bias & sentiment analysis."
        )
        st.info("\n".join(banner_parts))

    # Sentiment fallback warning
    if result.get("sentiment_fallback"):
        st.warning(
            "⚠️ Sentiment analysis could not be performed accurately for this "
            "language. The values shown are neutral defaults."
        )
    
    # Explanation tooltip
    with st.expander("ℹ️ What do these metrics mean?"):
        st.markdown("""
        **Bias Confidence**: How confident the model is about the predicted political leaning.
        - This is the ML model's prediction confidence for political bias (left/center/right)
        - Lower confidence (30-40%) means the model is less certain
        
        **Sentiment**: Emotional tone of the writing (positive/negative/neutral)
        - Different from bias! An article can be neutral in tone but still have political bias
        - Example: A neutral news report can still lean left or right in its framing
        
        **Subjectivity**: How opinionated vs factual the text is
        - 0% = Very factual/objective
        - 100% = Very opinionated/subjective
        - Different from confidence! Subjectivity measures opinion vs fact, not prediction certainty

        **🌐 Multilingual Articles**: Non-English articles are automatically detected and
        translated to English before bias & sentiment analysis. Named entities are extracted
        from the original text using a multilingual NER model.
        """)
    
    # Headline display
    if result.get("headline"):
        st.subheader(result["headline"])
        # Show original headline if it's different (translated)
        if (
            result.get("original_headline")
            and result["original_headline"] != result["headline"]
        ):
            st.caption(f"Original: {result['original_headline']}")
    
    st.divider()
    
    # ── Visualizations ───────────────────────────────────────────────
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Bias Probability")
        bias_labels = ["left", "center", "right"]
        # Prefer real probability distribution if provided (transformer path),
        # otherwise fall back to the previous "confidence + remaining" heuristic.
        probs_dict = result.get("bias_probabilities") or {}
        if probs_dict and all(k in probs_dict for k in bias_labels):
            bias_probs = [float(probs_dict[k]) for k in bias_labels]
        else:
            bias_probs = [0.0, 0.0, 0.0]
            predicted_bias = result.get("bias", "center").lower()
            confidence = result.get("confidence", 0.5)
            bias_idx = bias_labels.index(predicted_bias) if predicted_bias in bias_labels else 1
            bias_probs[bias_idx] = confidence
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
    
    # ── Topics ───────────────────────────────────────────────────────
    st.subheader("📝 Topics & Keywords")
    topics = result.get("topics", [])
    if topics:
        for topic in topics:
            keywords = ", ".join(topic.get("keywords", []))
            st.write(f"**Topic {topic.get('topic_id', 0) + 1}:** {keywords}")
    else:
        st.info("No topics extracted")
    
    st.divider()
    
    # ── Entities ─────────────────────────────────────────────────────
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
    
    # ── Summary ──────────────────────────────────────────────────────
    if "summary" in result:
        st.subheader("📄 Summary")
        st.write(result["summary"])
    
    # ── Translated text (for non-English articles) ───────────────────
    if result.get("is_translated") and result.get("translated_text"):
        with st.expander("🌐 View Translated Text (English)"):
            st.text(result.get("translated_text", ""))

    # ── Full original text ───────────────────────────────────────────
    with st.expander("View Full Article Text (Original)"):
        st.text(result.get("text", ""))

    # ── Language detection details ───────────────────────────────────
    with st.expander("🔬 Language Detection Details"):
        lang_cols = st.columns(3)
        with lang_cols[0]:
            st.write(f"**Detected Language:** {result.get('language', 'N/A')}")
            native = result.get("language_native_name", "")
            if native and native != result.get("language", ""):
                st.write(f"**Native Name:** {native}")
        with lang_cols[1]:
            st.write(f"**Language Code:** `{result.get('language_code', 'N/A')}`")
            st.write(f"**Detection Confidence:** {result.get('language_confidence', 'N/A')}")
        with lang_cols[2]:
            conf_score = result.get("language_confidence_score", 0)
            st.write(f"**Confidence Score:** {conf_score:.1%}")
            st.write(f"**Was Translated:** {'Yes ✅' if result.get('is_translated') else 'No'}")
