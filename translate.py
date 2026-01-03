import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

# Page Config
st.set_page_config(page_title="AI Smart Translator", page_icon="🌍")

# UI Design
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 18px !important; border-radius: 10px !important; }
    .result-box {
        padding: 20px; background-color: #f0f2f6; border-radius: 10px;
        border-left: 5px solid #007bff; font-size: 20px; color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Smart AI Translator")
st.write("ဘာသာစကားအစုံကို Error မရှိဘဲ မြန်မြန်ဆန်ဆန် ဘာသာပြန်ပေးပါသည်")

LANGS = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    from_l = st.selectbox("From", ["auto"] + list(LANGS.keys()))
with col2:
    to_l = st.selectbox("To", list(LANGS.keys()), index=1)

text_in = st.text_area("စာသားရိုက်ပါ...", height=150)

if st.button("ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('ဘာသာပြန်နေပါသည်...'):
                # API Key မလိုသော Engine ကို သုံးခြင်း
                src = from_l if from_l == "auto" else LANGS[from_l]
                dest = LANGS[to_l]
                
                translated = GoogleTranslator(source=src, target=dest).translate(text_in)
                
                if translated:
                    st.subheader("ရလဒ် -")
                    st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)
                    
                    # Copy ယူရန် အကွက်
                    st.text_input("Copy ယူရန် (စာသားကို ဖိနှိပ်ပါ)", value=translated)
                    
                    # အသံထွက် (TTS)
                    tts = gTTS(text=translated, lang=dest)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    b64 = base64.b64encode(fp.read()).decode()
                    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                    st.audio(fp)
        except Exception as e:
            st.error("အင်တာနက် အဆင်မပြေပါ သို့မဟုတ် Error တစ်ခုရှိနေပါသည်။")
    else:
        st.warning("စာသား အရင်ရိုက်ပါ")
