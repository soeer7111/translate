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
    st.error("API Key config Error!")

st.set_page_config(page_title="AI Pro Hub", page_icon="⚡", layout="wide")

# Autoplay Audio Function
def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except: pass

st.title("😁barlar barlar AI  Translator😁")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}
tab1, tab2 = st.tabs(["📝 Text Translate", "🖼️ Image Scan"])

# Model ID
MODEL_ID = "gemini-3-flash-preview"

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("Translate To", list(LANGS.keys()))
        input_text = st.text_area("Source Text", height=100)
    
    if st.button("✨ Translate Now"):
        if input_text:
            with st.spinner("Translating..."):
                try:
                    # AI ကို စကားမများဖို့ ဒီမှာ ပိတ်လိုက်ပြီ
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=f"Translate the following text to {target_lang}. Provide ONLY the translated text. Do not include explanations, notes, or phonetic transcriptions: {input_text}"
                    )
                    res = response.text.strip()
                    
                    # Result ပြသခြင်း
                    st.subheader("Result:")
                    st.success(res)
                    st.code(res) # Copy ကူးရ လွယ်အောင်
                    
                    play_audio(res, LANGS[target_lang])
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    target_img = st.selectbox("Translate Image To", list(LANGS.keys()))
    file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    if file:
        img = Image.open(file)
        st.image(img, width=300)
        if st.button("🔍 Scan & Translate"):
            with st.spinner("AI Scanning..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[f"Read the text in this image and translate to {target_img}. Provide ONLY the translated text, no explanation.", img]
                    )
                    res = response.text.strip()
                    st.success(res)
                    st.code(res)
                    play_audio(res, LANGS[target_img])
                except Exception as e:
                    st.error(f"Error: {e}")
                    
