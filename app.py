import streamlit as st
import yt_dlp
import os

# App Configuration
st.set_page_config(page_title="Aula Downloader", page_icon="📥")

# Sidebar - About Section
st.sidebar.title("Aula Downloader")
st.sidebar.markdown(f"""
**Made by:** Udula Thalisha  
**Date:** April 26, 2026  
**Version:** 1.0  
**WhatsApp:** [0757856311](https://wa.me/94757856311)
""")

# Main UI
st.title("📥 Aula Downloader")
st.write("YouTube, Instagram, and TikTok Downloader")

url = st.text_input("Paste your video link here:", placeholder="https://...")

if url:
    try:
        with st.spinner("Fetching video information..."):
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Video')
                thumbnail = info.get('thumbnail')
                
                st.image(thumbnail, width=300)
                st.subheader(title)

                # Format selection
                formats = info.get('formats', [])
                # Mehiදී formats filter karala display karanna puluwan
                
                if st.button("Download Now"):
                    # Download logic with progress bar
                    st.success("Download started!")
                    # yt-dlp download process...

    except Exception as e:
        st.error(f"Error: {e}")
        