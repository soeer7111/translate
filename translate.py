import streamlit as st
from google import genai
from gtts import gTTS
import base64
import io

# ၁။ API Configuration (SDK အသစ်ပုံစံ)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("Secrets ထဲမှာ API Key ကို အရင်စစ်ဆေးပါ Bro!")

st.set_page_config(page_title="AI Gemini 3 Translator", page_icon="⚡")
st.title("⚡ AI Translator (Gemini 3 Flash)")

# ဘာသာစကားစာရင်း
LANGS = {
    'Myanmar': 'my', 
    'English': 'en', 
    'Thai': 'th', 
    'Korean': 'ko', 
    'Japanese': 'ja', 
    'Chinese': 'zh-CN'
}

to_lang_name = st.selectbox("ဘာသာပြန်မည့် ဘာသာစကားကို ရွေးပါ -", list(LANGS.keys()))
text_in = st.text_area("ဘာသာပြန်ချင်သည့် စာသားကို ဒီမှာ ရိုက်ထည့်ပါ...", height=150)

# ၂။ ဘာသာပြန်ခြင်း လုပ်ဆောင်ချက်
if st.button("AI ဖြင့် ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('Gemini 3 က စဉ်းစားနေပါသည်...'):
                # Colab မှာ အောင်မြင်ခဲ့တဲ့ gemini-3-flash-preview ကို သုံးပါမယ်
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=f"Translate the following text to {to_lang_name} naturally. Only output the translated text: {text_in}"
                )
                
                res_text = response.text.strip()
                
                # ရလဒ်ပြသခြင်း
                st.subheader("ဘာသာပြန်ရလဒ် -")
                st.success(res_text)
                
                # ၃။ အသံထွက် (TTS)
                dest_code = LANGS[to_lang_name]
                tts = gTTS(text=res_text, lang=dest_code)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                # Audio Autoplay လုပ်ခြင်း
                b64 = base64.b64encode(fp.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                st.audio(fp)
                
        except Exception as e:
            # 429 Quota ပြည့်ရင် ပြမယ့်စာသား
            if "429" in str(e):
                st.error("Gemini 3 က Preview ဖြစ်လို့ အခုခဏ Quota ပြည့်သွားပါပြီ။ ၁ မိနစ်လောက် စောင့်ပြီး ပြန်နှိပ်ပေးပါ Bro။")
            else:
                st.error(f"Error: {e}")
    else:
        st.warning("ဘာသာပြန်ဖို့ စာသား အရင်ရိုက်ပါဦး Bro ရေ")
        
