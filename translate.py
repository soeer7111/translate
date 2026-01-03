import streamlit as st
from google import genai
from gtts import gTTS
import base64
import io

# API Key ကို Secrets မှယူခြင်း
API_KEY = st.secrets["GEMINI_API_KEY"]

# Client အသစ် တည်ဆောက်ခြင်း
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="AI Pro Translator", page_icon="🤖")
st.title("🤖 Pro AI Translator (Gemini 2.0)")

LANGS = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    to_lang = st.selectbox("To (ဘာသာပြန်မည့်ဘာသာ)", list(LANGS.keys()))

text_in = st.text_area("စာသားရိုက်ပါ...", height=150)

if st.button("AI ဖြင့် ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('AI က စဉ်းစားနေပါသည်...'):
                # Gemini 2.0 Flash ကို အသုံးပြုခြင်း
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Professional translation: Translate this text into {to_lang}. Output only the translated text: {text_in}"
                )
                res = response.text.strip()
                
                st.subheader("ဘာသာပြန်ရလဒ် -")
                st.info(res)
                st.text_input("Copy ယူရန်", value=res)

                # အသံထွက်
                tts = gTTS(text=res, lang=LANGS[to_lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                b64 = base64.b64encode(fp.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                st.audio(fp)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("စာသား အရင်ရိုက်ပါ")
        
