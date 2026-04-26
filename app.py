import streamlit as st
import yt_dlp
import os
import re
from datetime import date

# --- Page Configuration ---
st.set_page_config(
    page_title="Aula Downloader",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Session State Init ---
defaults = {
    'theme': 'Dark',
    'stage': 'home',
    'video_info': None,
    'url': '',
    'formats': {}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Helper Functions ---
def format_size(bytes_val):
    if not bytes_val:
        return "~Unknown"
    mb = bytes_val / (1024 * 1024)
    if mb >= 1000:
        return f"~{mb/1024:.1f} GB"
    return f"~{mb:.1f} MB"

def detect_platform(url):
    if not url:
        return "unknown"
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    return "other"

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def get_format_sizes(info, platform):
    """Extract available format sizes from video info."""
    formats = {}
    available_formats = info.get('formats', [])

    # Get audio size
    audio_size = None
    for f in available_formats:
        if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
            if f.get('filesize') or f.get('filesize_approx'):
                audio_size = f.get('filesize') or f.get('filesize_approx')
                break

    if platform == "youtube":
        quality_map = {
            "MP3 Audio": ("bestaudio/best", audio_size),
            "480p Video": ("bestvideo[height<=480]+bestaudio/best[height<=480]/best[height<=480]", None),
            "720p Video": ("bestvideo[height<=720]+bestaudio/best[height<=720]/best[height<=720]", None),
            "1080p Video": ("bestvideo[height<=1080]+bestaudio/best[height<=1080]/best[height<=1080]", None),
        }
        for label, (fmt, size) in quality_map.items():
            # Try to find matching format size
            if size is None and label != "MP3 Audio":
                height = int(re.search(r'(\d+)p', label).group(1)) if re.search(r'(\d+)p', label) else None
                for f in available_formats:
                    fh = f.get('height', 0) or 0
                    if height and fh <= height and fh > 0 and f.get('vcodec') != 'none':
                        sz = f.get('filesize') or f.get('filesize_approx')
                        if sz:
                            size = sz
                            break
            formats[label] = {'format': fmt, 'size': size, 'is_audio': label == "MP3 Audio"}

    elif platform == "instagram":
        quality_map = {
            "Best Quality": ("bestvideo+bestaudio/best", None),
            "Medium Quality": ("bestvideo[height<=720]+bestaudio/best[height<=720]", None),
            "Low Quality": ("bestvideo[height<=480]+bestaudio/best[height<=480]", None),
        }
        for label, (fmt, size) in quality_map.items():
            for f in available_formats:
                sz = f.get('filesize') or f.get('filesize_approx')
                if sz and not size:
                    size = sz
            formats[label] = {'format': fmt, 'size': size, 'is_audio': False}

    elif platform == "tiktok":
        formats["No Watermark HD"] = {
            'format': 'bestvideo+bestaudio/best',
            'size': None,
            'is_audio': False
        }
        formats["No Watermark SD"] = {
            'format': 'worst',
            'size': None,
            'is_audio': False
        }
        # Try to get size
        for f in available_formats:
            sz = f.get('filesize') or f.get('filesize_approx')
            if sz:
                formats["No Watermark HD"]['size'] = sz
                break
    else:
        formats["Best Quality"] = {'format': 'bestvideo+bestaudio/best', 'size': None, 'is_audio': False}
        formats["Audio Only"] = {'format': 'bestaudio/best', 'size': None, 'is_audio': True}

    return formats

def download_video(url, fmt, is_audio, output_name="aula_download"):
    """Download video/audio and return file path."""
    ext = "mp3" if is_audio else "mp4"
    out_template = f"/tmp/{output_name}.%(ext)s"

    ydl_opts = {
        'format': fmt,
        'outtmpl': out_template,
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4' if not is_audio else None,
    }

    if is_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    # TikTok-specific: try to get no-watermark version
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.tiktok.com/',
    }
    if 'tiktok' in url.lower():
        ydl_opts['http_headers'] = headers

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Find the downloaded file
    for f in os.listdir('/tmp'):
        if f.startswith(output_name):
            return f"/tmp/{f}"
    return None

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    theme = st.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, horizontal=True)
    st.session_state.theme = theme
    st.markdown("---")
    st.markdown("## ℹ️ About")
    st.markdown(f"""
| | |
|---|---|
| **App** | Aula Downloader |
| **Made by** | Udula Thalisha |
| **Version** | 1.0 |
| **Date** | April 26, 2026 |
| **WhatsApp** | 0757856311 |
""")
    st.markdown("---")
    st.markdown("### 📱 Supported Platforms")
    st.markdown("✅ YouTube  \n✅ Instagram Reels  \n✅ TikTok")

# ============================================================
# DYNAMIC CSS
# ============================================================
is_dark = st.session_state.theme == "Dark"

bg_main = "linear-gradient(135deg, #0a0a12 0%, #12002a 50%, #0a0a12 100%)" if is_dark else "linear-gradient(135deg, #f8f4ff 0%, #ede8ff 50%, #f8f4ff 100%)"
text_color = "#f0f0ff" if is_dark else "#1a0040"
subtext_color = "#a090c0" if is_dark else "#6040a0"
card_bg = "rgba(255,255,255,0.04)" if is_dark else "rgba(255,255,255,0.85)"
card_border = "rgba(150,100,255,0.25)" if is_dark else "rgba(120,60,220,0.2)"
input_bg = "rgba(255,255,255,0.07)" if is_dark else "rgba(255,255,255,0.9)"
input_border = "rgba(150,100,255,0.4)" if is_dark else "rgba(120,60,220,0.4)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Global Reset */
.stApp {{
    background: {bg_main};
    color: {text_color};
    font-family: 'DM Sans', sans-serif;
}}

/* Hide Streamlit branding */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; padding-bottom: 2rem; max-width: 680px; }}

/* Title */
.aula-hero {{
    text-align: center;
    padding: 2rem 0 1.5rem;
}}
.aula-title {{
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #f472b6, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1.1;
}}
.aula-sub {{
    font-family: 'DM Sans', sans-serif;
    color: {subtext_color};
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}}

/* Cards */
.glass-card {{
    background: {card_bg};
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 2rem;
    border: 1px solid {card_border};
    box-shadow: 0 8px 40px rgba(100,60,200,0.15);
    margin-bottom: 1rem;
}}

/* Platform badges */
.platform-badge {{
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 0 4px;
}}
.yt-badge {{ background: rgba(255,0,0,0.15); color: #ff6b6b; border: 1px solid rgba(255,0,0,0.25); }}
.ig-badge {{ background: rgba(225,48,108,0.15); color: #f472b6; border: 1px solid rgba(225,48,108,0.25); }}
.tt-badge {{ background: rgba(0,200,200,0.15); color: #67e8f9; border: 1px solid rgba(0,200,200,0.25); }}

/* Input styling */
.stTextInput > div > div > input {{
    background: {input_bg} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 14px !important;
    color: {text_color} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
}}

/* Buttons */
.stButton > button {{
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 25px rgba(124,58,237,0.5) !important;
}}

/* Download button (special) */
.stDownloadButton > button {{
    background: linear-gradient(135deg, #059669, #0891b2) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(5,150,105,0.35) !important;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background: {input_bg} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 14px !important;
    color: {text_color} !important;
}}

/* Progress bar */
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, #7c3aed, #db2777) !important;
    border-radius: 10px !important;
}}

/* Success/Error/Info */
.stSuccess, .stError, .stInfo, .stWarning {{
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
}}

/* Video info */
.video-title {{
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: {text_color};
    margin: 0.8rem 0 0.4rem;
    line-height: 1.3;
}}
.video-meta {{
    color: {subtext_color};
    font-size: 0.85rem;
    margin-bottom: 1rem;
}}
.size-tag {{
    font-size: 0.78rem;
    color: {subtext_color};
    font-style: italic;
}}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {{
    background: {'rgba(10,5,25,0.95)' if is_dark else 'rgba(245,240,255,0.95)'} !important;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="aula-hero">
    <h1 class="aula-title">AULA</h1>
    <p class="aula-sub">Universal Media Downloader</p>
    <div style="margin-top: 0.8rem;">
        <span class="platform-badge yt-badge">▶ YouTube</span>
        <span class="platform-badge ig-badge">◈ Instagram</span>
        <span class="platform-badge tt-badge">♪ TikTok</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# STAGE: HOME
# ============================================================
if st.session_state.stage == 'home':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Paste Your Link")

    url = st.text_input(
        "Video URL",
        placeholder="https://youtube.com/watch?v=... or instagram.com/reel/...",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        search_btn = st.button("🔍 FETCH VIDEO INFO", use_container_width=True)
    with col2:
        if url:
            platform = detect_platform(url)
            icons = {"youtube": "▶️ YT", "instagram": "📸 IG", "tiktok": "🎵 TT", "other": "🌐 Web"}
            st.markdown(f"<div style='text-align:center;padding-top:0.6rem;font-size:0.85rem;color:{subtext_color};'>{icons.get(platform,'🌐')}</div>", unsafe_allow_html=True)

    if search_btn:
        if not url or not url.strip():
            st.error("⚠️ Please paste a valid URL first.")
        else:
            url = url.strip()
            platform = detect_platform(url)
            progress = st.progress(0, text="Connecting to platform...")
            try:
                progress.progress(30, text="Fetching video metadata...")
                info = get_video_info(url)
                progress.progress(70, text="Analyzing available formats...")
                formats = get_format_sizes(info, platform)
                progress.progress(100, text="Done!")
                st.session_state.video_info = info
                st.session_state.url = url
                st.session_state.formats = formats
                st.session_state.platform = platform
                st.session_state.stage = 'quality'
                import time; time.sleep(0.3)
                st.rerun()
            except Exception as e:
                progress.empty()
                err_msg = str(e)
                if "Private" in err_msg or "private" in err_msg:
                    st.error("🔒 This video is private. Please use a public link.")
                elif "Sign in" in err_msg or "login" in err_msg.lower():
                    st.error("🔑 This content requires login. Only public content is supported.")
                elif "not available" in err_msg.lower():
                    st.error("❌ Video not available in your region or has been removed.")
                else:
                    st.error(f"❌ Could not fetch video info. Please check the link and try again.\n\nHint: Make sure the video is public and the URL is complete.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Tips card
    st.markdown(f"""
    <div class="glass-card" style="padding:1.2rem 2rem;">
        <p style="color:{subtext_color};font-size:0.85rem;margin:0;line-height:1.8;">
        💡 <strong>Tips:</strong><br>
        • YouTube: Use full URLs (youtube.com/watch?v=...) or short links (youtu.be/...)<br>
        • Instagram: Make sure the Reel/post is public<br>
        • TikTok: Copy the share link from the app for best results
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# STAGE: QUALITY SELECTION
# ============================================================
elif st.session_state.stage == 'quality':
    info = st.session_state.video_info
    formats = st.session_state.formats
    platform = st.session_state.get('platform', 'other')
    platform_labels = {"youtube": "▶ YouTube", "instagram": "◈ Instagram", "tiktok": "♪ TikTok", "other": "🌐 Web"}

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # Thumbnail + info
    thumb = info.get('thumbnail')
    title = info.get('title', 'Video')
    duration = info.get('duration')
    uploader = info.get('uploader') or info.get('channel') or ""

    if thumb:
        st.image(thumb, use_container_width=True)

    platform_icon = {"youtube": "🔴", "instagram": "💜", "tiktok": "🖤", "other": "🌐"}
    st.markdown(f"""
    <div class="video-title">{title[:80]}{'...' if len(title)>80 else ''}</div>
    <div class="video-meta">
        {platform_icon.get(platform,'🌐')} {platform_labels.get(platform,'Web')}
        {'&nbsp;&nbsp;•&nbsp;&nbsp;⏱ ' + str(int(duration//60)) + 'm ' + str(int(duration%60)) + 's' if duration else ''}
        {'&nbsp;&nbsp;•&nbsp;&nbsp;' + uploader if uploader else ''}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📥 Select Download Quality")

    # Build selectbox options with size info
    format_labels = []
    for label, fdata in formats.items():
        size_str = format_size(fdata['size'])
        format_labels.append(f"{label}  ({size_str})")

    selected_idx = st.selectbox(
        "Quality",
        range(len(format_labels)),
        format_func=lambda i: format_labels[i],
        label_visibility="collapsed"
    )

    selected_label = list(formats.keys())[selected_idx]
    selected_format = formats[selected_label]

    # Show format info
    is_audio = selected_format.get('is_audio', False)
    file_type = "MP3 Audio" if is_audio else "MP4 Video"
    st.markdown(f"<div class='size-tag'>📦 Format: {file_type} &nbsp;|&nbsp; Estimated size: {format_size(selected_format['size'])}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Download button
    dl_btn = st.button("⬇️ DOWNLOAD NOW", use_container_width=True)

    if dl_btn:
        progress = st.progress(0, text="Starting download...")
        try:
            progress.progress(20, text="Connecting to server...")
            import time
            time.sleep(0.5)
            progress.progress(50, text="Downloading... (this may take a moment)")

            file_path = download_video(
                st.session_state.url,
                selected_format['format'],
                is_audio,
                output_name="aula_output"
            )
            progress.progress(90, text="Preparing file...")
            time.sleep(0.3)

            if file_path and os.path.exists(file_path):
                progress.progress(100, text="✅ Ready!")
                ext = "mp3" if is_audio else "mp4"
                safe_title = re.sub(r'[^\w\s-]', '', title[:40]).strip().replace(' ', '_')
                download_name = f"Aula_{safe_title}_{selected_label.replace(' ','_')}.{ext}"

                with open(file_path, "rb") as f:
                    file_bytes = f.read()

                st.success("✅ Download ready! Click below to save to your device.")
                st.download_button(
                    label=f"💾 SAVE TO DEVICE  ({format_size(len(file_bytes))})",
                    data=file_bytes,
                    file_name=download_name,
                    mime="audio/mpeg" if is_audio else "video/mp4",
                    use_container_width=True
                )
                # Cleanup temp file
                try:
                    os.remove(file_path)
                except:
                    pass
            else:
                progress.empty()
                st.error("❌ Download failed. The file could not be found after download.")

        except Exception as e:
            progress.empty()
            err = str(e)
            if "ffmpeg" in err.lower():
                st.error("⚠️ FFmpeg is required for this format. Please install ffmpeg on your server.")
            elif "403" in err or "forbidden" in err.lower():
                st.error("🔒 Access denied by platform. Try a different quality or check if the link is still valid.")
            elif "unavailable" in err.lower() or "removed" in err.lower():
                st.error("❌ This video is no longer available.")
            else:
                st.warning(f"⚠️ Download encountered an error. Try a different quality option.\n\nDetails: {err[:200]}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Back butto
