import streamlit as st
# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="TN Kalvimate", layout="wide")

st.markdown("""
<style>

/* 🔹 Login background container (IMPORTANT FIX) */
.login-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 0;   /* was -1 ❌ */
}

/* 🔹 Bubble style */
.bubble {
    position: absolute;
    bottom: -120px;
    width: 40px;
    height: 40px;
    background: rgba(255,255,255,0.15);
    border-radius: 50%;
    animation: rise 20s infinite ease-in;
}

/* Different sizes & speeds */
.bubble:nth-child(1) { left: 10%; animation-duration: 18s; }
.bubble:nth-child(2) { left: 25%; width: 60px; height: 60px; animation-duration: 22s; }
.bubble:nth-child(3) { left: 40%; animation-duration: 16s; }
.bubble:nth-child(4) { left: 60%; width: 50px; height: 50px; animation-duration: 25s; }
.bubble:nth-child(5) { left: 80%; animation-duration: 19s; }
.bubble:nth-child(6) { left: 90%; width: 30px; height: 30px; animation-duration: 21s; }

/* 🔹 Animation */
@keyframes rise {
    0% {
        transform: translateY(0);
        opacity: 0;
    }
    20% {
        opacity: 0.6;
    }
    100% {
        transform: translateY(-1000px);
        opacity: 0;
    }
}

/* 🔹 Make login card ABOVE bubbles */
.login-box {
    position: relative;
    z-index: 2;   /* important */
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ================= GLOBAL BACKGROUND ================= */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    background-size: 200% 200%;
    animation: gradientMove 15s ease infinite;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}



/* ================= LOGIN CARD ================= */
.login-box {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(10px);
}

/* ================= BUTTONS ================= */
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* ================= CHAT CONTAINER ================= */
.chat-container {
    max-width: 850px;
    margin: auto;
    padding: 20px;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    border-radius: 20px;
}

/* ================= CHAT BUBBLES ================= */
.user-bubble {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    padding: 12px;
    border-radius: 15px 15px 0 15px;
    margin: 10px 0;
    text-align: right;
}

.bot-bubble {
    background: rgba(255,255,255,0.9);
    color: black;
    padding: 12px;
    border-radius: 15px 15px 15px 0;
    margin: 10px 0;
}

/* ================= INPUT ================= */
.stTextInput>div>div>input {
    border-radius: 10px;
}

/* ================= PDF VIEW ================= */
iframe {
    border-radius: 12px;
}

/* ================= TITLE ================= */
h1, h2, h3 {
    color: white;
}

/* ================= CARD ================= */
.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

from auth import login, signup
# ✅ MUST BE HERE (top)
st.markdown("""
<div class="login-bg">
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
</div>
""", unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "chat"

from chat_ui import init_chat_state, render_chat_interface, chat_input_box
from rag import ask_rag, generate_study_plan
import base64
import os
import streamlit.components.v1 as components
# LOGIN SYSTEM
import os

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        # ✅ Get image path safely
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(BASE_DIR, "assets", "books.png")

        # ✅ Show image if exists
        if os.path.exists(logo_path):
            st.image(logo_path, width=120)
        else:
            st.warning("⚠ Logo not found")
        if os.path.exists("assets"):
           st.write("Assets folder found:", os.listdir("assets"))
        else:
         st.write("❌ No assets folder found")

        # ✅ ALWAYS show title
        st.markdown("## 🔐 Welcome to EduAI")

        # ✅ Login box UI
        st.markdown('<div class="login-box">', unsafe_allow_html=True)


        tab1, tab2 = st.tabs(["Login", "Signup"])

        # ---------------- LOGIN ----------------
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.page = "chat"
                    st.session_state.user = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        # ---------------- SIGNUP ----------------
        with tab2:
            new_user = st.text_input("New Username", key="signup_user")
            new_pass = st.text_input("New Password", type="password", key="signup_pass")

            if st.button("Signup"):
                success, msg = signup(new_user, new_pass)
                if success:
                    st.success(msg)
                    st.success(f"Welcome {new_user}! 🎉")
                else:
                    st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)

    # LOGIN PAGE
if not st.session_state.logged_in:

    # login form
    if success:
        st.session_state.logged_in = True
        st.session_state.page = "chat"
        st.rerun()

    st.stop()   # stop only AFTER UI

    st.markdown('</div>', unsafe_allow_html=True)

   

st.markdown("""
<style>

/* ---------- BACKGROUND (School Theme) ---------- */
.stApp {
    background-image: url("https://img.freepik.com/free-vector/abstract-low-poly-geometric-dots-lines-connectivity-vector_1017-45668.jpg?semt=ais_hybrid&w=740&q=80");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}



/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(10px);
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ---------- HEADINGS ---------- */
h1, h2, h3 {
    color: #1e293b;
    font-weight: 600;
}

/* ---------- BUTTONS ---------- */
.stButton>button {
    border-radius: 12px;
    padding: 10px;
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
}

/* ---------- INPUT BOX ---------- */
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
}

/* ---------- CHAT INPUT ---------- */
textarea, input {
    border-radius: 10px !important;
}

/* ---------- CHAT MESSAGE STYLE ---------- */
[data-testid="stChatMessage"] {
    background-color: black;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}

/* ---------- CARD STYLE ---------- */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* ---------- DOWNLOAD BUTTON ---------- */
.stDownloadButton>button {
    border-radius: 10px;
    background-color: #16a34a;
    margin-bottom: 30px;
}

.stDownloadButton>button:hover {
    background-color: #15803d;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #94a3b8;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------- QUESTION PAPER PDF ----------
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ QUESTION PAPERS
question_pdf_files = {
    "Computer Science":"https://drive.google.com/uc?id=cTIycvTfOtdh5yYo6jX2Ph1DEE_1A2j",
    "Physics": "https://drive.google.com/uc?id=1e0tpLGuJ8u319TFOgBKapsm-zivwrcXM",
    "Chemistry":"https://drive.google.com/uc?id=1QwHixvHfIo3_CO4pbueBeAhh9ajeYQ2Q",
    "Mathematics":"https://drive.google.com/uc?id=12K9AbilMV889rH0od79OrMLquMaU1JeR",
    "Tamil":"https://drive.google.com/uc?id=1aANLs4TOYBzvhkAJ-J8qDpfvfU6Ds8OI",
    "English" :"https://drive.google.com/uc?id=1mAvXhiD7JUFkROZ2x6Bkbn8jziocmp_R"
}

# ✅ STUDY PLANNER FILES
planner_pdf_map = {
    "Computer Science":"https://drive.google.com/uc?id=16xEUCo1XOA1oAT1RtkxpKbH8yQW1H6FW",
    "Physics":"https://drive.google.com/uc?id=1s7MpCwylHEOxn1z5TuvGpwEbPtvN43zP",
    "Chemistry":"https://drive.google.com/uc?id=1Y7fLTcj9lUAigbonCyzHfWdvOzLG3bbQ",
    "Mathematics":"https://drive.google.com/uc?id=1fT4M4iYmPMbGOWhCgwQleI_p4x4O1HIW",
    "Tamil":"https://drive.google.com/uc?id=1RIL03AHQOyeMlqamwUHEl5_qRC4L-YjE",
    "English":"https://drive.google.com/uc?id=1fvm97i3KMuTfLF3GI8nzVH9knZakNKtO"
}
import requests
def display_pdf(file_path):
    try:
        if file_path.startswith("http"):
            response = requests.get(file_path)
            pdf_bytes = response.content
        else:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        st.markdown(f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}"
        width="100%" height="700"></iframe>
        """, unsafe_allow_html=True)

        st.download_button(
            "⬇ Download PDF",
            data=pdf_bytes,
            file_name="file.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error("❌ Unable to load PDF")



# ---------- STUDY PLANNER ----------
def study_planner():
    

    subject = st.selectbox("Select Subject", list(planner_pdf_map.keys()))
    days = st.slider("Preparation Days", 3, 30, 7)
    hours = st.slider("Study Hours per Day", 1, 8, 3)

    if st.button("Generate AI Study Plan"):
        with st.spinner("Generating your study plan..."):
            pdf_path = planner_pdf_map[subject]
            plan = generate_study_plan(subject, days, hours, pdf_path)

        st.subheader("📚 AI Generated Study Plan")
        st.write(plan)
# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("📚 TN Kalvimate")
    st.write(f"👤 {st.session_state.get('user','User')}")


    if st.button("📖 Question Papers", use_container_width=True):
        st.session_state.page = "qp"
        st.rerun()

    if st.button("📝 Mock Tests", use_container_width=True):
        st.session_state.page = "mock"

    if st.button("📄 Study Planner", use_container_width=True):
        st.session_state.page = "planner"
        st.rerun()
    
    if st.button("🤖 Q & A", use_container_width=True):
        st.session_state.page = "chat"
    
    if st.button("🧠 AI Evaluator", use_container_width=True):
        st.session_state.page = "evaluator"

    st.divider()

    # ✅ FIXED LOGOUT
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


# ---------- PAGE ROUTING ----------

# 📖 QUESTION PAPER
if st.session_state.page == "qp":
    st.header("📖 Question Papers")

    subject = st.selectbox(
        "Select Subject",
        list(question_pdf_files.keys())
    )

    file_path = question_pdf_files.get(subject)

    if file_path:
        display_pdf(file_path)
    else:
        st.error("❌ No file mapped")


# 📄 STUDY PLANNER
elif st.session_state.page == "planner":
    st.header("📅 Study Planner")
    study_planner()
    init_chat_state()
    render_chat_interface()
    chat_input_box()


# 🧠 AI EVALUATOR
elif st.session_state.page == "evaluator":

    st.header("🧠 AI Answer Evaluator")
    st.write("Upload your answer image and click submit")

    from PIL import Image
    import pytesseract
    import ollama

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🚀 Submit"):

        if uploaded_file is None:
            st.warning("Please upload an image first!")
        else:
            st.info("🔍 Processing your image...")

            image = Image.open(uploaded_file)
            image = image.convert('L')

            extracted_text = pytesseract.image_to_string(image)

            st.subheader("📄 Extracted Text")
            st.write(extracted_text)

            st.info("🧠 Evaluating answer...")

            prompt = f"""
Evaluate the student's answer.

Question: Explain the concept clearly.

Expected:
- Key concepts
- Explanation
- Important points

Student Answer:
{extracted_text}

Give:
1. Score out of 10
2. Missing points
3. Suggestions to improve
"""

            response = ollama.chat(
                model='phi3',
                messages=[{"role": "user", "content": prompt}]
            )

            st.subheader("📊 Evaluation Result")
            st.write(response['message']['content'])
            study_planner()
            init_chat_state()
            render_chat_interface()
            chat_input_box()



# 📝 MOCK TEST
elif st.session_state.page == "mock":
    st.header("📝 Mock Test")

    with open("Final output.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    components.html(html_code, height=900, scrolling=True)

    
    init_chat_state()
    render_chat_interface()
    chat_input_box()



# 🤖 CHATBOT (ONLY HERE)
elif st.session_state.page == "chat":
    st.header("🤖 Q & A")
    st.divider()

    init_chat_state()
    render_chat_interface()
    chat_input_box()
