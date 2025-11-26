---
title: Voice Cloning AI
emoji: 🎤
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🎤 Voice Cloning AI

Clone your voice with AI and generate personalized audio!

**Powered by:** ElevenLabs + Groq (Llama 3.1 8B) - Ultra Fast & Economical ⚡💰

## ✨ Features

- 📝 **AI Script Generation**: Get optimized reading texts (Groq Llama 3.1 8B)
- 🎤 **Browser Voice Recording**: Record directly from your browser
- 📁 **File Upload**: Use existing audio files
- 🎭 **Voice Cloning**: Clone voices using ElevenLabs API
- 🔊 **Audio Generation**: Generate speech with your cloned voice

## 💰 Cost-Effective

- **Groq API:** Ultra low-cost ($0.05/$0.08 per million tokens)
- **Ultra Fast:** 840 tokens/second
- **~$1.30 for 10,000 users** - Virtually free!

## 🚀 Quick Start

### Deploy on Hugging Face Spaces (Recommended)

1. **Create a new Space** on [Hugging Face](https://huggingface.co/spaces)
2. Choose **Gradio** as SDK
3. **Upload files:**
   - `app.py`
   - `requirements.txt`
   - `README.md` (this file)

4. **Add secrets** in Settings > Repository secrets:
   - `GROQ_API_KEY` - Get free at [console.groq.com](https://console.groq.com)
   - `ELEVENLABS_API_KEY` - Get at [elevenlabs.io](https://elevenlabs.io)

5. Wait for build (3-5 minutes) → **You're live!** 🎉

See [DEPLOYMENT_HF.md](DEPLOYMENT_HF.md) for detailed instructions.

### Local Usage

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
Create a `.env` file:
```env
GROQ_API_KEY=gsk_your_groq_key_here
ELEVENLABS_API_KEY=sk_your_elevenlabs_key_here
```

3. **Run:**
```bash
python app.py
```
Or double-click `launch_gradio.bat` (Windows)

The app will open at `http://localhost:7861`

## 📖 How to Use

### Step 1: Generate Script (Optional)
Click "🎲 Generate Script with AI" to get an optimized reading text.

### Step 2: Provide Voice Sample

**Option A - Record:**
1. Click the microphone icon
2. Allow browser microphone access
3. Record 10-30 seconds of clear speech

**Option B - Upload:**
1. Click "Upload" tab
2. Upload your audio file (.wav, .mp3, etc.)

### Step 3: Clone & Generate
1. Name your cloned voice
2. Enter text to generate
3. Click "🚀 Clone Voice & Generate Audio!"
4. Wait 10-30 seconds
5. Listen to the result and download!

## 💡 Tips for Better Cloning

- 🎙️ Use a quality microphone
- 🤫 Record in a quiet environment
- 🗣️ Speak naturally and clearly
- ⏱️ Record at least 10-15 seconds
- 📝 Vary sounds and intonations

## 🔑 API Keys

### Groq API (Script Generation) - FREE
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Generate API key (free, no credit card)

**Model:** Llama 3.1 8B Instant
**Cost:** $0.05 input / $0.08 output per million tokens
**Speed:** 840 tokens/second

### ElevenLabs API (Voice Cloning)
1. Go to [elevenlabs.io](https://elevenlabs.io)
2. Sign up
3. Get API key from settings

**Note:** ElevenLabs has a free tier!

## 📁 Project Structure

```
voice_cloning/
├── app.py                  # Main Gradio app (Groq-powered)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── DEPLOYMENT_HF.md       # Detailed deployment guide
├── launch_gradio.bat      # Windows launcher
├── .env                   # Environment variables (local only, not on HF)
├── .gitignore            # Git ignore file
└── temp_audio/           # Temporary audio files
```

## 🛠️ Tech Stack

- **Gradio 4.0+** - Web interface
- **ElevenLabs** - Professional voice cloning
- **Groq (Llama 3.1 8B)** - Fast & economical AI script generation
- **LangChain** - LLM orchestration

## ⚠️ Requirements

- Valid Groq API key (free)
- Valid ElevenLabs API key
- Python 3.10+
- Modern web browser with microphone access

## 🐛 Troubleshooting

### App won't start
```bash
pip install --upgrade -r requirements.txt
```

### Missing API keys
Check secrets on Hugging Face or `.env` file locally

### Recording not working
- Allow microphone access in browser
- Or use file upload instead

### "Module not found" error
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📊 Performance

- **Script generation:** ~1-2 seconds (Groq)
- **Voice cloning:** ~5-10 seconds (ElevenLabs)
- **Audio generation:** ~5-15 seconds (ElevenLabs)
- **Total time:** ~15-30 seconds per generation

## 💰 Cost Estimation

For **10,000 users** generating 1 script each:
- Groq API: ~$1.30
- ElevenLabs: Depends on your plan

**Groq is virtually free!** 🎉

## 📄 License

MIT License - Free to use and modify

## 🔗 Links

- [Groq Console](https://console.groq.com) - Get free API key
- [ElevenLabs](https://elevenlabs.io) - Voice cloning service
- [Gradio Documentation](https://gradio.app/docs/)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)

## 🙏 Acknowledgments

- **ElevenLabs** for professional voice cloning technology
- **Groq** for ultra-fast and economical AI inference
- **Gradio** for the amazing web interface framework
- **LangChain** for LLM orchestration

---

<div align="center">

**Built with ❤️ using Open Source AI**

Ready for Hugging Face Spaces 🚀 | Ultra Fast ⚡ | Economical 💰

[Deploy Now](https://huggingface.co/spaces) | [Get Help](https://github.com/yourusername/voice-cloning-ai/issues)

</div>
