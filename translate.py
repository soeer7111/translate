import streamlit as st
from streamlit_mic_recorder import mic_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64

st.title("🇲🇲 Myanmar-English Translator")

# အသံဖမ်းခလုတ်
st.write("အသံဖြင့် ပြောဆိုရန် အောက်က ခလုတ်ကို နှိပ်ပါ")
audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="🛑 Stop Recording", key='recorder')

if audio:
    # ဤနေရာတွင် speech-to-text library တစ်ခုခု ထပ်ပေါင်းရန် လိုပါမည်
    st.audio(audio['bytes'])
    st.info("အသံဖမ်းယူပြီးပါပြီ။ စာသားအဖြစ် ပြောင်းလဲရန် စနစ်ပြင်ဆင်နေဆဲဖြစ်သည်။")

# စာရိုက်ပြီး ဘာသာပြန်သည့်အပိုင်း
text_input = st.text_area("စာသားရိုက်ပါ သို့မဟုတ် Keyboard Voice သုံးပါ")
if st.button("Translate & Speak"):
    if text_input:
        translated = GoogleTranslator(source='auto', target='en').translate(text_input)
        st.success(f"Result: {translated}")
        # အသံထွက်ပေးမည့်အပိုင်း...
      
