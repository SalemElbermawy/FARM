# app.py — streamlit run app.py

import streamlit as st
from model_deploy import run_pipeline

st.set_page_config(
    page_title="AI Farming Health Shield",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #060810;
    color: #d0dae8;
    font-family: 'JetBrains Mono', monospace;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden; }

.block-container {
    max-width: 780px !important;
    padding: 60px 40px !important;
    margin: 0 auto;
}

/* ── Glow background ── */
.stApp::after {
    content: '';
    position: fixed;
    top: -300px; left: 50%; transform: translateX(-50%);
    width: 700px; height: 600px;
    background: radial-gradient(ellipse, rgba(0,200,110,0.07) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
}

/* ── Header ── */
.app-header {
    text-align: center;
    margin-bottom: 56px;
}

.app-label {
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #00c86e;
    margin-bottom: 20px;
    display: flex; align-items: center; justify-content: center; gap: 8px;
}

.app-label span {
    width: 24px; height: 1px;
    background: #00c86e;
    display: inline-block;
}

.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #eaf0f8;
    margin-bottom: 16px;
}

.app-title em {
    font-style: normal;
    background: linear-gradient(90deg, #00c86e, #00aaff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.app-desc {
    font-size: 13px;
    color: #4a6080;
    line-height: 1.8;
    max-width: 480px;
    margin: 0 auto;
    letter-spacing: 0.01em;
}

/* ── Upload area ── */
.stFileUploader {
    margin-bottom: 0;
}

.stFileUploader > div {
    background: #0c1018 !important;
    border: 1px solid #1c2535 !important;
    border-radius: 14px !important;
    padding: 36px !important;
    transition: border-color 0.2s !important;
}

.stFileUploader > div:hover {
    border-color: rgba(0,200,110,0.4) !important;
}

.stFileUploader label { display: none !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #00c86e 0%, #00aaff 100%) !important;
    color: #060810 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.04em !important;
    padding: 14px !important;
    width: 100% !important;
    margin-top: 12px !important;
    transition: opacity 0.2s, transform 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Image ── */
.stImage img {
    border-radius: 12px !important;
    border: 1px solid #1c2535 !important;
    margin: 16px 0 !important;
}

/* ── Cards ── */
.card {
    background: #0c1018;
    border: 1px solid #1c2535;
    border-radius: 14px;
    padding: 24px 28px;
    margin: 12px 0;
}

.card-top {
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00c86e;
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 10px;
}

.card-top::before {
    content: '';
    width: 16px; height: 1px;
    background: #00c86e;
    flex-shrink: 0;
}

.card-text {
    font-size: 12.5px;
    line-height: 1.9;
    color: #7a90a8;
    white-space: pre-wrap;
}

/* ── Final report ── */
.report {
    background: #0c1018;
    border: 1px solid rgba(0,200,110,0.25);
    border-radius: 14px;
    padding: 32px 36px;
    margin-top: 12px;
    box-shadow: 0 0 40px rgba(0,200,110,0.04);
}

.report-label {
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00c86e;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1c2535;
    display: flex; align-items: center; gap: 10px;
}

.report-label::before {
    content: '';
    width: 16px; height: 1px;
    background: #00c86e;
    flex-shrink: 0;
}

.report-text {
    font-size: 13px;
    line-height: 2;
    color: #8fa8c0;
    white-space: pre-wrap;
}

/* ── Divider ── */
.sep {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1c2535, transparent);
    margin: 40px 0;
}

/* ── Spinner ── */
.stSpinner > div { color: #00c86e !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <div class="app-label"><span></span>AI Farming Health Shield<span></span></div>
    <div class="app-title">Detect Disease.<br><em>Protect Your Crop.</em></div>
   
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded:
    st.image(uploaded, use_container_width=True)
    run_btn = st.button("Run Full Analysis")

    if run_btn:
        tmp_path = f"tmp_{uploaded.name}"
        with open(tmp_path, "wb") as f:
            f.write(uploaded.read())

        with st.spinner("Running pipeline..."):
            vision_analysis, rag_context, recommendation = run_pipeline(tmp_path)

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="card">
    <div class="card-top">Vision LLM Analysis</div>
    <div class="card-text"><h5>{vision_analysis}</h5></div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="card">
    <div class="card-top">Scientific Context — Research Paper</div>
    <div class="card-text"><h5>{rag_context[:700]}{'...' if len(rag_context) > 700 else ''}</h5></div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="report">
    <div class="report-label">Final Recommendation Report</div>
    <div class="report-text"><h5>{recommendation}</h5></div>
</div>
""", unsafe_allow_html=True)