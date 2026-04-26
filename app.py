import streamlit as st
import yt_dlp
import os
import time
from datetime import date

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🔮", layout="centered")

# --- Session State for Theme and Stage ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'
if 'stage' not in st.session_state:
    st.session_state.stage = 'home'

# --- Sidebar: Settings & About ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Theme Toggle
    st.session_state.theme = st.selectbox("Select Theme:", ["Dark", "Light"])
    
    st.markdown("---")
    st.title("ℹ️ About")
    st.markdown(f"""
    **Made by:** Udula Thalisha  
    **Version:** 8.0  
    **Date:** {date.today().strftime('%Y-%m-%d')}  
    **WhatsApp:** [0757856311](https://wa.me/94757856311)
    """)

# --- Dynamic CSS based on Theme ---
if st.session_state.theme == 'Dark':
    bg_gradient = "linear-gradient(45deg, #09090e, #1f0033, #001133, #09090e)"
    card_bg = "rgba(255, 255, 255, 0.03)"
    text_color = "#ffffff"
    border_color = "rgba(0, 210, 255, 0.4)"
else:
    bg_gradient = "linear-gradient(45deg, #f0f2f6, #e0e5ec, #ffffff)"
    card_bg = "rgba(255, 255, 255, 0.7)"
    text_color = "#1f0033"
    border_color = "rgba(145, 70, 255, 0.5)"

st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_gradient};
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }}
    
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .main-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 50px;
    }}

    .glass-card {{
        background: {card_bg}; 
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {border_color}; 
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 210, 255, 0.15); 
        width: 100%;
        max-width: 450px;
        text-align: center;
    }}

    .aura-title {{
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(to right, #00d2ff, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
        letter-spacing: 6px;
        margin-bottom: 0;
    }}

    .subtitle {{
        color: {text_color};
        opacity: 0.6;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 40px;
    }}

    .stTextInput>div>div>input {{
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid {border_color} !important;
        color: {text_color} !important;
        border-radius: 12px;
        text-align: center;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #ff0080);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        letter-spacing: 2px;
        width: 100%;
        height: 3.5em;
        transition: 0.3s;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- UI Render ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="aura-title">AURA</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">YouTube • Instagram • TikTok</p>', unsafe_allow_html=True)

if st.session_state.stage == 'home':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("", placeholder="Paste your link here...", label_visibility="collapsed")
    if st.button("SEARCH LINK"):
        if url:
            with st.spinner("Searching..."):
                time.sleep(1.5)
                st.session_state.url = url
                st.session_state.stage = 'quality'
                st.rerun()
        else:
            st.error("Please enter a link!")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.stage == 'quality':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {text_color};'>Select Quality</h3>", unsafe_allow_html=True)
    option = st.selectbox("", ["High Quality Video", "Audio Only (MP3)"], label_visibility="collapsed")
    if st.button("START DOWNLOAD"):
        st.success("Download started!")
    if st.button("← GO BACK"):
        st.session_state.stage = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
