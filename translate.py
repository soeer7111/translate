import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# Secrets မှ API Key ကို ယူခြင်း
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # v1beta 404 error ကင်းဝေးစေရန် models/prefix ကို သုံးထားပါသည်
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error("Secrets ထဲမှာ API Key ကို 'GEMINI_API_KEY' ဆိုတဲ့ နာမည်နဲ့ သေချာထည့်ပေးပါ Bro")

# UI Settings
st.set_page_config(page_title="Pro AI Translator", page_icon="💎")
st.title("💎 Pro AI Translator")

LANGS = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    to_lang_name = st.selectbox("ဘာသာပြန်မည့်ဘာသာ (To)", list(LANGS.keys()))

text_in = st.text_area("ဒီမှာ စာရိုက်ပါ...", height=150)

if st.button("AI ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('AI က စဉ်းစားနေပါသည်...'):
                # AI ကို ပိုမိုကျွမ်းကျင်စွာ ဘာသာပြန်ခိုင်းမည့် Prompt
                prompt = f"You are an expert translator. Translate the following text into {to_lang_name} naturally and accurately. Only output the translated text: {text_in}"
                
                response = model.generate_content(prompt)
                translated_text = response.text.strip()
                
                if translated_text:
                    st.subheader("ရလဒ် -")
                    st.success(translated_text)
                    
                    # Copy ယူရန် အကွက်
                    st.text_input("Copy ယူရန် (Long Press)", value=translated_text)
                    
                    # အသံထွက် (TTS)
                    dest_code = LANGS[to_lang_name]
                    tts = gTTS(text=translated_text, lang=dest_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    b64 = base64.b64encode(fp.read()).decode()
                    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                    st.audio(fp)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("ဘာသာပြန်ဖို့ စာသားအရင်ရိုက်ပါ")
        
