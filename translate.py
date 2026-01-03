import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# Secrets မှ API Key ကို ယူခြင်း
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # 404 Error မတက်စေရန် နာမည်အပြည့်အစုံသုံးပါ
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"API Configuration Error: {e}")

st.set_page_config(page_title="AI Pro Translator", page_icon="🤖")

st.title("🤖 Pro AI Translator (Gemini)")

LANGS = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    from_l = st.selectbox("မူရင်း (From)", ["Auto Detect"] + list(LANGS.keys()))
with col2:
    to_l = st.selectbox("ပြန်မည့်ဘာသာ (To)", list(LANGS.keys()), index=1)

text_in = st.text_area("စာသားရိုက်ပါ...", height=150)

if st.button("AI ဖြင့် ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('AI က စဉ်းစားနေပါသည်...'):
                prompt = f"Professional translation: Translate this to {to_l}. Output only translated text: {text_in}"
                
                response = model.generate_content(prompt)
                res = response.text.strip()
                
                st.subheader("ဘာသာပြန်ရလဒ် -")
                st.info(res)
                
                # Copy Box (စာသားကို Select ပေးပြီး ကူးယူနိုင်ရန်)
                st.text_input("Copy ယူရန် (Long Press)", value=res)

                # အသံထွက်
                dest_code = LANGS[to_l]
                tts = gTTS(text=res, lang=dest_code)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                b64 = base64.b64encode(fp.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                st.audio(fp)
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("စာသား အရင်ရိုက်ပါ")
        
