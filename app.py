st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(270deg, #0f0c29, #302b63, #24243e, #1a012d);
        background-size: 800% 800%;
        animation: gradientFlow 20s ease infinite;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .glass {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(145,70,255,0.3);
    }

    .stButton>button {
        background: linear-gradient(90deg, #9146ff, #6200ea);
        border-radius: 12px;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)
