import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    with open("output.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_bytes=True)

st.title("🇲🇲 Myanmar-English AI Translator")

option = st.selectbox("ဘာသာပြန်မည့် ပုံစံကို ရွေးပါ", 
                     ("English to Myanmar", "Myanmar to English"))

text_input = st.text_area("စာသားကို ဤနေရာတွင် ရိုက်ပါ (သို့မဟုတ်) Voice Typing သုံးပါ")

if st.button("Translate & Speak"):
    if text_input:
        src, dest = ('en', 'my') if option == "English to Myanmar" else ('my', 'en')
        translated = GoogleTranslator(source=src, target=dest).translate(text_input)
        
        st.success(f"ရလဒ်: {translated}")
        
        # အသံထွက်ပေးခြင်း
        text_to_speech(translated, dest)
    else:
        st.warning("စာသား အရင်ရိုက်ပေးပါခင်ဗျာ")
      
