import io
import base64
from gtts import gTTS

def generate_audio_base64(text: str, lang: str = "hi") -> str:
    tts = gTTS(text=text, lang=lang, slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    audio_bytes = fp.read()
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    return f"data:audio/mp3;base64,{base64_audio}"