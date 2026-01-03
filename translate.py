import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Translator", layout="centered")

st.title("🇲🇲 Myanmar-English Translator")

# JavaScript ကို သုံးပြီး Browser ရဲ့ Voice စနစ်ကို တိုက်ရိုက်ခေါ်ပါမယ်
voice_js = """
<script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'my-MM'; // မြန်မာစာအတွက်

    function startSpeech() {
        recognition.start();
        document.getElementById("status").innerText = "🎙️ နားထောင်နေပါသည်...";
    }

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        window.parent.postMessage({type: 'voice_input', data: text}, '*');
        document.getElementById("status").innerText = "✅ ပြောလိုက်သည့်စာ: " + text;
    };
</script>
<div style="text-align: center; padding: 10px;">
    <button onclick="startSpeech()" style="padding: 15px 30px; font-size: 18px; border-radius: 10px; background-color: #007bff; color: white; border: none; cursor: pointer;">
        🎙️ စတင်အသံဖမ်းမည်
    </button>
    <p id="status" style="margin-top: 10px; font-weight: bold; color: #555;">ခလုတ်ကို နှိပ်ပြီး စကားပြောပါ</p>
</div>
"""

components.html(voice_js, height=150)

# စာသားရိုက်သည့်နေရာ
if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""

# Browser က ပို့လိုက်တဲ့ အသံစာသားကို ဖမ်းယူခြင်း (Streamlit မှာ ဒါကို အခုလို ဖမ်းလို့မရသေးလို့ Text Input ပဲ အရင်သုံးရအောင်)
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

text_input = st.text_area("ဘာသာပြန်မည့်စာသား (ဤနေရာတွင် Keyboard Voice လည်း သုံးနိုင်သည်)", value=st.session_state.speech_text)

if st.button("Translate & Speak"):
    if text_input:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text_input)
            st.success(f"Result: {translated}")
            
            # အသံထွက်ပေးခြင်း
            tts = gTTS(text=translated, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        except:
            st.error("Error occurred during translation.")
            
