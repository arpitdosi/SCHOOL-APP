import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- अपनी API KEY यहाँ डालें ---
API_KEY = "अपनी_API_KEY_यहाँ_पेस्ट_करें" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Rutvi's Smart School", layout="wide", page_icon="🎓")

st.title("🌟 Rutvi's Interactive Smart School")
st.write("---")

# Sidebar for Navigation and Info
st.sidebar.header("📚 Chapter Manager")
st.sidebar.write("Upload all pages of the chapter together.")

# 1. MULTIPLE FILE UPLOADER
uploaded_files = st.file_uploader("📸 Upload All Chapter Pages (1-15 pages)", 
                                  type=['jpg', 'jpeg', 'png'], 
                                  accept_multiple_files=True)

if uploaded_files:
    # Total pages uploaded
    num_pages = len(uploaded_files)
    st.sidebar.success(f"✅ {num_pages} Pages Loaded!")
    
    # 2. PAGE SELECTION SLIDER
    # रुत्वि यहाँ से पेज चुन सकती है
    page_number = st.select_slider(
        "Select the page you want to study:",
        options=range(1, num_pages + 1),
        value=1
    )
    
    # Get the current selected image
    current_img_file = uploaded_files[page_number - 1]
    img = Image.open(current_img_file)
    
    # Display the current page
    st.image(img, caption=f"Currently studying: Page {page_number} of {num_pages}", width=500)
    
    st.write("---")
    st.write(f"### Options for Page {page_number}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"📖 Explain Page {page_number}"):
            with st.spinner(f"Teacher is reading Page {page_number}..."):
                response = model.generate_content([
                    "Explain this specific textbook page to a 5th grade student. "
                    "Use a mix of simple English and Hindi. Keep it like a story.", 
                    img
                ])
                st.info(response.text)
                
    with col2:
        if st.button(f"🎮 Play Quiz (Page {page_number})"):
            with st.spinner("Generating fun questions..."):
                prompt = (
                    "Create 1 interesting multiple choice question from this page with 4 options (A,B,C,D). "
                    "Tell me the correct answer at the end. Format it clearly."
                )
                response = model.generate_content([prompt, img])
                st.success(response.text)

else:
    st.info("👋 Hello Rutvi! Please ask Papa to upload your chapter pages to start studying.")

st.sidebar.write("---")
st.sidebar.write("Keep studying, Rutvi! ⭐")
