import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64

st.title("🇲🇲 Myanmar-English Translator")

# အသံဖမ်းယူသည့်အပိုင်း
st.write("အသံဖြင့် ပြောဆိုရန် ခလုတ်ကို နှိပ်ပါ")
audio_data = mic_recorder(start_prompt="🎙️ စတင်အသံဖမ်းမည်", stop_prompt="🛑 ရပ်တန့်မည်", key='recorder')

# အသံဖမ်းပြီးလျှင် စာသားပြောင်းရန်
if audio_data:
    st.audio(audio_data['bytes'])
    
    # Speech to Text လုပ်ငန်းစဉ်
    r = sr.Recognizer()
    audio_file = io.BytesIO(audio_data['bytes'])
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    
    try:
        # မြန်မာစာအတွက် 'my-MM' သို့မဟုတ် English အတွက် 'en-US'
        # ဒီနေရာမှာ Auto Detect လုပ်ဖို့ခက်လို့ မြန်မာစာလို့ပဲ အရင်သတ်မှတ်ပါမယ်
        spoken_text = r.recognize_google(audio, language='my-MM')
        st.session_state.text_to_translate = spoken_text
        st.success(f"ပြောလိုက်သည့်စာသား: {spoken_text}")
    except:
        st.error("အသံကို စာသားအဖြစ် ပြောင်းမရပါ၊ ထပ်မံကြိုးစားပါ သို့မဟုတ် ကိုယ်တိုင်ရိုက်ထည့်ပါ။")

# ဘာသာပြန်သည့်အပိုင်း
text_input = st.text_area("ဘာသာပြန်မည့်စာသား", value=st.session_state.get('text_to_translate', ''))

if st.button("Translate & Speak"):
    if text_input:
        # ဘာသာပြန်ခြင်း
        translated = GoogleTranslator(source='auto', target='en').translate(text_input)
        st.success(f"ဘာသာပြန်ရလဒ်: {translated}")
        
        # အသံထွက်ပေးခြင်း
        tts = gTTS(text=translated, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
      
