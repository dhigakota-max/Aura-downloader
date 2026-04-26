import streamlit as st
import yt_dlp
import os
import re
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AURA Downloader",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================
for k, v in {
    'theme': 'Dark',
    'stage': 'home',
    'video_info': None,
    'url': '',
    'formats': {},
    'platform': 'other',
    'settings_open': False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# HELPERS
# ============================================================
def fmt_size(b):
    if not b: return "~Size N/A"
    mb = b / 1048576
    return f"~{mb/1024:.1f} GB" if mb >= 1000 else f"~{mb:.1f} MB"

def detect_platform(url):
    u = (url or "").lower()
    if "youtube.com" in u or "youtu.be" in u: return "youtube"
    if "instagram.com" in u: return "instagram"
    if "tiktok.com" in u: return "tiktok"
    return "other"

def get_ydl_base():
    return {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept-Language': 'en-us,en;q=0.5',
        },
    }

def get_video_info(url):
    opts = get_ydl_base()
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)

def get_format_sizes(info, platform):
    formats = {}
    avail = info.get('formats', [])

    audio_size = next(
        (f.get('filesize') or f.get('filesize_approx')
         for f in avail
         if f.get('vcodec') == 'none' and f.get('acodec') != 'none'
         and (f.get('filesize') or f.get('filesize_approx'))),
        None
    )

    def size_for_height(h):
        for f in avail:
            fh = f.get('height') or 0
            if fh <= h and fh > 0 and f.get('vcodec') != 'none':
                sz = f.get('filesize') or f.get('filesize_approx')
                if sz: return sz
        return None

    if platform == "youtube":
        entries = [
            ("🎵 MP3 Audio",    "bestaudio/best",                                           None, True),
            ("📱 480p Video",   "bestvideo[height<=480]+bestaudio/best[height<=480]/best",  480,  False),
            ("🎬 720p Video",   "bestvideo[height<=720]+bestaudio/best[height<=720]/best",  720,  False),
            ("🖥  1080p Video", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",1080, False),
        ]
        for label, fmt, h, is_a in entries:
            sz = audio_size if is_a else size_for_height(h)
            formats[label] = {'format': fmt, 'size': sz, 'is_audio': is_a}

    elif platform == "instagram":
        best_sz = next(
            (f.get('filesize') or f.get('filesize_approx') for f in avail
             if f.get('filesize') or f.get('filesize_approx')), None
        )
        for label, fmt in [
            ("🌟 Best Quality",  "bestvideo+bestaudio/best"),
            ("📱 Medium 720p",   "bestvideo[height<=720]+bestaudio/best"),
            ("🔻 Low 480p",      "bestvideo[height<=480]+bestaudio/best"),
        ]:
            formats[label] = {'format': fmt, 'size': best_sz, 'is_audio': False}

    elif platform == "tiktok":
        best_sz = next(
            (f.get('filesize') or f.get('filesize_approx') for f in avail
             if f.get('filesize') or f.get('filesize_approx')), None
        )
        formats["🎵 No Watermark HD"] = {'format': 'bestvideo+bestaudio/best', 'size': best_sz, 'is_audio': False}
        formats["📱 No Watermark SD"] = {'format': 'best[height<=480]',        'size': None,     'is_audio': False}

    else:
        formats["🌟 Best Quality"] = {'format': 'bestvideo+bestaudio/best', 'size': None, 'is_audio': False}
        formats["🎵 Audio Only"]   = {'format': 'bestaudio/best',           'size': None, 'is_audio': True}

    return formats

def download_video(url, fmt, is_audio, output_name="aura_dl"):
    for f in os.listdir('/tmp'):
        if f.startswith(output_name):
            try: os.remove(f"/tmp/{f}")
            except: pass

    opts = get_ydl_base()
    opts.update({
        'format': fmt,
        'outtmpl': f"/tmp/{output_name}.%(ext)s",
        'merge_output_format': 'mp4' if not is_audio else None,
        # Use android player client to bypass YouTube 403
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    })

    if is_audio:
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    if 'tiktok' in url.lower():
        opts['http_headers']['Referer'] = 'https://www.tiktok.com/'

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    for f in os.listdir('/tmp'):
        if f.startswith(output_name):
            return f"/tmp/{f}"
    return None

# ============================================================
# INLINE SETTINGS PANEL
# ============================================================
if st.session_state.settings_open:
    is_d2 = st.session_state.theme == "Dark"
    p_bg  = "rgba(16,4,36,0.97)"   if is_d2 else "rgba(238,232,255,0.97)"
    p_fg  = "#d8c8ff"               if is_d2 else "#1a0050"

    st.markdown(f"""
    <div style="background:{p_bg};border:1px solid rgba(140,90,255,0.3);
         border-radius:20px;padding:1.4rem 1.8rem;margin-bottom:0.8rem;
         box-shadow:0 8px 32px rgba(90,40,180,0.3);">
      <p style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;
         color:{p_fg};margin:0 0 0.8rem;">⚙️ Settings &amp; About</p>
    </div>
    """, unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        t_sel = st.radio("🎨 Theme", ["Dark", "Light"],
                          index=0 if st.session_state.theme == "Dark" else 1,
                          key="theme_radio")
        if t_sel != st.session_state.theme:
            st.session_state.theme = t_sel
            st.rerun()
    with cb:
        st.markdown(f"""
        <div style="font-size:0.83rem;line-height:2.1;color:{p_fg};">
        📱 <b>AURA Downloader</b><br>
        👤 Udula Thalisha<br>
        🔢 Version 1.0<br>
        📅 April 26, 2026<br>
        💬 0757856311
        </div>""", unsafe_allow_html=True)

    st.markdown("✅ YouTube &nbsp; ✅ Instagram &nbsp; ✅ TikTok")
    if st.button("✕  Close Settings", key="close_set"):
        st.session_state.settings_open = False
        st.rerun()
    st.markdown("---")

# ============================================================
# DYNAMIC CSS
# ============================================================
is_dark = st.session_state.theme == "Dark"

bg      = "linear-gradient(135deg,#060612 0%,#0e0025 55%,#060612 100%)" if is_dark else "linear-gradient(135deg,#f4f0ff 0%,#e8deff 55%,#f4f0ff 100%)"
fg      = "#f0eeff" if is_dark else "#180040"
sub     = "#9070c0" if is_dark else "#5030a0"
crd_bg  = "rgba(255,255,255,0.04)" if is_dark else "rgba(255,255,255,0.85)"
crd_bdr = "rgba(140,90,255,0.22)"  if is_dark else "rgba(110,50,210,0.18)"
inp_bg  = "rgba(255,255,255,0.06)" if is_dark else "rgba(255,255,255,0.9)"
inp_bdr = "rgba(140,90,255,0.38)"  if is_dark else "rgba(110,50,210,0.38)"
sb_bg   = "rgba(8,2,22,0.96)"      if is_dark else "rgba(242,237,255,0.96)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800;900&family=Inter:wght@300;400;500&display=swap');

.stApp {{ background:{bg}; color:{fg}; font-family:'Inter',sans-serif; }}
#MainMenu {{ visibility:visible !important; }}
footer {{ visibility:hidden; }}
header {{ visibility:visible !important; }}
.block-container {{ padding-top:0.5rem; padding-bottom:2rem; max-width:660px; }}

/* Sidebar arrow button — purple gradient */
[data-testid="collapsedControl"] {{
    background:linear-gradient(135deg,#7c3aed,#db2777) !important;
    border-radius:10px !important;
    color:white !important;
    opacity:1 !important;
    visibility:visible !important;
}}
[data-testid="collapsedControl"] svg {{
    fill:white !important;
    stroke:white !important;
}}

/* Hero */
.aura-wrap {{ text-align:center; padding:1rem 0 0.4rem; }}
.aura-name {{
    font-family:'Syne',sans-serif;
    font-size:4rem;
    font-weight:900;
    background:linear-gradient(135deg,#a78bfa 0%,#f472b6 50%,#60a5fa 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    letter-spacing:-2px;
    line-height:1;
    margin:0;
}}
.aura-sub {{
    color:{sub};
    font-size:0.75rem;
    letter-spacing:4px;
    text-transform:uppercase;
    margin:0.3rem 0 0.6rem;
    font-weight:500;
}}
.badge {{
    display:inline-block;
    padding:3px 12px;
    border-radius:30px;
    font-size:0.68rem;
    font-weight:700;
    letter-spacing:1.5px;
    text-transform:uppercase;
    margin:0 3px;
}}
.yt {{ background:rgba(255,50,50,0.12);  color:#ff7070; border:1px solid rgba(255,50,50,0.25); }}
.ig {{ background:rgba(220,50,110,0.12); color:#f472b6; border:1px solid rgba(220,50,110,0.25); }}
.tt {{ background:rgba(0,210,210,0.12);  color:#67e8f9; border:1px solid rgba(0,210,210,0.25); }}

/* Cards */
.card {{
    background:{crd_bg};
    backdrop-filter:blur(18px);
    border-radius:22px;
    padding:1.5rem 1.7rem;
    border:1px solid {crd_bdr};
    box-shadow:0 6px 32px rgba(100,50,200,0.12);
    margin-bottom:0.9rem;
}}

/* Text input */
.stTextInput > div > div > input {{
    background:{inp_bg} !important;
    border:1.5px solid {inp_bdr} !important;
    border-radius:13px !important;
    color:{fg} !important;
    font-family:'Inter',sans-serif !important;
    font-size:0.93rem !important;
    padding:0.72rem 1rem !important;
}}
.stTextInput > div > div > input:focus {{
    border-color:#a78bfa !important;
    box-shadow:0 0 0 3px rgba(167,139,250,0.18) !important;
}}

/* All buttons default */
.stButton > button {{
    background:linear-gradient(135deg,#7c3aed,#db2777) !important;
    color:white !important;
    border:none !important;
    border-radius:13px !important;
    font-family:'Syne',sans-serif !important;
    font-weight:700 !important;
    font-size:0.88rem !important;
    letter-spacing:1.2px !important;
    padding:0.65rem 1.5rem !important;
    width:100% !important;
    box-shadow:0 4px 18px rgba(124,58,237,0.28) !important;
    transition:transform .15s,box-shadow .15s !important;
}}
.stButton > button:hover {{
    transform:translateY(-2px) !important;
    box-shadow:0 7px 24px rgba(124,58,237,0.45) !important;
}}

/* Settings icon button — small & outlined */
div[data-testid="column"]:last-child .stButton > button {{
    background:transparent !important;
    border:1.5px solid rgba(167,139,250,0.45) !important;
    color:#a78bfa !important;
    font-size:1rem !important;
    padding:0.3rem 0.7rem !important;
    box-shadow:none !important;
    width:auto !important;
    min-width:unset !important;
}}

/* Download save button */
.stDownloadButton > button {{
    background:linear-gradient(135deg,#047857,#0e7490) !important;
    color:white !important;
    border:none !important;
    border-radius:13px !important;
    font-family:'Syne',sans-serif !important;
    font-weight:700 !important;
    padding:0.65rem 1.5rem !important;
    width:100% !important;
    box-shadow:0 4px 18px rgba(4,120,87,0.28) !important;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background:{inp_bg} !important;
    border:1.5px solid {inp_bdr} !important;
    border-radius:13px !important;
    color:{fg} !important;
}}

/* Progress bar */
.stProgress > div > div > div > div {{
    background:linear-gradient(90deg,#7c3aed,#db2777) !important;
    border-radius:10px !important;
}}

.meta   {{ color:{sub}; font-size:0.81rem; margin:0.25rem 0 0.7rem; }}
.vtitle {{ font-family:'Syne',sans-serif; font-weight:700; font-size:1.04rem; color:{fg}; margin:0.5rem 0 0.15rem; line-height:1.3; }}
.stag   {{ font-size:0.77rem; color:{sub}; font-style:italic; margin-top:0.35rem; }}

[data-testid="stSidebar"] {{ background:{sb_bg} !important; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="aura-wrap">
  <h1 class="aura-name">AURA</h1>
  <p class="aura-sub">Universal Media Downloader</p>
  <div>
    <span class="badge yt">▶ YouTube</span>
    <span class="badge ig">◈ Instagram</span>
    <span class="badge tt">♪ TikTok</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Settings gear button — top right
_, col_gear = st.columns([6, 1])
with col_gear:
    if st.button("⚙️", key="gear_btn", help="Settings & About"):
        st.session_state.settings_open = not st.session_state.settings_open
        st.rerun()

# ============================================================
# STAGE: HOME
# ============================================================
if st.session_state.stage == 'home':

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<p style='font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:{fg};margin:0 0 0.5rem;'>🔗 Paste Video Link</p>", unsafe_allow_html=True)

    url = st.text_input(
        "url",
        placeholder="youtube.com/watch?v=...  •  instagram.com/reel/...  •  tiktok.com/...",
        label_visibility="collapsed",
        key="url_input"
    )

    c1, c2 = st.columns([5, 1])
    with c1:
        fetch_btn = st.button("🔍  FETCH VIDEO INFO", use_container_width=True)
    with c2:
        if url:
            pf = detect_platform(url)
            icons = {"youtube": "▶️", "instagram": "📸", "tiktok": "🎵", "other": "🌐"}
            st.markdown(
                f"<div style='text-align:center;padding-top:0.5rem;font-size:1.3rem'>{icons.get(pf,'🌐')}</div>",
                unsafe_allow_html=True
            )

    if fetch_btn:
        if not (url and url.strip()):
            st.error("⚠️ Please paste a link first.")
        else:
            url = url.strip()
            pf  = detect_platform(url)
            bar = st.progress(0, text="Connecting…")
            try:
                bar.progress(25, text="Fetching video info…")
                info = get_video_info(url)
                bar.progress(70, text="Reading formats…")
                fmts = get_format_sizes(info, pf)
                bar.progress(100, text="Done!")
                st.session_state.video_info = info
                st.session_state.url        = url
                st.session_state.formats    = fmts
                st.session_state.platform   = pf
                st.session_state.stage      = 'quality'
                time.sleep(0.2)
                st.rerun()
            except Exception as e:
                bar.empty()
                msg = str(e)
                if "private" in msg.lower():
                    st.error("🔒 Private video — please use a public link.")
                elif "sign in" in msg.lower() or "login" in msg.lower():
                    st.error("🔑 Login required — only public videos are supported.")
                elif "not available" in msg.lower():
                    st.error("❌ Video unavailable or removed.")
                else:
                    st.error("❌ Could not fetch video. Please check the link and try again.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""<div class="card" style="padding:0.9rem 1.5rem;">
    <p style="color:{sub};font-size:0.8rem;margin:0;line-height:2;">
    💡 <b>Tips</b><br>
    • YouTube — full URL or short youtu.be link<br>
    • Instagram — must be a public Reel or post<br>
    • TikTok — use Share → Copy Link from the app
    </p></div>""", unsafe_allow_html=True)

# ============================================================
# STAGE: QUALITY
# ============================================================
elif st.session_state.stage == 'quality':
    info     = st.session_state.video_info
    formats  = st.session_state.formats
    platform = st.session_state.platform
    url      = st.session_state.url

    thumb    = info.get('thumbnail')
    title    = info.get('title', 'Video')
    duration = info.get('duration')
    uploader = info.get('uploader') or info.get('channel') or ""

    pf_icon  = {"youtube": "🔴", "instagram": "💜", "tiktok": "🖤", "other": "🌐"}
    pf_label = {"youtube": "YouTube", "instagram": "Instagram", "tiktok": "TikTok", "other": "Web"}

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if thumb:
        st.image(thumb, use_container_width=True)

    dur_str = f"⏱ {int(duration//60)}m {int(duration%60)}s  •  " if duration else ""
    st.markdown(f"""
    <div class="vtitle">{title[:85]}{'…' if len(title) > 85 else ''}</div>
    <div class="meta">{pf_icon.get(platform,'🌐')} {pf_label.get(platform,'Web')}
     &nbsp;•&nbsp; {dur_str}{uploader}</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p style='font-family:Syne,sans-serif;font-weight:700;color:{fg};margin:0 0 0.4rem;'>📥 Select Quality</p>", unsafe_allow_html=True)

    fmt_keys   = list(formats.keys())
    fmt_labels = [f"{k}  ({fmt_size(formats[k]['size'])})" for k in fmt_keys]

    sel_idx = st.selectbox(
        "qual", range(len(fmt_labels)),
        format_func=lambda i: fmt_labels[i],
        label_visibility="collapsed"
    )

    sel_key  = fmt_keys[sel_idx]
    sel_fmt  = formats[sel_key]
    is_audio = sel_fmt.get('is_audio', False)
    ftype    = "MP3 Audio" if is_audio else "MP4 Video"
    st.markdown(f"<div class='stag'>📦 {ftype}  |  Est. size: {fmt_size(sel_fmt['size'])}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    dl_btn = st.button("⬇️  DOWNLOAD NOW", use_container_width=True)

    if dl_btn:
        bar = st.progress(0, text="Starting download…")
        try:
            bar.progress(15, text="Connecting to platform…")
            time.sleep(0.3)
            bar.progress(45, text="Downloading… (may take a moment)")

            path = download_video(url, sel_fmt['format'], is_audio)
            bar.progress(90, text="Preparing file…")
            time.sleep(0.2)

            if path and os.path.exists(path):
                bar.progress(100, text="✅ Ready!")
                ext   = "mp3" if is_audio else "mp4"
                safe  = re.sub(r'[^\w\s-]', '', title[:40]).strip().replace(' ', '_')
                fname = f"AURA_{safe}.{ext}"

                with open(path, "rb") as f:
                    data = f.read()

                st.success("✅ Done! Tap the button below to save to your device.")
                st.download_button(
                    label=f"💾  SAVE TO DEVICE  ({fmt_size(len(data))})",
                    data=data,
                    file_name=fname,
                    mime="audio/mpeg" if is_audio else "video/mp4",
                    use_container_width=True
                )
                try: os.remove(path)
                except: pass
            else:
                bar.empty()
                st.error("❌ File not found after download. Please try again.")

        except Exception as e:
            bar.empty()
            err = str(e)
            if "ffmpeg" in err.lower():
                st.error("⚠️ FFmpeg missing. Make sure 'ffmpeg' is in packages.txt.")
            elif "403" in err or "forbidden" in err.lower():
                st.warning("⚠️ Platform blocked the request. Please try a different quality option.")
            elif "unavailable" in err.lower() or "removed" in err.lower():
                st.error("❌ This video is no longer available.")
            elif "nsig" in err.lower() or "cipher" in err.lower():
                st.error("⚠️ yt-dlp is outdated. Update it: pip install -U yt-dlp")
            else:
                st.warning(f"⚠️ Error occurred: {err[:250]}")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("← Search New Link"):
        st.session_state.stage      = 'home'
        st.session_state.video_info = None
        st.session_state.formats    = {}
        st.session_state.platform   = 'other'
        st.rerun()
