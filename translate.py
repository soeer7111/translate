import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# Secrets မှ API Key ကို ယူခြင်း
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Error 404 ကို ကျော်လွှားရန် Stable ဖြစ်သော gemini-pro ကို သုံးပါမည်
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"API Key ထည့်သွင်းမှု မှားယွင်းနေပါသည်: {e}")

st.set_page_config(page_title="AI Pro Translator", page_icon="🤖")

st.title("🤖 Pro AI Translator (Stable Version)")

LANGS = {
    'Myanmar': 'my', 'English': 'en', 'Thai': 'th', 
    'Korean': 'ko', 'Japanese': 'ja', 'Chinese': 'zh-CN'
}

col1, col2 = st.columns(2)
with col1:
    from_l = st.selectbox("From", ["Auto Detect"] + list(LANGS.keys()))
with col2:
    to_l = st.selectbox("To", list(LANGS.keys()), index=1)

text_in = st.text_area("စာသားရိုက်ပါ...", height=150)

if st.button("AI ဖြင့် ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('AI စဉ်းစားနေပါသည်...'):
                prompt = f"Professional translation to {to_l}. Output only the translated text: {text_in}"
                
                response = model.generate_content(prompt)
                res = response.text.strip()
                
                st.subheader("ဘာသာပြန်ရလဒ် -")
                # စာသားကို Copy ကူးရလွယ်အောင် text_area နှင့် ပြပေးခြင်း
                st.text_area("ရလဒ် (Copy ကူးနိုင်သည်)", value=res, height=100)
                
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
            st.info("အကယ်၍ 404 ဆက်တက်နေပါက API Key အသစ်ပြန်ယူပြီး Reboot လုပ်ပေးပါ Bro")
    else:
        st.warning("စာသား အရင်ရိုက်ပါ")
        
