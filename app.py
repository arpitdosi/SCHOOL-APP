import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import random

# --- API SETUP ---
API_KEY = "अपनी_API_KEY_यहाँ_पेस्ट_करें" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Rutvi's Smart School", layout="wide", page_icon="🎓")

st.title("🌟 Rutvi's Master Study App")
st.write("---")

# --- SIDEBAR: PROGRESS ---
st.sidebar.header("📈 Study Progress")

# 1. MULTIPLE FILE UPLOADER
uploaded_files = st.file_uploader("📸 Upload Chapter/Revision Pages", 
                                  type=['jpg', 'jpeg', 'png'], 
                                  accept_multiple_files=True)

if uploaded_files:
    num_pages = len(uploaded_files)
    st.sidebar.success(f"✅ {num_pages} Pages in Session")
    
    # --- SECTION 1: WHOLE CHAPTER / MIX REVISION ---
    st.header("📋 Whole Chapter / Mix Revision")
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("📖 Summarize Everything (पूरा चैप्टर समझाओ)"):
            with st.spinner("AI Teacher is reading all pages for a summary..."):
                # Sending all images for a combined summary
                images_to_process = [Image.open(f) for f in uploaded_files]
                response = model.generate_content(["Look at all these pages and give a combined summary/story of the whole chapter in Hinglish.", *images_to_process])
                st.info(response.text)
                
    with col_b:
        if st.button("🎲 Mega Quiz (Mix Questions from all pages)"):
            with st.spinner("Creating a mixed revision quiz..."):
                random_page = random.choice(uploaded_files)
                img_for_quiz = Image.open(random_page)
                response = model.generate_content(["Create 1 tough MCQ from this page for a mix-revision test.", img_for_quiz])
                st.warning(response.text)
                st.balloons()

    st.write("---")
    
    # --- SECTION 2: SPECIFIC PAGE STUDY ---
    st.header("🔍 Specific Page Study")
    page_number = st.select_slider("Select a page to focus:", options=range(1, num_pages + 1), value=1)
    
    current_img_file = uploaded_files[page_number - 1]
    raw_img = Image.open(current_img_file)
    
    # Compression for speed
    raw_img.thumbnail((1000, 1000), Image.LANCZOS)
    st.image(raw_img, caption=f"Focusing on: Page {page_number}", width=450)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📄 Explain Page {page_number}"):
            with st.spinner(f"Reading Page {page_number}..."):
                response = model.generate_content(["Explain this specific page in detail (Hinglish).", raw_img])
                st.success(response.text)
                
    with col2:
        if st.button(f"🎯 Quiz on Page {page_number}"):
            with st.spinner("Generating question..."):
                response = model.generate_content(["Create 1 MCQ question from this page.", raw_img])
                st.write(response.text)

else:
    st.info("👋 Rutvi, please upload your pages to start the Master Class!")

st.sidebar.write("---")
st.sidebar.write("Goal: Complete 5 Chapters! 🚀")
