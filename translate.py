import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

st.set_page_config(page_title="AI Translator", layout="centered")
st.title("🇲🇲 AI Translator (Myanmar-English)")

# App ရှင်းလင်းအောင် စာသားရိုက်ပြီး ဘာသာပြန်တဲ့စနစ်ကိုပဲ အာရုံစိုက်ပါမယ်
st.info("အသံဖြင့် ဘာသာပြန်ရန် ဖုန်း Keyboard ရှိ Microphone (🎙️) ကို အသုံးပြုပေးပါခင်ဗျာ။")

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# Input Section
option = st.selectbox("ဘာသာပြန်မည့်ပုံစံ", ["မြန်မာ > English", "English > မြန်မာ"])
text_input = st.text_area("ဘာသာပြန်မည့်စာသားကို ဒီမှာရိုက်ပါ (သို့) Keyboard Voice သုံးပါ")

if st.button("ဘာသာပြန်မည်"):
    if text_input:
        try:
            # ဘာသာပြန်ခြင်း
            src, dest = ('my', 'en') if option == "မြန်မာ > English" else ('en', 'my')
            translated = GoogleTranslator(source=src, target=dest).translate(text_input)
            st.session_state.translated_text = translated
            
            st.success(f"ရလဒ်: {translated}")
            
            # အသံထွက်ပေးခြင်း
            tts = gTTS(text=translated, lang=dest)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("ဘာသာပြန်ရာတွင် အမှားရှိနေပါသည်။ အင်တာနက်ကို စစ်ဆေးပေးပါ။")
    else:
        st.warning("စာသား အရင်ရိုက်ပေးပါ")
