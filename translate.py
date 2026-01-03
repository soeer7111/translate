import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# --- ဤနေရာတွင် Bro ယူထားသော API Key ကို ထည့်ပါ ---
API_KEY = "AIzaSyB407uCt2nb6ym3s0iOFXXKi2Y5g28Cuo4"
# -------------------------------------------

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Gemini AI Translator", page_icon="💎")

st.markdown("""
    <style>
    .result-box { padding: 20px; background-color: #f0f4f8; border-radius: 15px; border: 1px solid #007bff; color: #000; font-size: 18px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Gemini AI Translator")
st.write("Google ရဲ့ အဆင့်မြင့် Gemini AI ကို အသုံးပြုထားပါတယ်")

target_lang = st.selectbox("ဘာသာပြန်မည့် ဘာသာစကား", ["English", "Myanmar", "Thai", "Korean", "Japanese"])

text_input = st.text_area("ဘာသာပြန်မည့် စာသားကို ရိုက်ပါ...", height=150)

if st.button("AI ဖြင့် ဘာသာပြန်မည်"):
    if text_input:
        try:
            with st.spinner('Gemini AI က စဉ်းစားနေပါသည်...'):
                # Gemini ကို ဘာသာပြန်ခိုင်းခြင်း
                prompt = f"Translate the following text to {target_lang}. Return only the translated text: {text_input}"
                response = model.generate_content(prompt)
                translated = response.text

                st.subheader("ဘာသာပြန်ရလဒ် -")
                st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)
                
                # Copy ရလွယ်အောင် ထည့်ပေးထားခြင်း
                st.text_input("Copy ယူရန် ဤနေရာတွင် ဖိနှိပ်ပါ", value=translated)

                # အသံထွက်ပေးခြင်း
                lang_code = {'English': 'en', 'Myanmar': 'my', 'Thai': 'th', 'Korean': 'ko', 'Japanese': 'ja'}
                tts = gTTS(text=translated, lang=lang_code[target_lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                b64 = base64.b64encode(fp.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                st.audio(fp)

        except Exception as e:
            st.error("API Key မှားနေသည် (သို့မဟုတ်) အင်တာနက် မကောင်းပါ။")
    else:
        st.warning("စာသား အရင်ရိုက်ပါ")
        
        
