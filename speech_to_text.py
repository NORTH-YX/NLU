"""
Este módulo se encarga de convertir archivos de audio en texto usando Whisper.
Puede ser utilizado para transcribir mensajes de voz antes de pasarlos al modelo de lenguaje.
"""

import whisper
import os
import subprocess

import tempfile
import whisper

def transcribe_audio(audio_file, language="es"):
    """
    Transcribe un archivo de audio recibido como FileStorage.
    
    Args:
        audio_file: Archivo subido (Flask FileStorage).
        language: Idioma para la transcripción (default "es").
        
    Returns:
        str: Texto transcrito o mensaje de error en caso de fallo.
    """
    temp_file_path = None
    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            audio_file.save(tmp.name)
            temp_file_path = tmp.name

        # Cargar el modelo (ajusta el modelo si es necesario)
        model = whisper.load_model("base")
        
        # Realizar la transcripción usando la ruta del archivo temporal
        result = model.transcribe(temp_file_path, language=language)
        transcript = result['text']
        return transcript
    except Exception as e:
        # Capturar cualquier error durante la transcripción y retornar un mensaje amigable
        return f"Error during transcription: {str(e)}"
    finally:
        # Eliminar el archivo temporal si fue creado
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def convert_ogg_to_wav(input_path: str, output_path: str) -> None:
    """
    Convierte archivos .ogg (formato típico de Telegram) a .wav usando ffmpeg.
    Este paso es necesario porque algunos modelos de Whisper requieren .wav o .mp3.
    """
    try:
        subprocess.run(["ffmpeg", "-y", "-i", input_path, output_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise RuntimeError("❌ Error al convertir audio. Asegúrate de que ffmpeg esté instalado.")


def transcribe_telegram_ogg(ogg_path: str) -> str:
    """
    Flujo completo para transcribir un archivo de voz descargado de Telegram (.ogg).
    Convierte el archivo a .wav y luego lo transcribe.
    """
    wav_path = ogg_path.replace(".ogg", ".wav")
    convert_ogg_to_wav(ogg_path, wav_path)
    return transcribe_audio(wav_path)

# ✅ Ejemplo de uso:
# text = transcribe_telegram_ogg("notas/audio.ogg")
# print(text)  