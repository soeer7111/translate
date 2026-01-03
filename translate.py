import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# --- API KEY နေရာ ---
API_KEY = st.secrets["GEMINI_API_KEY"] 
# ------------------

# Gemini Configuration
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("API Configuration မှာ အမှားရှိနေပါတယ်။")

st.set_page_config(page_title="AI Multi-Translator", page_icon="💎")

# UI Styling
st.markdown("""
    <style>
    .result-box { padding: 15px; background-color: #ffffff; border-radius: 10px; border-left: 5px solid #007bff; color: #000; font-size: 18px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Smart AI Multi-Translator")

# ဘာသာစကားစာရင်း (Bro စိတ်ကြိုက်ထပ်တိုးနိုင်သည်)
LANG_LIST = {
    'Myanmar': 'my',
    'English': 'en',
    'Thai': 'th',
    'Korean': 'ko',
    'Japanese': 'ja',
    'Chinese': 'zh-CN',
    'French': 'fr'
}

# Language Selectors (ဒီမှာ From နဲ့ To ကို စိတ်ကြိုက်ရွေးလို့ရအောင် လုပ်ပေးထားပါတယ်)
col1, col2 = st.columns(2)
with col1:
    from_lang = st.selectbox("မူရင်းဘာသာ (From)", ["Auto Detect"] + list(LANG_LIST.keys()))
with col2:
    to_lang = st.selectbox("ဘာသာပြန်မည့်ဘာသာ (To)", list(LANG_LIST.keys()), index=1)

text_input = st.text_area("စာသားရိုက်ပါ (သို့မဟုတ်) Voice Keyboard သုံးပါ...", height=150)

if st.button("AI ဘာသာပြန်မည်"):
    if text_input:
        try:
            with st.spinner('AI စဉ်းစားနေပါသည်...'):
                # Gemini ကို ခိုင်းမည့်စာသား (Prompt)
                prompt = f"Translate the following text from {from_lang} to {to_lang}. Output ONLY the translated text: {text_input}"
                
                response = model.generate_content(prompt)
                translated_text = response.text.strip()

                if translated_text:
                    st.subheader("ဘာသာပြန်ရလဒ်")
                    st.markdown(f'<div class="result-box">{translated_text}</div>', unsafe_allow_html=True)
                    
                    # Copy ရန် အကွက်
                    st.text_input("Copy ယူရန် (Long press to copy)", value=translated_text)

                    # အသံထွက် (TTS)
                    dest_code = LANG_LIST[to_lang]
                    tts = gTTS(text=translated_text, lang=dest_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    b64 = base64.b64encode(fp.read()).decode()
                    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                    st.audio(fp)
                else:
                    st.warning("ဘာသာပြန်လို့ မရပါဘူးခင်ဗျာ။")

        except Exception as e:
            # တကယ်လို့ Error တက်ရင် ဘာကြောင့်လဲဆိုတာ မြင်ရအောင် e ကိုပါ ပြခိုင်းထားပါတယ်
            st.error(f"Error တက်နေပါတယ်: {str(e)}")
            st.info("API Key သေချာထည့်ထားလား ပြန်စစ်ပေးပါ Bro")
    else:
        st.warning("ဘာသာပြန်ဖို့ စာသားအရင်ရိုက်ပါ")
        
