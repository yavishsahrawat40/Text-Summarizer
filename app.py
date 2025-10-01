import streamlit as st
import time
from summarizer_cli import load_config, query_api

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Custom CSS ---
def load_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found. Using default styling.")
    except Exception as e:
        st.warning(f"Error loading CSS: {e}")

load_css('styles.css')

# --- Enhanced Header ---
st.markdown("""
<div class="header-container">
    <div class="header-title">📝 AI-Powered Text Summarizer</div>
    <div class="header-subtitle">Transform lengthy articles into concise, meaningful summaries using advanced AI</div>
</div>
""", unsafe_allow_html=True)

# --- Configuration Loading ---
try:
    config = load_config()
    if "api_url" not in config or "api_token" not in config:
        st.error("⚠️ Configuration Error: Please check your .env file and ensure HF_API_KEY is set correctly.")
        st.stop()
except SystemExit:
    st.error("⚠️ Configuration Error: Could not load configuration. Please ensure your HF_API_KEY is set in the .env file.")
    st.stop()

# --- Enhanced Input Section ---
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# Sample texts for placeholder rotation
sample_texts = [
    "Paste your article, research paper, or long document here...",
    "Try summarizing news articles, blog posts, or academic papers...",
    "Enter any lengthy text you'd like to condense into key points...",
    "Copy and paste content from websites, PDFs, or documents..."
]

# Initialize session state for placeholder rotation
if 'placeholder_index' not in st.session_state:
    st.session_state.placeholder_index = 0

# Rotate placeholder text every few seconds (simulated)
current_placeholder = sample_texts[st.session_state.placeholder_index % len(sample_texts)]

input_col1, input_col2 = st.columns([3, 1])

with input_col1:
    st.markdown("### 📄 Input Text")
    
with input_col2:
    if st.button("🔄 Clear", help="Clear the input text"):
        st.session_state.text_input = ""
        st.rerun()

input_text = st.text_area(
    "Enter your text:",
    height=200,
    placeholder=current_placeholder,
    key="text_input",
    label_visibility="collapsed"
)

# Enhanced character counter with visual feedback
char_count = len(input_text)
if char_count == 0:
    counter_class = "normal"
    counter_text = "Start typing to see character count"
elif char_count < 3000:
    counter_class = "normal"
    counter_text = f"✅ {char_count:,} characters - Perfect length"
elif char_count < 4000:
    counter_class = "warning"
    counter_text = f"⚠️ {char_count:,} characters - Getting long, but still good"
else:
    counter_class = "danger"
    counter_text = f"🔴 {char_count:,} characters - Very long! Will be truncated to ~5000 chars"

st.markdown(f'<div class="char-counter {counter_class}">{counter_text}</div>', unsafe_allow_html=True)

# Tips section
if char_count == 0:
    st.markdown("""
    <div class="tips-section">
        <strong>💡 Tips for best results:</strong>
        <ul>
            <li>Paste articles, research papers, or long documents</li>
            <li>Optimal length: 500-3000 characters</li>
            <li>The AI works best with well-structured text</li>
            <li>Multiple paragraphs are handled automatically</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Summarization Logic ---
button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    generate_button = st.button("🚀 Generate Summary", type="primary", use_container_width=True)

if generate_button:
    if not input_text.strip():
        st.warning("📝 Please enter some text to summarize first!")
    else:
        # Enhanced loading state with progress and tips
        loading_container = st.empty()
        
        with loading_container.container():
            st.markdown("""
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <h3>🤖 AI is analyzing your text...</h3>
                <p>This usually takes 10-30 seconds depending on text length</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress with helpful tips
            tips = [
                "🔍 Analyzing text structure...",
                "🧠 Identifying key concepts...",
                "📊 Processing with AI model...",
                "✨ Generating concise summary..."
            ]
            
            for i, tip in enumerate(tips):
                status_text.text(tip)
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.5)  # Small delay for better UX
            
            # Make API call
            result = query_api(input_text, config["api_url"], config["api_token"])
            
            # Clear loading state
            loading_container.empty()
        
        # Handle results
        if result["error"]:
            st.error(f"❌ **Something went wrong:** {result['error']}")
            st.markdown("""
            <div class="tips-section">
                <strong>🔧 Troubleshooting tips:</strong>
                <ul>
                    <li>Check your internet connection</li>
                    <li>Try with shorter text (under 4000 characters)</li>
                    <li>Wait a moment and try again</li>
                    <li>Ensure your text contains meaningful content</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Success! Display results beautifully
            st.markdown('<div class="results-section">', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="success-header">
                <span>🎉</span>
                <span>Summary Generated Successfully!</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Create two columns for before/after comparison
            result_col1, result_col2 = st.columns([1, 1])
            
            with result_col1:
                st.markdown("### 📄 Original Text Preview")
                preview_text = input_text[:300] + "..." if len(input_text) > 300 else input_text
                st.text_area("Original", value=preview_text, height=150, disabled=True, label_visibility="collapsed")
                st.caption(f"Original: {len(input_text):,} characters")
            
            with result_col2:
                st.markdown("### ✨ AI Summary")
                summary_text = result["summary"]
                st.text_area("Summary", value=summary_text, height=150, disabled=True, label_visibility="collapsed")
                st.caption(f"Summary: {len(summary_text):,} characters ({len(summary_text)/len(input_text)*100:.1f}% of original)")
            
            st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 Powered by Hugging Face AI • Built with Streamlit</p>
    <p><small>This tool uses the BART model for intelligent text summarization</small></p>
</div>
""", unsafe_allow_html=True)