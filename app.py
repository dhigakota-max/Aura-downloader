import streamlit as st
import yt_dlp
import os
import time

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🟣", layout="centered")

# --- Liquid Glass Effect CSS ---
st.markdown("""
    <style>
    /* Animated Liquid Background */
    .stApp {
        background: linear-gradient(45deg, #0e1117, #1a012d, #0e1117);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Container */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 50px;
    }

    /* Liquid Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05); /* Very light white */
        backdrop-filter: blur(15px); /* Liquid blur effect */
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); /* Soft border */
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(145, 70, 255, 0.3); /* Glow */
        width: 100%;
        max-width: 450px;
        text-align: center;
    }

    .aura-title {
        font-size: 4rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(145, 70, 255, 0.8);
        letter-spacing: 5px;
        margin-bottom: 0;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }

    /* Smooth Input Field */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(145, 70, 255, 0.5) !important;
        color: white !important;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }

    /* Liquid Button */
    .stButton>button {
        background: linear-gradient(90deg, #9146ff, #6200ea);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        letter-spacing: 1px;
        width: 100%;
        height: 3.5em;
        box-shadow: 0 4px 15px rgba(145, 70, 255, 0.4);
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(145, 70, 255, 0.6);
    }

    /* UI Clean-up */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session State for Stages
if 'stage' not in st.session_state:
    st.session_state.stage = 'home'

# --- UI Render ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="aura-title">AURA</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Gen Media Downloader</p>', unsafe_allow_html=True)

if st.session_state.stage == 'home':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("", placeholder="Paste your cosmic link...", label_visibility="collapsed")
    if st.button("ANALYZE LINK"):
        if url:
            with st.spinner("Processing through the nebula..."):
                time.sleep(1.5)
                st.session_state.url = url
                st.session_state.stage = 'quality'
                st.rerun()
        else:
            st.error("Please provide a link.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.stage == 'quality':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color: white; font-size: 1.5rem;'>Choose Quality</h2>", unsafe_allow_html=True)
    
    # Simulating quality selection
    option = st.selectbox("", ["4K Ultra HD", "1080p Full HD", "720p HD", "MP3 Audio"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("START DOWNLOAD"):
        st.success("The download has been initialized!")
        
    if st.button("← GO BACK"):
        st.session_state.stage = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
