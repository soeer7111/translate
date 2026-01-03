import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import io

# ၁။ API Configuration
# Streamlit Secrets ထဲမှာ GEMINI_API_KEY ဆိုတဲ့ နာမည်နဲ့ Key ထည့်ထားရပါမယ်
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Gemini 1.5 Flash က Free ပေးသုံးတာ ပိုများပြီး ပိုငြိမ်ပါတယ်
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key မတွေ့ပါ။ Secrets ထဲမှာ GEMINI_API_KEY ကို သေချာထည့်ပေးပါ။")

# ၂။ UI Design
st.set_page_config(page_title="AI Smart Translator", page_icon="🌍")
st.title("🌍 AI Smart Translator")
st.write("Gemini 1.5 Flash ကို အသုံးပြု၍ ဘာသာပြန်ပေးနေပါသည်")

# ဘာသာစကား ရွေးချယ်မှု
LANGS = {
    'Myanmar': 'my', 
    'English': 'en', 
    'Thai': 'th', 
    'Korean': 'ko', 
    'Japanese': 'ja', 
    'Chinese': 'zh-CN'
}

to_lang_name = st.selectbox("ဘာသာပြန်မည့် ဘာသာစကားကို ရွေးပါ -", list(LANGS.keys()))

# စာရိုက်သည့်အကွက်
text_in = st.text_area("ဘာသာပြန်ချင်သည့် စာသားကို ဒီမှာ ရိုက်ထည့်ပါ...", height=150)

# ၃။ ဘာသာပြန်သည့် လုပ်ဆောင်ချက်
if st.button("AI ဖြင့် ဘာသာပြန်မည်"):
    if text_in:
        try:
            with st.spinner('AI က စဉ်းစားနေပါသည်...'):
                # Prompt ကို ပိုကောင်းအောင် ရေးထားပါသည်
                prompt = f"You are a professional translator. Translate the following text into {to_lang_name} naturally. Only output the translated text: {text_in}"
                
                response = model.generate_content(prompt)
                res_text = response.text.strip()
                
                # ရလဒ်ပြသခြင်း
                st.subheader("ရလဒ် -")
                st.success(res_text)
                
                # Copy ကူးရန် လွယ်ကူစေရန်
                st.text_input("စာသားကို Copy ကူးရန် -", value=res_text)
                
                # ၄။ အသံထွက် (Audio)
                dest_code = LANGS[to_lang_name]
                tts = gTTS(text=res_text, lang=dest_code)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                # Audio ကို Base64 အဖြစ် ပြောင်း၍ Autoplay လုပ်ခြင်း
                b64 = base64.b64encode(fp.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                st.audio(fp)
                
        except Exception as e:
            # Quota ပြည့်လျှင် သေချာပြသပေးမည်
            if "429" in str(e):
                st.error("တစ်နေ့တာ အခမဲ့ ဘာသာပြန်နိုင်သည့် အကြိမ်ရေ ပြည့်သွားပါပြီ။ ၁ မိနစ်လောက် စောင့်ပြီးမှ ပြန်စမ်းကြည့်ပါ သို့မဟုတ် API Key အသစ် လဲပေးပါ။")
            else:
                st.error(f"Error တစ်ခု ဖြစ်ပွားနေပါသည်- {e}")
    else:
        st.warning("ဘာသာပြန်ရန် စာသား အရင်ရိုက်ပါဦး Bro")
        
