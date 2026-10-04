import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- अपनी API KEY यहाँ डालें ---
API_KEY = "अपनी_API_KEY_यहाँ_पेस्ट_करें" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Rutvi's Smart School", layout="wide", page_icon="🎓")

st.title("🌟 Rutvi's Interactive Smart School")

# Sidebar
st.sidebar.header("📚 Chapter Manager")
uploaded_files = st.file_uploader("📸 Upload All Chapter Pages Together", 
                                  type=['jpg', 'jpeg', 'png'], 
                                  accept_multiple_files=True)

if uploaded_files:
    num_pages = len(uploaded_files)
    all_images = [Image.open(f) for f in uploaded_files]
    st.sidebar.success(f"✅ {num_pages} Pages Ready!")

    # --- SECTION 1: FULL CHAPTER MODE ---
    st.header("🏆 Full Chapter Mode (Big Boss)")
    st.write("AI will read all pages together to help you master the whole chapter!")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📖 Full Chapter Summary (Hinglish)"):
            with st.spinner("AI Teacher is reading the entire chapter..."):
                # Sending ALL images to Gemini at once
                prompt = "Look at all these images of a school chapter. Provide a detailed summary and explanation of the entire chapter in a mix of Hindi and English for a 5th grade student."
                response = model.generate_content([prompt] + all_images)
                st.info(response.text)
                
    with col_b:
        if st.button("✍️ Full Chapter Mega Quiz"):
            with st.spinner("Creating a grand test from all pages..."):
                prompt = "Look at all these chapter pages. Create a 5-question multiple choice test covering different parts of the chapter. Provide options and answers."
                response = model.generate_content([prompt] + all_images)
                st.success(response.text)

    st.write("---")

    # --- SECTION 2: PAGE FOCUS MODE ---
    st.header("🔍 Focus Mode (Page by Page)")
    page_number = st.select_slider("Select page to study closely:", options=range(1, num_pages + 1), value=1)
    
    current_img = all_images[page_number - 1]
    st.image(current_img, caption=f"Page {page_number}", width=400)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📖 Explain Only Page {page_number}"):
            with st.spinner(f"Reading Page {page_number}..."):
                response = model.generate_content(["Explain this specific page in simple Hinglish.", current_img])
                st.info(response.text)
    with col2:
        if st.button(f"🎮 Page {page_number} Quick Quiz"):
            with st.spinner("Generating quick question..."):
                response = model.generate_content(["Ask 1 MCQ from this specific page.", current_img])
                st.success(response.text)

else:
    st.info("👋 Rutvi! Please ask Papa to upload your chapter pages.")

st.sidebar.write("---")
st.sidebar.write("Keep studying, Rutvi! ⭐")
