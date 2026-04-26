import streamlit as st
import yt_dlp

def get_video_info(url):
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def format_size(bytes):
    if not bytes: return "Unknown"
    return f"{bytes / (1024 * 1024):.1f} MB"

st.title("AURA DOWNLOADER")

url = st.text_input("Paste Link Here...")

if url:
    try:
        info = get_video_info(url)
        st.image(info['thumbnail'], width=300)
        st.write(f"**Title:** {info['title']}")

        # ලබා ගත හැකි Quality සහ Size ලැයිස්තුවක් සෑදීම
        formats = info.get('formats', [])
        display_options = {}

        for f in formats:
            # වීඩියෝ සහ ඕඩියෝ දෙකම තියෙන (ext='mp4') ඒවා පමණක් තෝරාගැනීම
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                res = f.get('height')
                size = format_size(f.get('filesize') or f.get('filesize_approx'))
                label = f"{res}p - ({size})"
                display_options[label] = f['url']

        selected_label = st.selectbox("Select Quality & Size:", list(display_options.keys()))

        if st.button("GET DOWNLOAD LINK"):
            direct_url = display_options[selected_label]
            # සෘජු ලින්ක් එක බටන් එකක් ලෙස ලබා දීම
            st.markdown(f'''
                <a href="{direct_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #ff0080; color: white; padding: 10px; text-align: center; border-radius: 10px; font-weight: bold;">
                        CLICK HERE TO SAVE VIDEO
                    </div>
                </a>
            ''', unsafe_allow_html=True)
            st.info("පොප්-අප් එකක් විවෘත වූ විට වීඩියෝ එක මත 'Right Click' කර 'Save Video As' දෙන්න.")

    except Exception as e:
        st.error("Error fetching video. Please check the link.")
        
