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
    st.error("API Key မတွေ့ပါ။ Secrets ထဲမှာ GEMINI_API_KEY ကို ထည့်ပေးပါ။")

# UI Styling
st.set_page_config(page_title="Gemini Pro Vision Hub", page_icon="📸", layout="wide")

# Custom CSS for UI
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; font-weight: bold; }
    .result-area { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 10px; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - History
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("📜 History")
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
    for h in reversed(st.session_state.history[-10:]):
        st.caption(f"• {h}")

# Main App
st.title("📸 Barlar😁😁😁😁 AI  Translator")
st.write("Text, Files နှင့် Images များကို AI ဖြင့် တစ်နေရာတည်းတွင် ဘာသာပြန်ပါ")

LANGS = {'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'}

tab1, tab2, tab3 = st.tabs(["📝 Text", "📁 File", "🖼️ Image Scan"])

# Function to handle translation
def translate_ai(content, target_lang, is_image=False):
    try:
        if is_image:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["ဖော်ပြပါပုံထဲက စာသားများကို အကုန်ဖတ်ပြီး " + target_lang + " ဘာသာသို့ အဓိပ္ပာယ်ပြည့်စုံစွာ ပြန်ပေးပါ။ ရလဒ်စာသားပဲ ထုတ်ပေးပါ။", content]
            )
        else:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=f"Translate the following to {target_lang} naturally. Return only translation: {content}"
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
        st.session_state.history.append(f"Text: {res[:20]}...")
        st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
        st.text_input("Copy လုပ်ရန် (Select & Copy)", value=res)
        tts = gTTS(res, lang=LANGS[target_t])
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp)

# --- TAB 2: File ---
with tab2:
    target_f = st.selectbox("Target Language", list(LANGS.keys()), key="t2")
    file = st.file_uploader("Upload Text File (.txt)", type=['txt'])
    if file and st.button("Translate File 🚀"):
        content = file.getvalue().decode("utf-8")
        res = translate_ai(content[:5000], target_f)
        st.markdown(f'<div class="result-area">{res}</div>', unsafe_allow_html=True)
        st.download_button("Download Translated File", res, file_name="translated.txt")

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
                st.text_input("Copy Result:", value=res, key="img_res")
                try:
                    tts = gTTS(res, lang=LANGS[target_i])
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp)
                except: pass

st.divider()
st.caption("Powered by Gemini 3 Flash & 1.5 Flash Vision")
        
