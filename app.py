import streamlit as st
import yt_dlp
import os
import time

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🟣", layout="centered")

# --- Custom CSS for Vortex-like Neon Style ---
st.markdown("""
    <style>
    /* Main Background with subtle image */
    .stApp {
        background: radial-gradient(circle, #20023a 0%, #0e1117 100%);
    }
    
    /* Center the main container and apply card style */
    .stMainBlock {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    
    .stForm {
        background-color: #1a012d; /* Darker Purple Card */
        border: 2px solid #9146ff; /* Neon Purple Border */
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 15px rgba(145, 70, 255, 0.4);
        width: 100%;
        max-width: 450px;
        text-align: center;
    }

    /* Vortex Title Style */
    .title-text {
        font-family: 'Montserrat', sans-serif; /* You can change fonts */
        font-weight: 700;
        font-size: 2.8rem;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 25px;
        text-shadow: 0 0 10px rgba(145, 70, 255, 0.7);
    }
    
    /* Subtitle (Supported Platforms) */
    .subtitle-text {
        color: #aaaaaa;
        font-size: 0.9rem;
        margin-top: -15px;
        margin-bottom: 20px;
    }

    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: #0c0015 !important;
        border-radius: 10px;
        border: 1px solid #9146ff !important;
        color: #ffffff !important;
        height: 2.8em;
        text-align: center;
    }
    .stTextInput>div>div>input:focus {
        box-shadow: 0 0 8px rgba(145, 70, 255, 0.6) !important;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.2em;
        background-color: #9146ff; /* Primary Neon Purple */
        color: white;
        font-weight: bold;
        font-size: 1rem;
        text-transform: uppercase;
        border: none;
        transition: all 0.3s ease;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        background-color: #b07cff; /* Lighter Purple on hover */
        box-shadow: 0 0 12px rgba(145, 70, 255, 0.8);
    }

    /* Download Options Card */
    .options-card {
        background-color: #1a012d;
        border: 1px solid #9146ff;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 0 10px rgba(145, 70, 255, 0.3);
    }

    /* CSS for custom status messages */
    .stWarning, .stError, .stSuccess {
        border-radius: 10px !important;
        background-color: #0c0015 !important;
        border: 1px solid #9146ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'process_stage' not in st.session_state:
    st.session_state['process_stage'] = 'idle'
if 'video_info' not in st.session_state:
    st.session_state['video_info'] = None
if 'download_link' not in st.session_state:
    st.session_state['download_link'] = None

# --- Main UI Area ---
st.markdown('<h1 class="title-text">AURA</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">YouTube | Instagram | TikTok</p>', unsafe_allow_html=True)
st.markdown("---")

# Main Container
with st.container():
    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        if st.session_state['process_stage'] == 'idle':
            # 1. First Stage: Paste Link
            st.markdown('<div class="stMainBlock">', unsafe_allow_html=True)
            with st.form(key='link_form'):
                url = st.text_input("Paste Link Here...", placeholder="https://...")
                analyze_button = st.form_submit_button("ANALYZE LINK")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if analyze_button and url:
                st.session_state['process_stage'] = 'analyzing'
                st.experimental_rerun() # Refresh to show next stage

        elif st.session_state['process_stage'] == 'analyzing':
            # 2. Second Stage: Analysing (Simulated smooth transition)
            with st.spinner("Decoding Cosmic Codes... Please Wait."):
                time.sleep(2) # Fake processing time for smooth feel
                
                # ... (This part will actually get real info in the next version, for now it's simulated)
                st.session_state['process_stage'] = 'selecting'
                st.experimental_rerun() # Refresh to show options
                
        elif st.session_state['process_stage'] == 'selecting':
            # 3. Third Stage: Choose Quality/Type
            st.markdown('<div class="stMainBlock">', unsafe_allow_html=True)
            st.markdown('<div class="options-card">', unsafe_allow_html=True)
            st.markdown('### Download Options')
            st.markdown("Choose your preferred download type for: **'Downloaded Video'**")
            
            format_choice = st.radio("Select Format:", ["Best Video (MP4)", "Audio Only (MP3)"])
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                confirm_download = st.button("CONFIRM DOWNLOAD")
            with col_d2:
                cancel_button = st.button("CANCEL")
            st.markdown('</div></div>', unsafe_allow_html=True)

            if cancel_button:
                st.session_state['process_stage'] = 'idle'
                st.experimental_rerun()
            
            if confirm_download:
                st.session_state['process_stage'] = 'downloading'
                st.experimental_rerun()

        elif st.session_state['process_stage'] == 'downloading':
            # 4. Final Stage: Downloading (We just call the logic)
            with st.spinner("Downloading your media..."):
                time.sleep(2) # Fake time
                st.success("Successfully processed!")
                # For now, it doesn't download anything real, but the structure is there.
                
                # Cleanup and reset
                st.session_state['process_stage'] = 'idle'
                st.button("Back to Home") # Let user go back

# --- Footer (Optional) ---
st.markdown("---")
st.caption("Developed with ❤️ for Cosmic Travelers")
