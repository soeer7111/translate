import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

# Page Configuration
st.set_page_config(page_title="Global AI Translator", page_icon="🌐", layout="centered")

# Custom CSS for Modern UI
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #008DFF;
        color: white;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .result-container {
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Global AI Translator")
st.write("ဘာသာစကားပေါင်းစုံကို အသံထွက်နဲ့တကွ ဘာသာပြန်ပေးပါသည်")

# ဘာသာစကား စာရင်း
LANGUAGES = {
    'Myanmar': 'my',
    'English': 'en',
    'Thai': 'th',
    'Korean': 'ko',
    'Japanese': 'ja',
    'Chinese': 'zh-CN',
    'French': 'fr',
    'Russian': 'ru'
}

# Language Selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("မှ (From)", ["Auto Detect"] + list(LANGUAGES.keys()))
with col2:
    target_lang = st.selectbox("သို့ (To)", list(LANGUAGES.keys()), index=1)

# Input
text_to_translate = st.text_area("ဘာသာပြန်မည့်စာသားကို ရိုက်ပါ...", height=150)

if st.button("Translate Now"):
    if text_to_translate:
        try:
            with st.spinner('AI က ဘာသာပြန်ပေးနေပါသည်...'):
                # Translator Logic
                src = 'auto' if source_lang == "Auto Detect" else LANGUAGES[source_lang]
                dest = LANGUAGES[target_lang]
                
                translator = GoogleTranslator(source=src, target=dest)
                translated = translator.translate(text_to_translate)
                
                # Show Result
                st.markdown(f"""
                <div class="result-container">
                    <p style="color: #666; font-size: 0.9em;">ဘာသာပြန်ရလဒ် ({target_lang}):</p>
                    <h2 style="color: #333;">{translated}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Text to Speech
                tts = gTTS(text=translated, lang=dest)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                b64 = base64.b64encode(fp.read()).decode()
                
                # Audio Control
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                st.audio(fp, format="audio/mp3")
                
        except Exception as e:
            st.error("ခဏနေမှ ပြန်ကြိုးစားပါ (သို့မဟုတ်) စာသားကို စစ်ဆေးပါ။")
    else:
        st.warning("ဘာသာပြန်ဖို့ စာသားအရင်ရိုက်ပါ")

st.info("💡 အကြံပြုချက် - ဖုန်း keyboard က Microphone (🎙️) ကိုသုံးပြီး အသံနဲ့ စာရိုက်နိုင်ပါတယ်")
