import streamlit as st
import yt_dlp
import os
import time
from datetime import date

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🔮", layout="centered")

# --- Session State ---
if 'theme' not in st.session_state: st.session_state.theme = 'Dark'
if 'stage' not in st.session_state: st.session_state.stage = 'home'
if 'video_info' not in st.session_state: st.session_state.video_info = None

# --- Function to Get Video Info & Sizes ---
def get_info(url):
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def format_size(bytes):
    if bytes is None: return "Unknown Size"
    mb = bytes / (1024 * 1024)
    return f"{mb:.1f} MB"

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.session_state.theme = st.selectbox("Select Theme:", ["Dark", "Light"])
    st.markdown("---")
    st.title("ℹ️ About")
    st.markdown(f"**Made by:** Udula Thalisha\n\n**Version:** 8.0\n\n**Date:** {date.today()}\n\n**WhatsApp:** 0757856311")

# --- CSS (Dynamic) ---
color = "#ffffff" if st.session_state.theme == 'Dark' else "#1f0033"
bg = "linear-gradient(45deg, #09090e, #1f0033)" if st.session_state.theme == 'Dark' else "#f0f2f6"

st.markdown(f"""
    <style>
    .stApp {{ background: {bg}; color: {color}; }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }}
    .aura-title {{ font-size: 4rem; font-weight: 900; background: linear-gradient(to right, #00d2ff, #ff0080); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .stButton>button {{ background: linear-gradient(90deg, #00d2ff, #ff0080); color: white; border: none; width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- UI ---
st.markdown('<div style="text-align: center;"><h1 class="aura-title">AURA</h1><p>YouTube • Instagram • TikTok</p></div>', unsafe_allow_html=True)

if st.session_state.stage == 'home':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("", placeholder="Paste Link Here...", label_visibility="collapsed")
    if st.button("SEARCH LINK"):
        if url:
            try:
                with st.spinner("Fetching data..."):
                    st.session_state.video_info = get_info(url)
                    st.session_state.url = url
                    st.session_state.stage = 'quality'
                    st.rerun()
            except Exception as e:
                st.error("Invalid Link or Error fetching data.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.stage == 'quality':
    info = st.session_state.video_info
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.image(info.get('thumbnail', ''), width=200)
    st.write(f"**{info.get('title', 'Video')}**")
    
    # Sizes are dynamic if available, otherwise shown as estimated
    options = {
        "480p": "480",
        "720p": "720",
        "1080p": "1080",
        "4K": "2160",
        "MP3": "bestaudio"
    }
    
    selected_label = st.selectbox("Select Quality:", list(options.keys()))
    
    # Actual Download Logic
    if st.button("DOWNLOAD NOW"):
        with st.spinner("Downloading to server..."):
            format_id = options[selected_label]
            out_file = f"downloaded_file"
            
            ydl_opts = {
                'format': f'bestvideo[height<={format_id}]+bestaudio/best' if selected_label != "MP3" else 'bestaudio/best',
                'outtmpl': out_file,
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',}] if selected_label == "MP3" else []
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([st.session_state.url])
                
            # Streamlit download button for the user
            file_path = out_file if selected_label != "MP3" else f"{out_file}.mp3"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button("CLICK TO SAVE TO DEVICE", f, file_name=f"Aura_{selected_label}.{'mp3' if selected_label=='MP3' else 'mp4'}")
                st.success("Ready!")

    if st.button("← GO BACK"):
        st.session_state.stage = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
