st.markdown("""
<style>

/* 🌌 Animated Background */
.stApp {
    background: linear-gradient(270deg, #0f0c29, #302b63, #24243e, #1a012d);
    background-size: 800% 800%;
    animation: gradientFlow 20s ease infinite;
}

/* Background Animation */
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ✨ Glass Card */
.glass {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 
        0 8px 32px rgba(145,70,255,0.3),
        inset 0 0 10px rgba(255,255,255,0.05);
    transition: 0.4s ease;
}

/* Hover float effect */
.glass:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 
        0 12px 40px rgba(145,70,255,0.5),
        inset 0 0 12px rgba(255,255,255,0.08);
}

/* 🌟 Title Glow */
.title {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    color: white;
    text-shadow: 0 0 20px rgba(145,70,255,0.9);
    animation: fadeIn 1.5s ease;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.6);
    margin-bottom: 30px;
}

/* 🧊 Input Field */
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(145,70,255,0.6) !important;
    color: white !important;
    border-radius: 12px;
    text-align: center;
    transition: 0.3s;
}

/* Input Glow */
.stTextInput input:focus {
    border: 1px solid #9146ff !important;
    box-shadow: 0 0 10px #9146ff;
}

/* ⚡ Neon Buttons */
.stButton button {
    background: linear-gradient(90deg, #9146ff, #6200ea);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: bold;
    letter-spacing: 1px;
    height: 3em;
    width: 100%;
    transition: 0.3s;
    box-shadow: 0 0 10px rgba(145,70,255,0.5);
}

/* Button Hover */
.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 20px rgba(145,70,255,0.9);
}

/* 🎬 Fade Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px);}
    to { opacity: 1; transform: translateY(0);}
}

/* 📊 Progress Bar Glow */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #9146ff, #6200ea);
    box-shadow: 0 0 10px #9146ff;
}

/* Hide default UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)
