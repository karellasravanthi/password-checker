import streamlit as st
import re
import random
import string

# Streamlit Page Config
st.set_page_config(page_title="Password Strength Checker", page_icon="🔒", layout="wide")

# Custom Dark CSS for Dashboard Styling matching the Reference Image
st.markdown("""
<style>
    /* Dark Background */
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }
    
    /* Card Container Styling */
    div.css-1r6slb0, div.stColumn > div {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    
    /* Custom Purple Button Styling */
    .stButton>button {
        background-color: #6e44ff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5833e6;
        color: white;
    }
    
    /* Score Display Box */
    .score-container {
        text-align: center;
        padding: 10px;
    }
    .score-text-strong {
        color: #2ea44f;
        font-size: 28px;
        font-weight: bold;
    }
    .score-text-moderate {
        color: #e3b341;
        font-size: 28px;
        font-weight: bold;
    }
    .score-text-weak {
        color: #f85149;
        font-size: 28px;
        font-weight: bold;
    }
    .score-value {
        font-size: 22px;
        color: #8b949e;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.title("🔒 Password Strength Checker")
st.write("Check the strength of your password and create a strong one.")
st.write("---")

# Session state initialization for password generation
if "generated_password" not in st.session_state:
    st.session_state.generated_password = "G7!kLp#2mQ$9xR"

# Layout: Top Row
col1, col2 = st.columns([1, 1])

# --- TOP LEFT: ENTER PASSWORD ---
with col1:
    st.subheader("Enter Password")
    user_password = st.text_input("", type="password", placeholder="Type your password here...", key="pwd_input")
    check_btn = st.button("Check Strength")

# --- TOP RIGHT: STRENGTH METER & SCORE ---
with col2:
    st.subheader("Strength")
    
    # Calculate Strength Score
    score = 0
    if user_password:
        if len(user_password) >= 8: score += 20
        if len(user_password) >= 12: score += 10
        if re.search(r"[a-z]", user_password): score += 20
        if re.search(r"[A-Z]", user_password): score += 20
        if re.search(r"\d", user_password): score += 15
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password): score += 15

    # Determine Label & Color based on score
    if score >= 80:
        label = "Strong"
        css_class = "score-text-strong"
    elif score >= 50:
        label = "Moderate"
        css_class = "score-text-moderate"
    else:
        label = "Weak"
        css_class = "score-text-weak"

    st.markdown(f"""
        <div class="score-container">
            <div class="{css_class}">{label if user_password else "N/A"}</div>
            <div class="score-value">Score: <b>{score}/100</b></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Visual Progress Bar
    st.progress(score / 100)

st.write("")

# Layout: Bottom Row
col3, col4 = st.columns([1, 1])

# --- BOTTOM LEFT: PASSWORD ANALYSIS CHECKLIST ---
with col3:
    st.subheader("Password Analysis")
    
    c_len = "✅" if len(user_password) >= 8 else "❌"
    c_upper = "✅" if re.search(r"[A-Z]", user_password) else "❌"
    c_lower = "✅" if re.search(r"[a-z]", user_password) else "❌"
    c_num = "✅" if re.search(r"\d", user_password) else "❌"
    c_spec = "✅" if re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password) else "❌"

    st.write(f"{c_len} Minimum 8 characters")
    st.write(f"{c_upper} Contains uppercase letters")
    st.write(f"{c_lower} Contains lowercase letters")
    st.write(f"{c_num} Contains numbers")
    st.write(f"{c_spec} Contains special characters")

# --- BOTTOM RIGHT: GENERATE STRONG PASSWORD ---
with col4:
    st.subheader("Generate Strong Password")
    
    pwd_length = st.slider("Length:", min_value=8, max_value=32, value=16)
    
    # Generate Password Action
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    st.session_state.generated_password = "".join(random.choice(chars) for _ in range(pwd_length))

    st.code(st.session_state.generated_password, language="")
    
    if st.button("Copy Password"):
        st.toast("Password displayed! You can copy it directly from above box.", icon="📋")