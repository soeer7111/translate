import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64
from pydub import AudioSegment

st.title("🇲🇲 Myanmar-English Translator")

if 'text_to_translate' not in st.session_state:
    st.session_state.text_to_translate = ""

st.write("အသံဖြင့် ပြောဆိုရန် ခလုတ်ကို နှိပ်ပါ")
audio_data = mic_recorder(start_prompt="🎙️ စတင်အသံဖမ်းမည်", stop_prompt="🛑 ရပ်တန့်မည်", key='recorder')

if audio_data:
    try:
        # Browser ကလာတဲ့ အသံကို pydub နဲ့ WAV format ပြောင်းခြင်း
        audio_bytes = audio_data['bytes']
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        
        # Speech to Text လုပ်ငန်းစဉ်
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)
            spoken_text = r.recognize_google(audio, language='my-MM')
            st.session_state.text_to_translate = spoken_text
            st.success(f"ပြောလိုက်သည့်စာသား: {spoken_text}")
    except Exception as e:
        st.error("အသံဖမ်းယူရာတွင် အမှားရှိနေပါသည် (သို့မဟုတ်) စကားသံမကြားရပါ။")

# စာရိုက်သည့်နေရာ
text_input = st.text_area("ဘာသာပြန်မည့်စာသား", value=st.session_state.text_to_translate)

if st.button("Translate & Speak"):
    if text_input:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text_input)
            st.success(f"ဘာသာပြန်ရလဒ်: {translated}")
            
            # အသံထွက်ပေးခြင်း
            tts = gTTS(text=translated, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        except:
            st.error("ဘာသာပြန်၍ မရပါ")
            
