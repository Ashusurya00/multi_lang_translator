from flask import Flask, render_template, request, jsonify, url_for
from gtts import gTTS, lang as gtts_langs
from deep_translator import GoogleTranslator
import os
import tempfile

app = Flask(__name__)

# Supported languages
all_langs = {
    "English": "en", "Hindi": "hi", "Marathi": "mr", "Tamil": "ta", "Telugu": "te",
    "Gujarati": "gu", "Kannada": "kn", "Malayalam": "ml", "Punjabi": "pa", "Urdu": "ur",
    "Bengali": "bn", "Odia": "or", "Assamese": "as", "Nepali": "ne", "Sinhala": "si",
    "Arabic": "ar", "Persian": "fa", "Hebrew": "he", "Turkish": "tr", "Swahili": "sw",
    "Afrikaans": "af", "Zulu": "zu", "Somali": "so", "French": "fr", "Spanish": "es",
    "German": "de", "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Japanese": "ja",
    "Korean": "ko", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Vietnamese": "vi", "Thai": "th", "Indonesian": "id", "Filipino": "tl", "Malay": "ms"
}

tts_langs = gtts_langs.tts_langs().keys()

def clean_old_audio():
    folder = "static"
    for f in os.listdir(folder):
        if f.endswith(".mp3"):
            try:
                os.remove(os.path.join(folder, f))
            except:
                pass

@app.route("/")
def index():
    return render_template("index_ajax.html", all_langs=all_langs)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    paragraph = data.get("paragraph", "")
    target_lang = data.get("language", "")
    translated_text = ""
    audio_file = None
    warning_msg = None

    if paragraph and target_lang:
        try:
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(paragraph)

            if target_lang in tts_langs:
                clean_old_audio()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts = gTTS(text=translated_text, lang=target_lang)
                    tts.save(tmp.name)
                    tmp_filename = os.path.basename(tmp.name)
                audio_file = tmp_filename
                os.replace(tmp.name, os.path.join("static", audio_file))
            else:
                warning_msg = f"⚠️ Speech not supported for '{target_lang}', showing text only."
        except Exception as e:
            translated_text = f"⚠️ Error: {e}"

    return jsonify({
        "translated_text": translated_text,
        "audio_file": audio_file,
        "warning_msg": warning_msg
    })

if __name__ == "__main__":
    app.run(debug=True)
