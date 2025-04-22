import random
import streamlit as st
import string
from datetime import datetime

# Initialize session states
if 'strength_history' not in st.session_state:
    st.session_state.strength_history = []
if 'current_password' not in st.session_state:
    st.session_state.current_password = None

def check_strength(password):
    """Returns strength score 1-5 and feedback"""
    if not password:
        return 0, ["Enter a password to check"]
        
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Consider longer password (12+ chars)")
    
    # Complexity checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    if has_upper and has_lower:
        score += 1
    else:
        feedback.append("Mix uppercase and lowercase")
    
    if has_digit:
        score += 1
    else:
        feedback.append("Add numbers")
    
    if has_special:
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Unique chars check
    if len(set(password)) >= len(password)*0.7:
        score += 1
    else:
        feedback.append("More unique characters")
    
    return min(score, 5), feedback

# --- UI ---
st.title("🔐 Password Strength Analyzer")

# Password Strength Checker
with st.expander("🔍 Check Password Strength", expanded=True):
    user_password = st.text_input("Enter password to analyze:", type="password", key="pwd_input")
    check_button = st.button("Check Strength")
    
    if check_button or user_password:
        score, feedback = check_strength(user_password)
        
        # Add to history if checked via button
        if check_button and user_password:
            st.session_state.strength_history.append({
                "password": user_password,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "strength": score
            })
        
        # Display results
        st.progress(score/5)
        st.subheader(f"Strength: {'⭐' * score if score > 0 else '🚫 No password'}")
        if feedback:
            st.warning("#### Improvement Suggestions:")
            for item in feedback:
                st.write(f"- {item}")

# Strength History
if st.session_state.strength_history:
    st.divider()
    st.subheader("📜 Analysis History")
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.strength_history = []
        st.rerun()
    
    # Display history
    for entry in reversed(st.session_state.strength_history[-5:]):
        with st.container(border=True):
            cols = st.columns([3,1,1])
            cols[0].code(entry['password'])
            cols[1].write(entry['time'])
            cols[2].metric("Score", f"{'⭐' * entry['strength']}")

def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return "".join(random.choice(characters) for _ in range(length))

st.title("Password Generator")

length = st.slider("Select Password Length", min_value=4, max_value=32, value=12)

use_digits = st.checkbox("Use Digits")

use_special = st.checkbox("Use Special Characters")

if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special)
    st.write(f'Generated password: {password}')

st.write("-----------------------------------")

st.write("Build with ❤️ by Aliyan Ahmed")