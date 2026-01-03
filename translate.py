import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

# Page Configuration
st.set_page_config(page_title="AI Translator", page_icon="🌐", layout="centered")

# Custom CSS & Copy Function
st.markdown("""
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert("စာသားကို Copy ကူးလိုက်ပါပြီ!");
        });
    }
    </script>
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #008DFF;
        color: white;
        font-weight: bold;
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

# ဘာသာစကား စာရင်း
LANGUAGES = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("မှ (From)", ["Auto Detect"] + list(LANGUAGES.keys()))
with col2:
    target_lang = st.selectbox("သို့ (To)", list(LANGUAGES.keys()), index=1)

text_to_translate = st.text_area("ဘာသာပြန်မည့်စာသားကို ရိုက်ပါ...", height=120)

if st.button("Translate Now"):
    if text_to_translate:
        try:
            src = 'auto' if source_lang == "Auto Detect" else LANGUAGES[source_lang]
            dest = LANGUAGES[target_lang]
            
            translated = GoogleTranslator(source=src, target=dest).translate(text_to_translate)
            
            # Result Display
            st.markdown(f"""
                <div class="result-container">
                    <p style="color: #666;">ဘာသာပြန်ရလဒ် ({target_lang}):</p>
                    <h3 id="result_text">{translated}</h3>
                </div>
            """, unsafe_allow_html=True)

            # Copy Button (Using Streamlit Button with Logic)
            st.button("📋 Copy Translation", on_click=lambda: st.write(f"ကူးယူထားသောစာ: {translated}"))
            st.info("အပေါ်က စာသားကို ဖိပြီးလည်း Copy ကူးနိုင်ပါတယ်")

            # Text to Speech
            tts = gTTS(text=translated, lang=dest)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
            st.audio(fp, format="audio/mp3")

        except Exception as e:
            st.error("Error: ဘာသာပြန်၍ မရပါ။")
            
