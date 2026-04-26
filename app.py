import streamlit as st
import yt_dlp
import os
from datetime import date

# --- Page Configuration ---
st.set_page_config(page_title="Aura Downloader", page_icon="🔮")

if 'stage' not in st.session_state: st.session_state.stage = 'home'

# --- CSS Styling ---
st.markdown("""
    <style>
    .aura-title { font-size: 4rem; font-weight: 900; background: linear-gradient(to right, #00d2ff, #ff0080); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #00d2ff, #ff0080); color: white; width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="aura-title">AURA</h1>', unsafe_allow_html=True)

if st.session_state.stage == 'home':
    url = st.text_input("Paste your link here:", placeholder="https://...")
    if st.button("SEARCH LINK"):
        if url:
            with st.spinner("Fetching video details..."):
                try:
                    ydl_opts = {'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        st.session_state.video_info = info
                        st.session_state.url = url
                        st.session_state.stage = 'quality'
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif st.session_state.stage == 'quality':
    info = st.session_state.video_info
    st.image(info.get('thumbnail', ''), width=300)
    st.write(f"**Title:** {info.get('title')}")
    
    # MB ප්‍රමාණය ගණනය කිරීම
    filesize = info.get('filesize_approx') or info.get('filesize')
    if filesize:
        mb_size = filesize / (1024 * 1024)
        st.info(f"Estimated Size: {mb_size:.1f} MB")
    else:
        st.warning("Size: Unknown")

    quality = st.selectbox("Select Quality:", ["480p", "720p", "1080p", "4K", "MP3"])
    
    if st.button("START DOWNLOAD"):
        with st.spinner("Downloading... Please wait."):
            try:
                # Quality options mapping
                q_map = {"480p":"480", "720p":"720", "1080p":"1080", "4K":"2160"}
                
                if quality == "MP3":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'audio.mp3',
                        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
                    }
                    filename = "audio.mp3"
                else:
                    res = q_map[quality]
                    ydl_opts = {
                        'format': f'bestvideo[height<={res}]+bestaudio/best',
                        'outtmpl': 'video.mp4',
                        'merge_output_format': 'mp4'
                    }
                    filename = "video.mp4"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([st.session_state.url])
                
                # Device එකට සේව් කරන බටන් එක
                with open(filename, "rb") as f:
                    st.download_button("CLICK TO SAVE TO DEVICE", f, file_name=f"Aura_{quality}_{filename}")
                st.success("Download Successful!")
            except Exception as e:
                st.error("YouTube blocked this request. Try again or use a different link.")

    if st.button("← GO BACK"):
        st.session_state.stage = 'home'
        st.rerun()
        
