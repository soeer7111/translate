import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

st.set_page_config(page_title="AI Translator", layout="centered")
st.title("🇲🇲 AI Translator (Dual Way)")

# ဘာသာစကား ရွေးချယ်ရန်
option = st.selectbox(
    "ဘာသာပြန်မည့် ပုံစံကို ရွေးပါ",
    ("မြန်မာ > English", "English > မြန်မာ")
)

# စာသားရိုက်ရန်
text_input = st.text_area("ဘာသာပြန်မည့် စာသားကို ဤနေရာတွင် ရိုက်ပါ (သို့မဟုတ်) Keyboard Voice ကို သုံးပါ")

if st.button("ဘာသာပြန်မည်"):
    if text_input:
        try:
            # ရွေးချယ်မှုအလိုက် Source နဲ့ Target ကို သတ်မှတ်ခြင်း
            if option == "မြန်မာ > English":
                src_lang, dest_lang = 'my', 'en'
            else:
                src_lang, dest_lang = 'en', 'my'
            
            # ဘာသာပြန်ခြင်း
            translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text_input)
            
            st.success(f"ရလဒ် ({dest_lang}): {translated}")
            
            # အသံထွက်ပေးခြင်း
            # မြန်မာလိုဆိုရင် lang='my'၊ အင်္ဂလိပ်ဆိုရင် lang='en' ဖြစ်ရပါမယ်
            tts = gTTS(text=translated, lang=dest_lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("ဘာသာပြန်၍ မရပါ။ စာသားမှန်ကန်မှုကို စစ်ဆေးပါ။")
    else:
        st.warning("စာသား အရင်ရိုက်ပေးပါခင်ဗျာ။")
        
