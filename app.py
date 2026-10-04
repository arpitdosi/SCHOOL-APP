import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- API SETUP ---
API_KEY = "अपनी_API_KEY_यहाँ_पेस्ट_करें" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Flash model is fast

st.set_page_config(page_title="Rutvi's Smart School", layout="wide", page_icon="🎓")

# --- CUSTOM CSS FOR FAST LOADING ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4CAF50 , #8BC34A); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Rutvi's Fast Smart School")
st.write("---")

# 1. MULTIPLE FILE UPLOADER WITH PROGRESS
uploaded_files = st.file_uploader("📸 Upload Chapter Pages (एक साथ कई फोटो चुनें)", 
                                  type=['jpg', 'jpeg', 'png'], 
                                  accept_multiple_files=True)

if uploaded_files:
    num_pages = len(uploaded_files)
    
    # 2. PAGE SELECTION SLIDER
    page_number = st.select_slider(
        "Select Page Number:",
        options=range(1, num_pages + 1),
        value=1
    )
    
    # Get and compress the selected image
    current_img_file = uploaded_files[page_number - 1]
    raw_img = Image.open(current_img_file)
    
    # --- COMPRESSION LOGIC (ये फोटो को हल्का बना देगा) ---
    # Resize if image is too large
    max_size = (1000, 1000)
    raw_img.thumbnail(max_size, Image.LANCZOS)
    
    # Save to buffer to reduce quality
    img_byte_arr = io.BytesIO()
    raw_img.save(img_byte_arr, format='JPEG', quality=70) # 70% quality is enough for reading
    processed_img = Image.open(img_byte_arr)
    
    # Display the current page
    st.image(processed_img, caption=f"Page {page_number} of {num_pages}", width=500)
    
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"📖 Explain Page {page_number}"):
            with st.spinner("AI Teacher is analyzing the light-weight image..."):
                response = model.generate_content([
                    "Explain this textbook page clearly for a class 5 student. Mix Hindi and English.", 
                    processed_img
                ])
                st.info(response.text)
                
    with col2:
        if st.button(f"🎮 Play Quiz (Page {page_number})"):
            with st.spinner("Creating Quiz..."):
                response = model.generate_content([
                    "Create 1 MCQ question from this page. Keep it simple for a child.", 
                    processed_img
                ])
                st.success(response.text)

else:
    st.info("👋 Rutvi, please upload your chapter pages!")

st.sidebar.write(f"Points: {num_pages * 10 if uploaded_files else 0} ⭐")
