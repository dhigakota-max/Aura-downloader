import streamlit as st
import yt_dlp
import os
import time

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🔮", layout="centered")

# --- Liquid Glass & Neon CSS ---
st.markdown("""
    <style>
    /* Animated Liquid Background - Blue & Magenta vibes */
    .stApp {
        background: linear-gradient(45deg, #09090e, #1f0033, #001133, #09090e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Centered Container */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 50px;
    }

    /* Liquid Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(16px); 
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 210, 255, 0.15), 0 8px 32px 0 rgba(255, 0, 128, 0.15); 
        width: 100%;
        max-width: 450px;
        text-align: center;
    }

    /* AURA Title - Blue to Magenta Gradient Glow */
    .aura-title {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(to right, #00d2ff, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
        letter-spacing: 6px;
        margin-bottom: 0;
        text-align: center;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 40px;
        text-align: center;
    }

    /* Smooth Input Field */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 210, 255, 0.4) !important;
        color: white !important;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border: 1px solid rgba(255, 0, 128, 0.6) !important;
        box-shadow: 0 0 15px rgba(255, 0, 128, 0.3) !important;
    }

    /* Liquid Button - Blue to Magenta */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff, #ff0080);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        letter-spacing: 2px;
        width: 100%;
        height: 3.5em;
        box-shadow: 0 4px 15px rgba(255, 0, 128, 0.4);
        transition: 0.3s;
        margin-top: 10px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.6);
    }

    /* UI Clean-up */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session State
if 'stage' not in st.session_state:
    st.session_state.stage = 'home'

# --- UI Render ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="aura-title">AURA</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">YouTube • Instagram • TikTok</p>', unsafe_allow_html=True)

if st.session_state.stage == 'home':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("", placeholder="Paste your link here...", label_visibility="collapsed")
    if st.button("SEARCH LINK"):
        if url:
            with st.spinner("Analyzing the link..."):
                time.sleep(1.5)
                st.session_state.url = url
                st.session_state.stage = 'quality'
                st.rerun()
        else:
            st.error("Please provide a link.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.stage == 'quality':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Select Quality</h3>", unsafe_allow_html=True)
    
    option = st.selectbox("", ["High Quality Video (MP4)", "Audio Only (MP3)"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("START DOWNLOAD"):
        st.success("Download started! (Simulation)")
        
    if st.button("← GO BACK"):
        st.session_state.stage = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
