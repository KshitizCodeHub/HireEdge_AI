import streamlit as st
from career_backend_simple import career_assistant, extract_text_from_pdf
import json
import time

# Page configuration
st.set_page_config(
    page_title="HireEdge AI - Your AI-Powered Career Strategist",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "HireEdge AI - Get the competitive edge in your placement season with AI-powered career optimization!"
    }
)

# Initialize session state for persistence
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'company_research' not in st.session_state:
    st.session_state.company_research = {}
if 'job_match_results' not in st.session_state:
    st.session_state.job_match_results = {}
if 'interview_prep' not in st.session_state:
    st.session_state.interview_prep = {}
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""

# Custom CSS for Dark Theme
st.markdown("""
<style>
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #ffffff;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #00d4ff, #0099cc, #ff6b00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-family: 'Segoe UI', system-ui, sans-serif;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border: 1px solid #333;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00d4ff, #ff00ff, #ff6b00);
        border-radius: 15px 15px 0 0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.2);
        border-color: #00d4ff;
    }
    
    .feature-card h3 {
        color: #00d4ff;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .feature-card p {
        color: #b8b8b8;
        line-height: 1.6;
    }
    
    /* Success Metrics */
    .success-metric {
        background: linear-gradient(145deg, #1a4d3a, #2d6b4f);
        border: 1px solid #4ade80;
        padding: 0.8rem;
        border-radius: 10px;
        color: #4ade80;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 15px rgba(74, 222, 128, 0.2);
        margin: 0.5rem 0;
    }
    
    /* Natural Scrolling Sidebar with Enhanced Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a0a0a, #1a1a1a);
        border-right: 2px solid #00d4ff;
        box-shadow: 2px 0 10px rgba(0, 212, 255, 0.1);
    }
    
    .css-1lcbmhc {
        background: linear-gradient(180deg, #0a0a0a, #1a1a1a);
        border-right: 2px solid #00d4ff;
    }
    
    /* Compact Sidebar Title */
    .css-1d391kg .element-container:first-child {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border-radius: 8px;
        margin: 0.5rem 0;
        padding: 0.8rem;
        border: 1px solid #00d4ff;
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.3);
    }
    
    /* Compact Section Headers */
    .css-1d391kg h1 {
        color: #00d4ff !important;
        font-size: 1.3rem !important;
        margin: 0 !important;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.6);
    }
    
    .css-1d391kg h2, .css-1d391kg h3 {
        color: #00d4ff !important;
        font-size: 1rem !important;
        margin: 0.5rem 0 0.3rem 0 !important;
        text-shadow: 0 0 5px rgba(0, 212, 255, 0.4);
    }
    
    /* Ultra-Compact Text and Spacing */
    .css-1d391kg .element-container {
        margin-bottom: 0.2rem;
    }
    
    .css-1d391kg p {
        color: #e0e0e0;
        font-size: 0.8rem;
        margin: 0.1rem 0;
        line-height: 1.2;
    }
    
    /* Compact subtitle */
    .css-1d391kg em {
        color: #888;
        font-size: 0.75rem;
        line-height: 1.1;
    }
    
    /* Reduce overall sidebar padding */
    .css-1d391kg {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #0099cc);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #0099cc, #0066aa);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);
    }
    
    /* Compact Sidebar Button Styling */
    .css-1d391kg .stButton > button {
        width: 100%;
        margin: 0.2rem 0;
        font-size: 0.85rem;
        padding: 0.5rem 0.8rem;
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Debug button */
    .css-1d391kg .stButton:nth-last-child(2) > button {
        background: linear-gradient(45deg, #ff6b00, #ff4400);
        box-shadow: 0 2px 8px rgba(255, 107, 0, 0.3);
    }
    
    /* Clear button */
    .css-1d391kg .stButton:nth-last-child(1) > button {
        background: linear-gradient(45deg, #ff4444, #cc0000);
        box-shadow: 0 2px 8px rgba(255, 68, 68, 0.3);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border: 2px dashed #00d4ff;
        border-radius: 15px;
        padding: 2rem;
    }
    
    .stFileUploader:hover {
        border-color: #ff00ff;
        background: linear-gradient(145deg, #2a2a2a, #1e1e1e);
    }
    
    /* Text Areas */
    .stTextArea textarea {
        background: #1a1a1a;
        border: 1px solid #333;
        color: #ffffff;
        border-radius: 10px;
    }
    
    .stTextInput input {
        background: #1a1a1a;
        border: 1px solid #333;
        color: #ffffff;
        border-radius: 10px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        color: #00d4ff;
        border-radius: 10px;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border-left: 4px solid #00d4ff;
        color: #ffffff;
    }
    
    /* Compact Selectbox with reliable arrow */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
        border: 1px solid #00d4ff;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.2);
        position: relative;
    }
    
    .stSelectbox select {
        background: transparent;
        color: #ffffff;
        border: none;
        font-weight: 500;
        padding: 0.6rem 2rem 0.6rem 0.8rem;
        font-size: 0.9rem;
        appearance: none;
        -webkit-appearance: none;
        -moz-appearance: none;
    }
    
    /* Reliable dropdown arrow with multiple fallbacks */
    .stSelectbox > div > div::before {
        content: '⯆';
        position: absolute;
        right: 0.8rem;
        top: 50%;
        transform: translateY(-50%);
        color: #00d4ff;
        font-size: 0.9rem;
        pointer-events: none;
        z-index: 10;
        font-family: 'Arial', sans-serif;
    }
    
    /* Alternative arrow if first doesn't work */
    .css-1d391kg .stSelectbox > div > div::after {
        content: '▾';
        position: absolute;
        right: 0.8rem;
        top: 50%;
        transform: translateY(-50%);
        color: #00d4ff;
        font-size: 0.8rem;
        pointer-events: none;
        z-index: 9;
    }
    
    .stSelectbox select:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.4);
    }
    
    /* Progress indicators */
    .stSpinner {
        color: #00d4ff;
    }
    
    /* Columns spacing */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer-style {
        background: linear-gradient(135deg, #0a0a0a, #1a1a1a);
        padding: 2rem;
        text-align: center;
        color: #666;
        border-top: 1px solid #333;
        margin-top: 3rem;
    }
    
    /* Glow effect for important elements */
    .glow-effect {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        border: 1px solid rgba(0, 212, 255, 0.5);
        border-radius: 10px;
        padding: 1rem;
        background: rgba(0, 212, 255, 0.05);
    }
    
    /* Compact Sidebar Status Indicators */
    .css-1d391kg .stSuccess {
        background: linear-gradient(135deg, #00ff88, #00cc66);
        border: 1px solid #00ff88;
        border-radius: 6px;
        color: #000;
        font-weight: 500;
        margin: 0.1rem 0;
        padding: 0.3rem 0.6rem;
        font-size: 0.8rem;
    }
    
    .css-1d391kg .stInfo {
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        border: 1px solid #00d4ff;
        border-radius: 6px;
        color: #000;
        font-weight: 500;
        margin: 0.1rem 0;
        padding: 0.3rem 0.6rem;
        font-size: 0.8rem;
    }
    
    /* Status indicators */
    .status-complete {
        background: linear-gradient(45deg, #22c55e, #16a34a);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .status-pending {
        background: linear-gradient(45deg, #6b7280, #4b5563);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    /* Analysis results styling */
    .analysis-container {
        background: linear-gradient(145deg, #1a1a1a, #252525);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .section-title {
        color: #00d4ff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #333;
    }
    
    /* Enhanced Result Cards */
    .result-box {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border: 1px solid #00d4ff;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
    }
    
    /* Compact Sidebar Dividers */
    .css-1d391kg hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        margin: 0.8rem 0;
        border-radius: 1px;
    }
    
    /* Enhanced Text Styling */
    .analysis-text {
        color: #e0e0e0;
        line-height: 1.8;
        font-size: 1.1rem;
        background: rgba(0, 0, 0, 0.3);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 3px solid #ff6b00;
        margin: 1rem 0;
    }
    
    /* Status Indicators */
    .status-good { color: #00ff88; font-weight: bold; }
    .status-warning { color: #ffaa00; font-weight: bold; }
    .status-error { color: #ff4444; font-weight: bold; }
    
    /* Compact Debug Text Styling */
    .css-1d391kg .stExpander .stText {
        background: linear-gradient(135deg, #1a1a1a, #0f0f0f);
        border: 1px solid #333;
        border-radius: 5px;
        padding: 0.3rem 0.5rem;
        font-size: 0.75rem;
        margin: 0.1rem 0;
        color: #ccc;
    }
    
    /* Compact expander styling */
    .css-1d391kg .stExpander {
        margin: 0.3rem 0;
    }
    
    .css-1d391kg .stExpander .streamlit-expanderHeader {
        padding: 0.4rem 0.6rem;
        font-size: 0.85rem;
    }
    
    /* Subtle Custom Scrollbars */
    .css-1d391kg::-webkit-scrollbar {
        width: 4px;
    }
    
    .css-1d391kg::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .css-1d391kg::-webkit-scrollbar-thumb {
        background: rgba(0, 212, 255, 0.3);
        border-radius: 2px;
    }
    
    .css-1d391kg::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 212, 255, 0.5);
    }
    
    /* Improved Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, #2a2a2a, #1e1e1e);
        border: 1px solid #00d4ff;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for persistence - with debug info
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'company_research' not in st.session_state:
    st.session_state.company_research = {}
    # print("DEBUG: Initialized company_research session state")  # Commented out for production
if 'job_match_results' not in st.session_state:
    st.session_state.job_match_results = {}
if 'interview_prep' not in st.session_state:
    st.session_state.interview_prep = {}

# Sidebar navigation
st.sidebar.title("⚡ HireEdge AI")
st.sidebar.markdown("*Your AI-Powered Career Strategist*")

# Show persistent data status with details
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Session Data")
st.sidebar.markdown('<style>.css-1d391kg .element-container ul li { color: #00d4ff; font-size: 0.75rem; margin: 0.05rem 0; } .css-1d391kg .stText { font-size: 0.75rem; margin: 0.05rem 0; line-height: 1.2; }</style>', unsafe_allow_html=True)
if st.session_state.resume_text:
    st.sidebar.success(f"✅ Resume loaded ({len(st.session_state.resume_text)} chars)")
else:
    st.sidebar.info("📝 No resume loaded")

if st.session_state.analysis_results:
    st.sidebar.success(f"✅ {len(st.session_state.analysis_results)} analyses")

if st.session_state.company_research:
    st.sidebar.success(f"✅ {len(st.session_state.company_research)} companies")

if st.session_state.job_match_results:
    st.sidebar.success(f"✅ {len(st.session_state.job_match_results)} matches")

st.sidebar.markdown("---")

# Compact debug info
with st.sidebar.expander("🔍 Debug Info", expanded=False):
    st.text(f"Resume: {len(st.session_state.resume_text) if st.session_state.resume_text else 0} chars")
    if st.session_state.analysis_results:
        st.text(f"Analyses: {', '.join(st.session_state.analysis_results.keys())}")
    if st.session_state.company_research:
        companies = list(st.session_state.company_research.keys())
        st.text(f"Companies ({len(companies)}): {', '.join(companies[:2])}{'...' if len(companies) > 2 else ''}")
        # Show last research timestamp
        if companies:
            last_company = companies[-1]
            if 'timestamp' in st.session_state.company_research[last_company]:
                st.text(f"Last: {st.session_state.company_research[last_company]['timestamp']}")
    if st.session_state.job_match_results:
        st.text(f"Matches: {len(st.session_state.job_match_results)}")

if st.sidebar.button("🗑️ Clear All Data"):
    for key in ['resume_text', 'job_description', 'company_name', 'analysis_results', 'company_research', 'job_match_results', 'interview_prep']:
        if key in st.session_state:
            st.session_state[key] = "" if key in ['resume_text', 'job_description', 'company_name'] else {}
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown("### 🛠️ Choose Your Tool:")
page = st.sidebar.selectbox(
    "Navigation Menu",  # Proper label for accessibility
    ["🏠 Home", "📝 Resume Analyzer", "🎯 Job Matcher", "🏢 Company Research", "💼 Interview Prep", "📊 Dashboard"],
    label_visibility="collapsed"
)

# Configuration section
CONFIG = {'configurable': {'thread_id': 'career-session'}}

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">⚡ HireEdge AI</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to HireEdge AI - Your Career Advantage!
    
    Get the competitive edge in your placement season with AI-powered resume optimization, company research, and interview preparation.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>📝 Resume Optimizer</h3>
        <p>Upload your resume and get AI-powered optimization suggestions with ATS compatibility analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🎯 Job Matching</h3>
        <p>Compare your resume against job descriptions and identify skill gaps with precise match scoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>💼 Interview Prep</h3>
        <p>Get comprehensive company research and practice interview questions tailored to your role</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Get Started")
    st.info("👈 Choose a tool from the sidebar to begin optimizing your career!")

# RESUME ANALYZER PAGE
elif page == "📝 Resume Analyzer":
    st.markdown('<div class="section-title">📝 HireEdge Resume Optimizer</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glow-effect">Upload your resume (PDF) to get detailed AI-powered analysis and ATS optimization suggestions.</div>', unsafe_allow_html=True)
    
    # Show previous results if available - ALWAYS at top
    if 'resume' in st.session_state.analysis_results:
        st.markdown("### 📊 Previous Resume Analysis Results")
        prev_result = st.session_state.analysis_results['resume']
        
        # Display metrics prominently
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ATS Score", f"{prev_result['ats_score']}/100", delta=f"{prev_result['ats_score']-75}%")
        with col2:
            st.metric("Skills Found", len(prev_result['extracted_skills']))
        with col3:
            st.metric("Issues Found", len(prev_result['issues']))
        
        # Show analysis in expandable section
        with st.expander("📄 Full Analysis Report", expanded=True):
            st.markdown('<div class="analysis-text">', unsafe_allow_html=True)
            st.write(prev_result["analysis"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Show current resume status
    if st.session_state.resume_text:
        st.success(f"✅ Resume loaded ({len(st.session_state.resume_text)} characters)")
        if st.button("🔍 Re-analyze Current Resume", type="primary"):
            with st.spinner("AI is analyzing your resume... (this may take 30-60 seconds)"):
                try:
                    result = career_assistant.analyze_resume(st.session_state.resume_text)
                    if result.get("success"):
                        st.session_state.analysis_results['resume'] = result
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
    
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = resume_text
        
        if resume_text and not resume_text.startswith("❌"):
            st.success("✅ Resume uploaded successfully!")
            
            with st.expander("📄 Extracted Resume Text (Preview)"):
                st.text_area("Resume Content", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200)
            
            if st.button("🔍 Analyze Resume", type="primary"):
                with st.spinner("AI is analyzing your resume... (this may take 30-60 seconds)"):
                    try:
                        # Use the resume text from session state or current text
                        analysis_text = st.session_state.resume_text if st.session_state.resume_text else resume_text
                        result = career_assistant.analyze_resume(analysis_text)
                        
                        if result.get("success"):
                            # Store results first with timestamp
                            import datetime
                            result['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.analysis_results['resume'] = result
                            
                            # Display results with enhanced styling
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            st.markdown('### 📊 Resume Analysis Results')
                            
                            # Show metrics first
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("ATS Score", f"{result['ats_score']}/100", f"{result['ats_score']-75}%")
                            with col2:
                                st.metric("Skills Found", len(result['extracted_skills']))
                            with col3:
                                st.metric("Issues Found", len(result['issues']))
                            
                            # Display analysis text with proper formatting
                            st.markdown('<div class="analysis-text">', unsafe_allow_html=True)
                            st.write(result["analysis"])  # Already cleaned in backend
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                            st.markdown("**Possible solutions:**")
                            st.markdown("- Wait a moment and try again")
                            st.markdown("- Check internet connection") 
                            st.markdown("- API might be temporarily busy")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        st.markdown("**Troubleshooting:**")
                        st.markdown("- The AI service might be busy, please try again")
                        st.markdown("- Check if your resume text is clear and readable")
        else:
            st.error("PDF Processing Failed")
            if resume_text:
                st.markdown(resume_text)
            
            # Add manual text input option
            st.markdown("---")
            st.markdown("### 📝 Alternative: Paste Resume Text")
            st.info("If PDF upload isn't working, you can paste your resume text directly below:")
            
            manual_text = st.text_area(
                "Paste your resume text here:",
                value=st.session_state.resume_text if st.session_state.resume_text and not st.session_state.resume_text.startswith("❌") else "",
                height=300,
                placeholder="Copy and paste your resume content here..."
            )
            
            if manual_text and manual_text != st.session_state.resume_text:
                st.session_state.resume_text = manual_text
                st.success("✅ Resume text updated successfully!")
                st.rerun()
            
            if manual_text:
                with st.expander("📄 Resume Text Preview"):
                    st.text_area("Content Preview", manual_text[:1000] + "..." if len(manual_text) > 1000 else manual_text, height=200, disabled=True)
            
            # Add sample resume for testing
            if st.button("🔬 Use Sample Resume (For Testing)", type="secondary"):
                sample_resume = """
                John Smith
                Software Engineer
                Email: john.smith@email.com | Phone: (555) 123-4567
                LinkedIn: linkedin.com/in/johnsmith
                
                SUMMARY
                Experienced Software Engineer with 3+ years in full-stack development. 
                Proficient in Python, JavaScript, React, and cloud technologies. 
                Strong background in AI/ML and database management.
                
                EXPERIENCE
                Software Engineer | Tech Corp | 2022-Present
                • Developed web applications using React, Node.js, and Python
                • Implemented REST APIs serving 10K+ daily users
                • Worked with AWS, Docker, and CI/CD pipelines
                • Collaborated with cross-functional teams using Agile methodology
                
                Junior Developer | StartupXYZ | 2021-2022
                • Built responsive web interfaces using HTML, CSS, JavaScript
                • Integrated third-party APIs and payment systems
                • Maintained MySQL databases and optimized queries
                • Participated in code reviews and debugging sessions
                
                EDUCATION
                Bachelor of Computer Science | University ABC | 2021
                Relevant Coursework: Data Structures, Algorithms, Database Systems
                
                SKILLS
                Programming: Python, JavaScript, Java, SQL, HTML, CSS
                Frameworks: React, Node.js, Django, Flask, Express.js
                Databases: MySQL, PostgreSQL, MongoDB, Redis
                Cloud: AWS, Azure, Docker, Kubernetes
                Tools: Git, Jenkins, Postman, VS Code
                Soft Skills: Problem-solving, Team collaboration, Communication
                
                PROJECTS
                E-commerce Platform | Personal Project
                • Built full-stack e-commerce site with React and Node.js
                • Implemented user authentication, payment processing, inventory management
                • Deployed on AWS with CI/CD pipeline
                
                Machine Learning Model | Academic Project  
                • Developed predictive model using Python, pandas, scikit-learn
                • Achieved 85% accuracy in customer behavior prediction
                • Presented findings to faculty and industry partners
                """
                
                st.session_state.resume_text = sample_resume.strip()
                st.success("✅ Sample resume loaded for testing!")
                st.rerun()

# JOB MATCHER PAGE
elif page == "🎯 Job Matcher":
    st.markdown('<div class="section-title">🎯 HireEdge Job Matcher</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glow-effect">Compare your resume against a specific job description to find match percentage and improvement areas.</div>', unsafe_allow_html=True)
    
    # Show previous results if available
    if st.session_state.job_match_results:
        with st.expander("📈 Previous Job Match Results", expanded=False):
            for job_key, match_result in st.session_state.job_match_results.items():
                st.markdown(f"### {job_key.replace('_', ' ')[:100]}...")
                if 'timestamp' in match_result:
                    st.caption(f"Analyzed on: {match_result['timestamp']}")
                if match_result.get('compatibility_score'):
                    st.metric("Compatibility Score", f"{match_result['compatibility_score']}/100")
                clean_analysis = match_result["analysis"].replace('<div>', '').replace('</div>', '').replace('<br>', '\n')
                st.write(clean_analysis[:300] + "..." if len(clean_analysis) > 300 else clean_analysis)
                st.markdown("---")
    
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload your resume first in the Resume Analyzer page.")
    else:
        st.success("✅ Resume loaded!")
    
    st.markdown("### Job Description")
    job_description = st.text_area(
        "Paste the job description here:",
        value=st.session_state.job_description,
        height=200,
        placeholder="Copy and paste the full job description from the company's posting..."
    )
    
    # Update session state if job description changes
    if job_description != st.session_state.job_description:
        st.session_state.job_description = job_description
    
    # Add debug storage information
    with st.expander("🗂️ Debug: Storage Information", expanded=False):
        st.markdown("**Current Session State:**")
        st.write(f"Total Job Match Records: {len(st.session_state.job_match_results)}")
        if st.session_state.job_match_results:
            st.write("Stored Job Matches:", list(st.session_state.job_match_results.keys()))
            for job_key, data in st.session_state.job_match_results.items():
                st.write(f"- {job_key}: {data.get('timestamp', 'No timestamp')} (Score: {data.get('compatibility_score', 'N/A')})")
        
    if st.button("🎯 Analyze Job Match", type="primary"):
        if st.session_state.resume_text and job_description:
            with st.spinner("Analyzing job match... (this may take 30-60 seconds)"):
                try:
                    # Use simplified direct job matching
                    result = career_assistant.match_jobs(st.session_state.resume_text, job_description)
                    
                    if result.get("success"):
                        st.markdown('<div class="analysis-container">')
                        st.markdown('<div class="section-title">📈 HireEdge Match Analysis</div>')
                        st.markdown(result["analysis"])
                        
                        # Show match metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Compatibility Score", f"{result['compatibility_score']}/100")
                        with col2:
                            st.metric("Your Skills", len(result['resume_skills']))
                        with col3:
                            st.metric("Job Requirements", len(result['job_skills']))
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Store results with timestamp and proper key
                        import datetime
                        result['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        job_key = f"job_match_{job_description[:50].replace(' ', '_') if job_description else 'general'}"
                        st.session_state.job_match_results[job_key] = result
                        
                        st.success(f"✅ Job match analysis saved successfully!")
                        st.balloons()
                    else:
                        st.error(f"❌ Job matching failed: {result.get('error', 'Unknown error')}")
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
        else:
            if not st.session_state.resume_text:
                st.error("❌ Please upload your resume first!")
            if not job_description:
                st.error("❌ Please enter a job description!")

# COMPANY RESEARCH PAGE
elif page == "🏢 Company Research":
    st.markdown('<div class="section-title">🏢 HireEdge Company Intel</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glow-effect">Get comprehensive research about your target company for strategic interview preparation.</div>', unsafe_allow_html=True)
    
    # Show previous results if available - ALWAYS at top
    if st.session_state.company_research:
        st.markdown("### 📋 Previous Company Research")
        for comp_name, research in st.session_state.company_research.items():
            # Display each company research prominently
            st.markdown(f"#### 🏢 {comp_name}")
            
            # Show timestamp if available
            if 'timestamp' in research:
                st.caption(f"Researched on: {research['timestamp']}")
                
            # Show news count if available
            if research.get('recent_news'):
                st.caption(f"📰 {len(research['recent_news'])} recent news items included")
            
            # Display analysis in a container with extra HTML cleaning
            with st.container():
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown('<div class="analysis-text">', unsafe_allow_html=True)
                # Extra cleaning to remove any HTML tags that slipped through
                clean_analysis = research["analysis"].replace('<div class="analysis-container">', '').replace('<div class="section-title">', '').replace('</div>', '')
                import re
                clean_analysis = re.sub(r'<[^>]+>', '', clean_analysis)  # Remove any remaining HTML tags
                st.write(clean_analysis)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
        st.markdown("---")
    
    # Add debug storage information
    with st.expander("🗂️ Debug: Storage Information", expanded=False):
        st.markdown("**Current Session State:**")
        st.write(f"Total Company Research Records: {len(st.session_state.company_research)}")
        if st.session_state.company_research:
            st.write("Stored Companies:", list(st.session_state.company_research.keys()))
            for company, data in st.session_state.company_research.items():
                st.write(f"- {company}: {data.get('timestamp', 'No timestamp')} ({len(str(data.get('analysis', ''))):.0f} chars)")
    
    company_name = st.text_input(
        "Company Name:",
        value=st.session_state.company_name,
        placeholder="e.g., Google, Microsoft, Apple, Tesla..."
    )
    
    # Update session state if company name changes
    if company_name != st.session_state.company_name:
        st.session_state.company_name = company_name
    
    if company_name:
        
        if st.button("🔍 Research Company", type="primary"):
            with st.spinner(f"Researching {company_name}... (this may take 30-60 seconds)"):
                try:
                    # Use simplified direct company research
                    result = career_assistant.research_company(company_name, st.session_state.resume_text)
                    
                    if result.get("success"):
                        # Display results with clean formatting
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(f'### 🏢 Research Results: {company_name}')
                        
                        # Show research metrics first
                        if result.get("recent_news"):
                            st.info(f"📰 Found {len(result['recent_news'])} recent news items")
                        
                        # Display clean analysis text with extra cleaning
                        st.markdown('<div class="analysis-text">', unsafe_allow_html=True)
                        # Double-clean to ensure no HTML tags slip through
                        clean_analysis = result["analysis"].replace('<div class="analysis-container">', '').replace('<div class="section-title">', '').replace('</div>', '')
                        st.write(clean_analysis)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Store results in company_research with timestamp and clean data
                        import datetime
                        result['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Ensure the stored analysis is completely clean
                        result['analysis'] = result['analysis'].replace('<div class="analysis-container">', '').replace('<div class="section-title">', '').replace('</div>', '')
                        import re
                        result['analysis'] = re.sub(r'<[^>]+>', '', result['analysis'])
                        
                        st.session_state.company_research[company_name] = result
                        
                        st.success(f"\u2705 Company research for {company_name} saved successfully!")
                        st.balloons()
                        

                    else:
                        st.error(f"❌ Company research failed: {result.get('error', 'Unknown error')}")
                    
                except Exception as e:
                    st.error(f"❌ Research failed: {str(e)}")
                    st.markdown("**Troubleshooting:**")
                    st.markdown("- Check your internet connection")
                    st.markdown("- Try a different company name")
                    st.markdown("- The AI service might be busy, please try again")

# INTERVIEW PREP PAGE
elif page == "💼 Interview Prep":
    st.markdown('<div class="section-title">💼 HireEdge Interview Prep</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glow-effect">Generate customized interview questions and preparation material based on the job and company.</div>', unsafe_allow_html=True)
    
    # Show previous results if available
    if st.session_state.interview_prep:
        with st.expander("🎓 Previous Interview Preparations", expanded=False):
            for prep_key, prep in st.session_state.interview_prep.items():
                st.markdown(f"### {prep_key.replace('_', ' - ')[:100]}...")
                clean_prep = prep["analysis"].replace('<div>', '').replace('</div>', '').replace('<br>', '\n')
                st.write(clean_prep[:500] + "..." if len(clean_prep) > 500 else clean_prep)
                st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.job_description:
            st.success("✅ Job description loaded")
        else:
            st.warning("⚠️ Add job description in Job Matcher")
    
    with col2:
        if st.session_state.company_name:
            st.success(f"✅ Company: {st.session_state.company_name}")
        else:
            st.warning("⚠️ Add company in Company Research")
    
    # Add debug storage information
    with st.expander("🗂️ Debug: Storage Information", expanded=False):
        st.markdown("**Current Session State:**")
        st.write(f"Total Interview Prep Records: {len(st.session_state.interview_prep)}")
        if st.session_state.interview_prep:
            st.write("Stored Interview Preps:", list(st.session_state.interview_prep.keys()))
            for prep_key, data in st.session_state.interview_prep.items():
                st.write(f"- {prep_key}: {data.get('timestamp', 'No timestamp')} ({len(str(data.get('analysis', ''))):.0f} chars)")
    
    if st.button("🎯 Generate Interview Prep", type="primary"):
        if st.session_state.job_description or st.session_state.company_name:
            with st.spinner("Preparing your interview materials... (this may take 30-60 seconds)"):
                try:
                    # Use simplified direct interview preparation
                    result = career_assistant.prepare_interview(
                        st.session_state.job_description,
                        st.session_state.company_name,
                        st.session_state.resume_text
                    )
                    
                    if result.get("success"):
                        # Store results with timestamp
                        import datetime
                        result['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        prep_key = f"{st.session_state.company_name}_{st.session_state.job_description[:50] if st.session_state.job_description else 'general'}"
                        st.session_state.interview_prep[prep_key] = result
                        
                        # Display results with enhanced styling
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown('### 🎯 Interview Preparation Guide')
                        
                        # Show prep metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            if result.get("technical_questions"):
                                st.info(f"🔧 {len(result['technical_questions'])} Technical Questions")
                        with col2:
                            if result.get("behavioral_questions"):
                                st.info(f"👥 {len(result['behavioral_questions'])} Behavioral Questions")
                        
                        # Display analysis text with proper formatting
                        st.markdown('<div class="analysis-text">', unsafe_allow_html=True)
                        # Clean the analysis text to remove any HTML tags
                        clean_analysis = result["analysis"].replace('<div>', '').replace('</div>', '').replace('<br>', '\n')
                        st.write(clean_analysis)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.success(f"✅ Interview preparation for {st.session_state.company_name or 'position'} saved successfully!")
                        st.balloons()
                    else:
                        st.error(f"❌ Interview prep failed: {result.get('error', 'Unknown error')}")
                    
                except Exception as e:
                    st.error(f"❌ Preparation failed: {str(e)}")
        else:
            st.error("❌ Please provide job description and/or company name first.")

# DASHBOARD PAGE
elif page == "📊 Dashboard":
    st.markdown('<div class="section-title">📊 Career Progress Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glow-effect">Comprehensive overview of your career optimization progress and AI-generated insights.</div>', unsafe_allow_html=True)
    
    # Always show dashboard content
    # Show completion status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'resume' in st.session_state.analysis_results:
            st.markdown('<div class="status-complete">✅ Resume Analyzed</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-pending">⏳ Resume Analysis</div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.job_match_results:
            st.markdown('<div class="status-complete">✅ Job Matched</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-pending">⏳ Job Matching</div>', unsafe_allow_html=True)
    
    with col3:
        if st.session_state.company_research:
            st.markdown('<div class="status-complete">✅ Company Researched</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-pending">⏳ Company Research</div>', unsafe_allow_html=True)
    
    with col4:
        if st.session_state.interview_prep:
            st.markdown('<div class="status-complete">✅ Interview Prep</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-pending">⏳ Interview Prep</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show individual section results if available
    if st.session_state.analysis_results:
        st.markdown("### 📝 Resume Analysis Results")
        with st.expander("View Resume Analysis", expanded=True):
            for key, result in st.session_state.analysis_results.items():
                if key != 'comprehensive':
                    st.markdown(f"**{key.title()}:**")
                    st.write(result)
                    st.markdown("---")
    
    if st.session_state.job_match_results:
        st.markdown("### 🎯 Job Matching Results")
        with st.expander("View Job Matches", expanded=True):
            st.write(st.session_state.job_match_results)
    
    if st.session_state.company_research:
        st.markdown("### 🏢 Company Research Results")
        with st.expander("View Company Intel", expanded=True):
            st.write(st.session_state.company_research)
    
    if st.session_state.interview_prep:
        st.markdown("### 💼 Interview Preparation")
        with st.expander("View Interview Guide", expanded=True):
            st.write(st.session_state.interview_prep)
    
    # Show info message only if no results exist
    if not (st.session_state.analysis_results or st.session_state.job_match_results or st.session_state.company_research or st.session_state.interview_prep):
        st.info("Complete analysis in other sections to see your progress here.")
    
    st.markdown("---")
    
    # Add comprehensive analysis option
    st.markdown("### 🚀 Complete Career Analysis")
    st.info("Get a comprehensive end-to-end analysis combining all features!")
    
    if st.button("🎯 Run Complete Analysis", type="primary") and st.session_state.resume_text:
        with st.spinner("Running comprehensive career analysis... (this may take 1-2 minutes)"):
            try:
                # Use comprehensive analysis method
                result = career_assistant.comprehensive_career_analysis(
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    st.session_state.company_name
                )
                
                if result.get("success"):
                    # Store comprehensive results
                    st.session_state.analysis_results['comprehensive'] = result
                    st.session_state.analysis_results.update(result["results"])
                    
                    # Display results with enhanced styling
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown('### 🚀 Comprehensive Career Strategy')
                    
                    # Display analysis text with proper formatting
                    st.markdown('<div class="analysis-text">', unsafe_allow_html=True)
                    
                    # Show all analyses
                    for component, data in result["results"].items():
                        if data.get("success"):
                            st.markdown(f"## {component.replace('_', ' ').title()}")
                            # Clean the analysis text to remove any HTML tags
                            clean_analysis = data["analysis"].replace('<div>', '').replace('</div>', '').replace('<br>', '\n')
                            st.write(clean_analysis)
                            st.markdown("---")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.balloons()
                    st.success(f"✅ Complete! Analyzed {result['total_components']} components")
                else:
                    st.error(f"❌ Comprehensive analysis failed: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

# Footer
st.markdown(
    """
    <div class="footer-style">
        <h4 style="color: #00d4ff; margin-bottom: 1rem;">⚡ HireEdge AI</h4>
        <p style="margin: 0.5rem 0;">Powered by Advanced AI & Real-Time APIs</p>
        <p style="font-size: 0.8rem; color: #666;">Your AI-Powered Career Strategist - Get The Edge!</p>
    </div>
    """, 
    unsafe_allow_html=True
)