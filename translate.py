import streamlit as st
from google import genai
from gtts import gTTS
import base64
import io
from PIL import Image

# ၁။ API Configuration
try:
    # API Key ကို secrets ထဲက ယူမယ်
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("API Key config Error! Secrets ထဲမှာ သေချာပြန်စစ်ပါ Bro။")

st.set_page_config(page_title="AI Pro Hub", page_icon="⚡", layout="wide")

# CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #6200ea; color: white; height: 3em; }
    .result-box { padding: 20px; border-radius: 15px; background-color: #f0f2f6; border-left: 5px solid #6200ea; }
    </style>
    """, unsafe_allow_html=True)

def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except: pass

st.title("⚡ barbar Ai translate")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}
tab1, tab2 = st.tabs(["📝 Text Translation", "🖼️ Image Scan"])

# Colab မှာ အလုပ်လုပ်တာ သေချာတဲ့ Model
MODEL_ID = "gemini-3-flash-preview"

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("Target Language", list(LANGS.keys()))
        input_text = st.text_area("Source Text", height=150)
    
    if st.button("✨ Translate Now"):
        if input_text:
            with st.spinner("AI စဉ်းစားနေသည်..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=f"Translate to {target_lang}: {input_text}"
                    )
                    res = response.text.strip()
                    st.markdown(f'<div class="result-box"><b>Result:</b><br>{res}</div>', unsafe_allow_html=True)
                    st.code(res)
                    play_audio(res, LANGS[target_lang])
                except Exception as e:
                    if "429" in str(e):
                        st.warning("⚠️ Gemini 3 Quota ပြည့်သွားပါပြီ။ ၁ မိနစ်လောက် စောင့်ပေးပါဦး။")
                    else:
                        st.error(f"Error: {e}")

with tab2:
    target_img = st.selectbox("Translate To (Image)", list(LANGS.keys()))
    file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    if file:
        img = Image.open(file)
        st.image(img, width=300)
        if st.button("🔍 Scan Image"):
            with st.spinner("Scanning..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=["Extract and translate text to " + target_img, img]
                    )
                    res = response.text.strip()
                    st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)
                    st.code(res)
                    play_audio(res, LANGS[target_img])
                except Exception as e:
                    st.error(f"Error: {e}")
                    
