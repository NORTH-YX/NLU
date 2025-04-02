# ===============================
# 📁 app.py — Flask Microservice
# ===============================

from flask import Flask, request, jsonify
from openai_client import get_action_json
from parser import parse_response, summarize_actions, normalize_actions
from speech_to_text import transcribe_audio

app = Flask(__name__)

# =====================================
# 🔹 Endpoint: Interpret natural language (text)
# =====================================
@app.route("/interpret", methods=["POST"])
def interpret():
    """
    Input JSON: { "input": "natural language instruction" }
    Output JSON: { "actions": [...], "summary": "..." }
    
    NOTA: La validación y resolución de campos faltantes se realizará en el backend Java.
    """
    data = request.get_json()
    user_input = data.get("input", "")

    # Llama a OpenAI para extraer acciones en formato JSON
    json_string = get_action_json(user_input)
    actions = parse_response(json_string)
    actions = normalize_actions(actions)

    # Eliminamos la llamada a prompt_for_missing_info para que la validación
    # se realice en el backend Java.
    return jsonify({
        "actions": actions,
        "summary": summarize_actions(actions)
    })

# =====================================
# 🔹 Endpoint: Transcribe voice input
# =====================================
@app.route("/transcribe", methods=["POST"])
def transcribe():
    """
    Expects audio file (multipart/form-data with key 'audio')
    Returns transcript string.
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400

    audio_file = request.files['audio']
    transcript = transcribe_audio(audio_file)

    return jsonify({"transcription": transcript})

# ======================
# 🔧 Run the service
# ======================
if __name__ == "__main__":
    # For development only — replace with gunicorn in prod
    app.run(debug=True, host="0.0.0.0", port=5000)


# ===============================
# README:
# ===============================
# /interpret   → POST { input: "Crea una tarea..." } → returns structured actions and summary.
# /transcribe  → POST audio file (key=audio)       → returns transcription.
# This microservice converts natural language input into structured actions.
# The Java backend will handle validation and execution of database queries.