import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# API Key ကို Secrets မှယူခြင်း
API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini ကို အသေအချာ Configure လုပ်ခြင်း
genai.configure(api_key=API_KEY)

# Model ကို နာမည်အပြည့်အစုံဖြင့် ခေါ်ခြင်း
# နာမည်ကို 'gemini-1.5-flash' လို့ပဲ သုံးပါမယ်
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Smart Translator", page_icon="🤖")

st.title("🤖 Advanced AI Translator")
st.caption("Google Gemini AI ကို အသုံးပြုထားသောကြောင့် ဘာသာပြန် ပိုမိုမှန်ကန်ပါသည်")

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
            with st.spinner('AI က စဉ်းစားနေပါသည်...'):
                # Gemini ကို ခိုင်းမည့် Prompt ကို ပိုကောင်းအောင် ပြင်ထားသည်
                prompt = f"You are a professional translator. Translate the following text to {to_l}. Context: {from_l} to {to_l}. Text: {text_in}. Output ONLY the translated text."
                
                response = model.generate_content(prompt)
                res = response.text.strip()
                
                st.subheader("ဘာသာပြန်ရလဒ်:")
                st.info(res) # စာသားကို အပြာရောင်အကွက်နှင့် ပြပေးမည်
                
                # Copy ယူရန် အကွက်
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
            st.error(f"Error: {str(e)}")
            st.info("API Key သို့မဟုတ် Region ကန့်သတ်ချက် ရှိနေနိုင်ပါသည်။")
            
