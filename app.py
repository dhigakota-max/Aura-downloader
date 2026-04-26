import streamlit as st
import yt_dlp
import os
import time

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🟣", layout="centered")

# --- Optimized CSS for Mobile & Desktop ---
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle, #1a012d 0%, #0e1117 100%);
    }

    /* Main Container Styling */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 20px;
    }

    /* Aura Title Neon Style */
    .aura-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 15px #9146ff, 0 0 30px #9146ff;
        margin-bottom: 5px;
        text-align: center;
        letter-spacing: 3px;
    }

    .subtitle {
        color: #b07cff;
        font-size: 0.9rem;
        margin-bottom: 30px;
        text-align: center;
        opacity: 0.8;
    }

    /* Neon Card for Input */
    .input-card {
        background: rgba(26, 1, 45, 0.6);
        border: 2px solid #9146ff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(145, 70, 255, 0.3);
        width: 100%;
        max-width: 400px;
    }

    /* Input Field */
    .stTextInput>div>div>input {
        background-color: #0c0015 !important;
        border: 1px solid #9146ff !important;
        color: white !important;
        border-radius: 10px;
        text-align: center;
    }

    /* Analyze Button */
    .stButton>button {
        background: linear-gradient(90deg, #9146ff, #6200ea);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        width: 100%;
        height: 3.5em;
        transition: 0.3s;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 15px #9146ff;
        transform: scale(1.02);
    }

    /* Quality Select Card */
    .quality-card {
        background: #1a012d;
        border: 1px solid #9146ff;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }

    /* Hide Streamlit elements for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session State
if 'stage' not in st.session_state:
    st.session_state.stage = 'home'

# --- UI Layout ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="aura-title">AURA</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">YOUTUBE • INSTAGRAM • TIKTOK</p>', unsafe_allow_html=True)

if st.session_state.stage == 'home':
    # Link Input Area
    with st.container():
        url = st.text_input("", placeholder="Paste your link here...", label_visibility="collapsed")
        if st.button("ANALYZE LINK"):
            if url:
                with st.spinner("Decoding cosmic link..."):
                    time.sleep(1.5) # Smooth feeling
                    st.session_state.url = url
                    st.session_state.stage = 'quality'
                    st.rerun()
            else:
                st.error("Please paste a link first!")

elif st.session_state.stage == 'quality':
    # Quality Selection Area (The "Smooth" transition feel)
    st.markdown('<div class="quality-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>Select Quality</h3>", unsafe_allow_html=True)
    
    option = st.selectbox("Choose Format:", ["High Quality Video (MP4)", "Audio Only (MP3)"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("DOWNLOAD"):
            st.success("Download started! (Simulation)")
            # මෙතනට ඔයාගේ ඩවුන්ලෝඩ් logic එක දාන්න පුළුවන්
    with col2:
        if st.button("BACK"):
            st.session_state.stage = 'home'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><p style='text-align: center; color: #555; font-size: 0.8rem;'>Developed for Cosmic Travelers</p>", unsafe_allow_html=True)
