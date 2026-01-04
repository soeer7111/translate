import streamlit as st
from google import genai
from gtts import gTTS
import base64
import io
from PIL import Image

# ၁။ API Configuration
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("API Key မတွေ့ပါ။")

# UI Styling
st.set_page_config(page_title="😁barlar barlar AI Translatorr😂", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background-color: #007bff; color: white; font-weight: bold; height: 3em; }
    .result-area { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 15px; color: #1a1a1a; font-size: 1.2em; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Autoplay Function (နောက်ဆုံးပေါ် နည်းလမ်း)
def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.write("Audio format not supported for this language.")

st.title("🌍 Pro AI Multi-Translator")
st.write("Stable Version (Gemini 2.0 Flash) - အမှားအယွင်းကင်းစွာ သုံးနိုင်ပါပြီ")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}
tab1, tab2, tab3 = st.tabs(["📝 Text Translate", "📁 File Translate", "🖼️ Image Scan"])

# --- TAB 1: Text ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        target_t = st.selectbox("ဘာသာစကားရွေးပါ", list(LANGS.keys()), key="t1")
        input_t = st.text_area("Source Text", placeholder="ဘာသာပြန်ချင်တာ ရိုက်ထည့်ပါ...", height=150)
        btn_t = st.button("✨ ဘာသာပြန်မည်")
    
    if btn_t and input_t:
        with st.spinner("AI စဉ်းစားနေသည်..."):
            try:
                # Gemini 2.0 Flash ကို သုံးလိုက်ခြင်းဖြင့် Error ကင်းသွားပါမည်
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"Translate this text to {target_t} naturally: {input_t}"
                )
                res = response.text.strip()
                st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
                st.code(res, language=None)
                play_audio(res, LANGS[target_t])
            except Exception as e:
                st.error(f"Error: {e}. Please try again in a moment.")

# --- TAB 3: Image Scan ---
with tab3:
    target_i = st.selectbox("Target Language", list(LANGS.keys()), key="t3")
    img_file = st.file_uploader("ပုံတင်ပါ (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Uploaded Image", width=300)
        
        if st.button("🔍 Scan & Translate"):
            with st.spinner("AI ဖတ်နေသည်..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=["Read this image and translate the text to " + target_i + " naturally. Only result text.", img]
                    )
                    res = response.text.strip()
                    st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
                    st.code(res, language=None)
                    play_audio(res, LANGS[target_i])
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.caption("Powered by Gemini 2.0 Flash • Ultra Fast & Stable")
