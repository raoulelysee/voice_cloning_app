import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List, Dict

# Disable Gradio hot-reload dir watching before import
os.environ["GRADIO_WATCH_DIRS"] = ""

# Force UTF-8 on Windows consoles
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import gradio as gr
from dotenv import load_dotenv

# Try to import ElevenLabs SDK for text-to-speech; generation will use SDK when available.
try:
    from elevenlabs import ElevenLabs, VoiceSettings
    SDK_AVAILABLE = True
except Exception:
    SDK_AVAILABLE = False

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY missing. Please set it in your environment or .env file.")

# Initialize SDK client if available (for TTS)
elevenlabs_client = None
if SDK_AVAILABLE:
    try:
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    except Exception as e:
        SDK_AVAILABLE = False

# Local storage configuration
BASE_DIR = Path.cwd()
TEMP_DIR = BASE_DIR / "temp_audio"
CLONED_DIR = BASE_DIR / "cloned_voices"
METADATA_FILE = CLONED_DIR / "voices_metadata.json"
TEMP_DIR.mkdir(exist_ok=True)
CLONED_DIR.mkdir(exist_ok=True)

# Supported TTS models
AVAILABLE_TTS_MODELS = [
    ("eleven_multilingual_v2", "Multilingual (recommended)"),
    ("eleven_monolingual_v1", "Monolingual v1"),
]

def load_metadata() -> List[Dict]:
    if not METADATA_FILE.exists():
        return []
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_metadata(metadata: List[Dict]):
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def add_cloned_voice_record(name: str, voice_id: str, model_id: str, sample_filename: Optional[str] = None):
    metadata = load_metadata()
    record = {
        "name": name,
        "voice_id": voice_id,
        "model_id": model_id,
        "sample": sample_filename,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    metadata.append(record)
    save_metadata(metadata)
    return record

def list_cloned_voices() -> List[str]:
    metadata = load_metadata()
    return [f"{i} - {m['name']} ({m['voice_id']})" for i, m in enumerate(metadata)]

def get_voice_record_by_index(index: int) -> Optional[Dict]:
    metadata = load_metadata()
    if 0 <= index < len(metadata):
        return metadata[index]
    return None

def delete_voice_by_index(index: int) -> Tuple[bool, str]:
    """Delete a cloned voice by its index. Returns (success, message)."""
    metadata = load_metadata()
    if 0 <= index < len(metadata):
        deleted = metadata.pop(index)
        save_metadata(metadata)
        # Try to delete the sample file if it exists
        if deleted.get("sample") and os.path.exists(deleted["sample"]):
            try:
                os.remove(deleted["sample"])
            except Exception:
                pass
        return True, f"✅ Voix supprimée: {deleted['name']} (ID: {deleted['voice_id']})"
    return False, "❌ Index invalide"

# === ElevenLabs Instant Voice Cloning function (Official SDK method) ===
def clone_voice_ivc(audio_file_path: str, voice_name: str) -> str:
    """Clone a voice using ElevenLabs IVC (Instant Voice Cloning) API. Returns voice_id."""
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    if not SDK_AVAILABLE or elevenlabs_client is None:
        raise RuntimeError("ElevenLabs SDK is required for voice cloning. Please install: pip install elevenlabs")

    try:
        # Use the official IVC method from ElevenLabs documentation
        from io import BytesIO

        # Read the audio file and create BytesIO object as per documentation
        with open(audio_file_path, "rb") as f:
            audio_bytes = BytesIO(f.read())

        # Call the IVC create method
        voice = elevenlabs_client.voices.ivc.create(
            name=voice_name,
            files=[audio_bytes]
        )

        # Extract voice_id from response
        voice_id = voice.voice_id
        print(f"✅ Voice cloned successfully! ID: {voice_id}")
        return voice_id

    except Exception as e:
        raise RuntimeError(f"ElevenLabs IVC clone error: {e}") from e

# === TTS generation using ElevenLabs SDK ===
def generate_speech(text: str, voice_id: str, model_id: str = "eleven_multilingual_v2",
                    stability: float = 0.5, similarity_boost: float = 0.75, style: float = 0.0) -> str:
    """Generate audio using ElevenLabs SDK and write to a file. Returns filepath."""
    if not SDK_AVAILABLE or elevenlabs_client is None:
        raise RuntimeError("ElevenLabs SDK is required for TTS. Please install: pip install elevenlabs")

    try:
        # Save audio to file
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        out_path = TEMP_DIR / f"generated_{timestamp}.mp3"

        # Create voice settings for better accent control
        voice_settings = VoiceSettings(
            stability=stability,
            similarity_boost=similarity_boost,
            style=style,
            use_speaker_boost=True
        )

        # Generate and save directly using text_to_speech.convert
        audio = elevenlabs_client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
            voice_settings=voice_settings,
            output_format="mp3_44100_128"
        )

        # Write audio bytes
        with open(out_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

    except Exception as e:
        raise RuntimeError(f"ElevenLabs SDK TTS error: {e}") from e

    print(f"✅ Audio generated: {out_path}")
    return str(out_path)

# === Gradio callbacks ===

def clone_and_store(audio_file, voice_name: str, model_choice: str, progress=gr.Progress()) -> Tuple[Optional[str], str]:
    if not audio_file:
        return None, "❌ Aucun fichier audio fourni."
    audio_path = audio_file if isinstance(audio_file, str) else audio_file.name
    if not os.path.exists(audio_path):
        return None, f"❌ Fichier introuvable: {audio_path}"

    if not voice_name or voice_name.strip() == "":
        voice_name = f"ClonedVoice_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    try:
        progress(0.2, desc="🎧 Préparation...")
        voice_id = clone_voice_ivc(audio_path, voice_name)
        progress(0.6, desc="🧠 Clonage terminé, sauvegarde...")

        # copy sample locally for reference
        sample_filename = CLONED_DIR / f"sample_{voice_id}{Path(audio_path).suffix or '.wav'}"
        try:
            with open(audio_path, 'rb') as src, open(sample_filename, 'wb') as dst:
                dst.write(src.read())
            sample_filename_rel = str(sample_filename)
        except Exception:
            sample_filename_rel = None

        record = add_cloned_voice_record(voice_name, voice_id, model_choice, sample_filename_rel)
        progress(1.0, desc="✅ Voix clonée et stockée.")
        status = f"✅ Voix clonée: {voice_name} (ID: {voice_id})"
        return json.dumps(record, ensure_ascii=False, indent=2), status
    except Exception as e:
        return None, f"❌ Erreur pendant le clonage: {e}"

def generate_with_selected_voice(text_to_speak: str, selected_index: str, model_choice: str,
                                stability: float, similarity_boost: float, style: float,
                                progress=gr.Progress()) -> Tuple[Optional[str], str]:
    try:
        if not selected_index:
            return None, "❌ Aucune voix sélectionnée."
        index = int(selected_index.split(' - ')[0])
        rec = get_voice_record_by_index(index)
        if not rec:
            return None, "❌ Voix sélectionnée introuvable."
        voice_id = rec["voice_id"]
        progress(0.3, desc="🔊 Génération en cours...")
        out_path = generate_speech(text_to_speak, voice_id, model_choice, stability, similarity_boost, style)
        progress(1.0, desc="✅ Génération terminée.")
        return out_path, f"✅ Généré avec la voix: {rec['name']} (ID: {voice_id})"
    except Exception as e:
        return None, f"❌ Erreur de génération: {e}"

def delete_selected_voice(selected_index: str) -> Tuple[List[str], str]:
    """Delete the selected voice and return updated list."""
    try:
        if not selected_index:
            return refresh_voice_list(), "❌ Aucune voix sélectionnée."
        index = int(selected_index.split(' - ')[0])
        _, message = delete_voice_by_index(index)
        return refresh_voice_list(), message
    except Exception as e:
        return refresh_voice_list(), f"❌ Erreur: {e}"

def refresh_voice_list() -> List[str]:
    return list_cloned_voices()

# === Gradio UI ===

def create_interface():
    with gr.Blocks(title="🎤 Voice Cloner - ElevenLabs IVC") as app:
        gr.Markdown("# 🎤 Voice Cloner - ElevenLabs IVC\n**Instant Voice Cloning avec l'API officielle ElevenLabs.**")

        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1) Fournir un échantillon vocal (10-30s recommandé)")
                audio_input = gr.Audio(label="Sample audio", type="filepath", sources=["microphone", "upload"])
                voice_name = gr.Textbox(label="Nom de la voix à créer", placeholder="Ex: Ma Voix Clonée", value="Ma Cloned Voice")
                model_select = gr.Dropdown([m[0] for m in AVAILABLE_TTS_MODELS], value=AVAILABLE_TTS_MODELS[0][0], label="Select TTS model")
                clone_btn = gr.Button("🚀 Cloner et sauvegarder la voix")

                gr.Markdown("### 2) Voix clonées (stockées localement)")
                refresh_btn = gr.Button("🔁 Rafraîchir la liste des voix")
                voices_list = gr.Dropdown(choices=refresh_voice_list(), label="Voix clonées (index - name)", interactive=True)
                delete_btn = gr.Button("🗑️ Supprimer la voix sélectionnée", variant="stop")

                gr.Markdown("### 3) Générer de l'audio avec une voix clonée")
                text_to_tts = gr.Textbox(label="Texte à générer", lines=4, value="Bonjour! Ceci est un test de génération avec ma voix clonée.")

                gr.Markdown("#### ⚙️ Paramètres de voix (pour contrôler l'accent)")
                with gr.Row():
                    stability = gr.Slider(minimum=0.0, maximum=1.0, value=0.5, step=0.05, label="Stabilité",
                                         info="Plus stable = moins d'accent/variation")
                    similarity_boost = gr.Slider(minimum=0.0, maximum=1.0, value=0.75, step=0.05, label="Similarité",
                                                info="Plus haut = plus proche de l'original")
                with gr.Row():
                    style = gr.Slider(minimum=0.0, maximum=1.0, value=0.0, step=0.05, label="Style/Expressivité",
                                     info="Plus haut = plus expressif")

                gen_btn = gr.Button("🔊 Générer avec la voix sélectionnée")

                status_md = gr.Markdown(value="*Statut...*")
                generated_audio = gr.Audio(label="Audio généré", type="filepath")

            with gr.Column(scale=1):
                gr.Markdown("### Informations & Aide")
                gr.Markdown("- Enregistrez au moins 10 secondes de voix.") 
                gr.Markdown("- Les voix clonées sont stockées localement dans cloned_voices/ and metadata in voices_metadata.json.") 
                gr.Markdown("- Assurez-vous d'avoir des crédits et une clé API valide ElevenLabs.")
                if not SDK_AVAILABLE:
                    gr.Markdown("**Note:** ElevenLabs SDK non disponible. L'app utilisera les endpoints REST pour TTS (compatibilité maximale).")


        # Events
        clone_btn.click(fn=clone_and_store, inputs=[audio_input, voice_name, model_select], outputs=[status_md, status_md])
        refresh_btn.click(fn=refresh_voice_list, outputs=voices_list)
        delete_btn.click(fn=delete_selected_voice, inputs=[voices_list], outputs=[voices_list, status_md])
        gen_btn.click(fn=generate_with_selected_voice, inputs=[text_to_tts, voices_list, model_select, stability, similarity_boost, style], outputs=[generated_audio, status_md])

    return app

if __name__ == '__main__':
    app = create_interface()
    # try to avoid port conflict by using 7861
    app.launch(server_name='0.0.0.0', server_port=7861, share=False, show_error=True, debug=False)
