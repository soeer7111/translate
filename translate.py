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
st.set_page_config(page_title="Gemini Pro Hub", page_icon="📸", layout="wide")

# CSS & JavaScript for Copy Function
st.markdown("""
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Copied to clipboard!');
        });
    }
    </script>
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; font-weight: bold; }
    .result-area { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 10px; color: #333; font-size: 1.1em; }
    </style>
    """, unsafe_allow_html=True)

# Autoplay Audio Function
def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_bytes = fp.read()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"TTS Error: {e}")

st.title("🤣barlar barlar AI Translator😂")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}
tab1, tab2, tab3 = st.tabs(["📝 Text", "📁 File", "🖼️ Image Scan"])

# --- TAB 1: Text ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        target_t = st.selectbox("Target Language", list(LANGS.keys()), key="t1")
        input_t = st.text_area("Source Text", height=150)
        btn_t = st.button("Translate Text ✨")
    
    if btn_t and input_t:
        with st.spinner("Translating..."):
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=f"Translate to {target_t}: {input_t}"
            )
            res = response.text.strip()
            
            st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
            
            # Copy Button (Using Streamlit Button with Code placeholder)
            st.code(res, language=None)
            st.info("အပေါ်ကစာသားကို ကလစ်နှစ်ချက်နှိပ်ပြီး Copy ယူနိုင်သလို၊ အောက်က Audio ကိုလည်း နားထောင်နိုင်ပါတယ်")
            
            play_audio(res, LANGS[target_t])

# --- TAB 3: Image Scan ---
with tab3:
    target_i = st.selectbox("Target Language", list(LANGS.keys()), key="t3")
    img_file = st.file_uploader("စာသားပါသော ပုံကို တင်ပါ...", type=['jpg', 'jpeg', 'png'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Uploaded Image", width=300)
        
        if st.button("Scan & Translate 🔍"):
            with st.spinner("AI is reading and translating..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=["Read and translate to " + target_i + " naturally. Only result text.", img]
                )
                res = response.text.strip()
                
                st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
                st.code(res, language=None)
                
                play_audio(res, LANGS[target_i])

st.divider()
st.caption("Powered by Gemini 3 & Streamlit")
    
