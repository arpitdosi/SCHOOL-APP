import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- अपनी API KEY यहाँ डालें ---
API_KEY = "यहा_अपनी_चाबी_पेस्ट_करें"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Rutvi's School", layout="wide")

st.title("🌟 Rutvi's Interactive Smart School")

# Sidebar for settings
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Study Dashboard", "About Rutvi"])

uploaded_file = st.file_uploader("📸 Take or Upload Exercise Photo", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Current Page", width=400)
    
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📖 Story Mode (Explain)"):
            with st.spinner("AI Teacher is thinking..."):
                response = model.generate_content(["Explain this chapter image to a 5th grade student in simple English and Hindi mix story format.", img])
                st.info(response.text)
                
    with col2:
        if st.button("🎮 Game Mode (Quiz)"):
            with st.spinner("Creating a fun quiz..."):
                prompt = "Extract 1 multiple choice question from this image with 4 options. Format it nicely."
                response = model.generate_content([prompt, img])
                st.success(response.text)

st.sidebar.write("---")
st.sidebar.write("Keep studying, Rutvi! ⭐")
