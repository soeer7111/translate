import streamlit as st
from google import genai
from gtts import gTTS
import base64
import io
from PIL import Image
from st_copy_to_clipboard import st_copy_to_clipboard

# ၁။ API Configuration
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("API Key မတွေ့ပါ။")

# UI Styling
st.set_page_config(page_title="Gemini Pro Vision Hub", page_icon="📸", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; font-weight: bold; }
    .result-area { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 10px; color: #333; font-size: 1.1em; }
    </style>
    """, unsafe_allow_html=True)

# Autoplay Function
def autoplay_audio(audio_fp):
    audio_bytes = audio_fp.read()
    b64 = base64.b64encode(audio_bytes).decode()
    md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(md, unsafe_allow_html=True)

# Main App
st.title("😂 barlar barlar AI Translator😂")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}
tab1, tab2, tab3 = st.tabs(["📝 Text", "📁 File", "🖼️ Image Scan"])

def translate_ai(content, target_lang, is_image=False):
    try:
        if is_image:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["ပုံထဲကစာသားတွေကိုဖတ်ပြီး " + target_lang + " ဘာသာပြန်ပေးပါ။ ရလဒ်စာသားပဲပေးပါ။", content]
            )
        else:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=f"Translate to {target_lang} naturally: {content}"
            )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- TAB 1: Text ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        target_t = st.selectbox("Target Language", list(LANGS.keys()), key="t1")
        input_t = st.text_area("Source Text", height=150)
        btn_t = st.button("Translate Text ✨")
    
    if btn_t and input_t:
        res = translate_ai(input_t, target_t)
        st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
        
        # Copy Button ထည့်သွင်းခြင်း
        st_copy_to_clipboard(res, before_text="📋 Copy", after_text="✅ Copied!")
        
        tts = gTTS(res, lang=LANGS[target_t])
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        autoplay_audio(fp)

# --- TAB 3: Image Scan ---
with tab3:
    target_i = st.selectbox("Target Language", list(LANGS.keys()), key="t3")
    img_file = st.file_uploader("စာသားပါသော ပုံကို တင်ပါ...", type=['jpg', 'jpeg', 'png'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Uploaded Image", width=300)
        
        if st.button("Scan & Translate 🔍"):
            with st.spinner("AI is reading the image..."):
                res = translate_ai(img, target_i, is_image=True)
                st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
                
                # Copy Button ထည့်သွင်းခြင်း
                st_copy_to_clipboard(res, before_text="📋 Copy Result", after_text="✅ Copied to Clipboard!")
                
                tts = gTTS(res, lang=LANGS[target_i])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                autoplay_audio(fp)

st.divider()
st.caption("Powered by Gemini 3 & Streamlit")
