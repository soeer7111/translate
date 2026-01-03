import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

# Page Config
st.set_page_config(page_title="AI Translator", page_icon="🌐")

# Custom UI
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 18px !important; }
    .translated-text { 
        padding: 15px; 
        background-color: #f0f2f6; 
        border-radius: 10px; 
        border-left: 5px solid #008DFF;
        font-size: 20px;
        color: #1f1f1f;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Global AI Translator")

# ဘာသာစကားရွေးချယ်မှု
LANGUAGES = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From", ["Auto Detect"] + list(LANGUAGES.keys()))
with col2:
    target_lang = st.selectbox("To", list(LANGUAGES.keys()), index=1)

# Input
text_to_translate = st.text_area("စာသားရိုက်ပါ...", height=150)

if st.button("Translate Now"):
    if text_to_translate:
        try:
            src = 'auto' if source_lang == "Auto Detect" else LANGUAGES[source_lang]
            dest = LANGUAGES[target_lang]
            
            # ဘာသာပြန်ခြင်း
            translated = GoogleTranslator(source=src, target=dest).translate(text_to_translate)
            
            # ၁။ ဘာသာပြန်ထားတဲ့ စာသားကို ရှင်းရှင်းလင်းလင်း ပြပေးခြင်း
            st.subheader(f"ရလဒ် ({target_lang}):")
            st.markdown(f'<div class="translated-text">{translated}</div>', unsafe_allow_html=True)

            # ၂။ Copy ကူးရန် ခလုတ် (Streamlit ရဲ့ code block ကို သုံးရင် copy ကူးရတာ ပိုလွယ်ပါတယ်)
            st.code(translated, language=None)
            st.caption("အပေါ်က အကွက်ထဲက စာသားကို ညာဘက်ထောင့်က icon လေးနှိပ်ပြီး Copy ကူးနိုင်ပါတယ်။")

            # ၃။ အသံထွက်ပေးခြင်း
            tts = gTTS(text=translated, lang=dest)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
            st.audio(fp, format="audio/mp3")

        except Exception as e:
            st.error("ဘာသာပြန်ရာတွင် အမှားရှိနေပါသည်။")
    else:
        st.warning("စာသား အရင်ရိုက်ပါ")
        
