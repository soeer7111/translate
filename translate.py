import streamlit as st
from google import genai
from gtts import gTTS
import base64
import io
from PIL import Image

# ၁။ API Configuration
# Gemini 3 အတွက် SDK Version က နောက်ဆုံးဖြစ်ဖို့ လိုပါတယ်
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("API Key မတွေ့ပါ။")

# UI Styling
st.set_page_config(page_title="Gemini 3 Pro Hub", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background-color: #6200ea; color: white; font-weight: bold; height: 3.5em; }
    .result-area { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 2px solid #6200ea; color: #1a1a1a; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass

st.title("⚡barlar barlar Ai translate")
st.write("😁😁😁😁😁😁😁😁😁😁")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}
tab1, tab2 = st.tabs(["📝 Smart Translation", "🖼️ Visual Scan"])

# Gemini 3 က Preview ဖြစ်လို့ Model Name ကို ဒီလို အတိအကျ သုံးရပါမယ်
MODEL_ID = "gemini-3-flash-preview"

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        target_t = st.selectbox("Target Language", list(LANGS.keys()), key="t1")
        input_t = st.text_area("Input Text", placeholder="စာရိုက်ပါ...", height=150)
        btn_t = st.button("Generate Translation 🚀")
    
    if btn_t and input_t:
        with st.spinner("Gemini 3 is thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_ID, 
                    contents=f"Translate to {target_t} naturally. Only provide the translation: {input_t}"
                )
                res = response.text.strip()
                st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
                st.code(res)
                play_audio(res, LANGS[target_t])
            except Exception as e:
                # Gemini 3 က Preview ဖြစ်လို့ Quota က အရမ်းနည်းပါတယ်
                if "429" in str(e):
                    st.warning("Gemini 3 Quota Limit ရောက်သွားပါပြီ။ ၁ မိနစ်လောက်စောင့်ပြီး ပြန်စမ်းကြည့်ပါ Bro။")
                else:
                    st.error(f"Error: {e}")

with tab2:
    target_i = st.selectbox("Translate To", list(LANGS.keys()), key="t3")
    img_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400)
        if st.button("AI Scan & Translate 🔍"):
            with st.spinner("Gemini 3 Visual Analysis..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=["Extract and translate text in this image to " + target_i, img]
                    )
                    res = response.text.strip()
                    st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
                    st.code(res)
                    play_audio(res, LANGS[target_i])
                except Exception as e:
                    st.error(f"Error: {e}")

