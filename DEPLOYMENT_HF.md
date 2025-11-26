# 🚀 Guide de Déploiement sur Hugging Face Spaces

Ce guide vous explique comment déployer votre application de clonage vocal sur Hugging Face Spaces.

## 📋 Prérequis

1. Un compte Hugging Face ([créer un compte](https://huggingface.co/join))
2. Vos clés API:
   - Clé API ElevenLabs ([obtenir ici](https://elevenlabs.io))
   - Clé API OpenAI ([obtenir ici](https://platform.openai.com))

## 🔧 Étape 1: Préparer les fichiers

Vous avez besoin des fichiers suivants (déjà créés):
- `app.py` - L'application Gradio principale
- `requirements_gradio.txt` - Les dépendances Python
- `README_HF.md` - Documentation pour Hugging Face

## 🌐 Étape 2: Créer un Space sur Hugging Face

1. Allez sur [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Cliquez sur **"Create new Space"**
3. Remplissez les informations:
   - **Space name**: `voice-cloning-ai` (ou votre choix)
   - **License**: MIT
   - **Select the Space SDK**: **Gradio**
   - **Space hardware**: CPU basic (gratuit) ou GPU si vous avez un plan payant
4. Cliquez sur **"Create Space"**

## 📤 Étape 3: Uploader les fichiers

### Option A: Via l'interface web

1. Dans votre nouveau Space, cliquez sur **"Files"**
2. Uploadez ces fichiers:
   - `app.py`
   - `requirements_gradio.txt` → renommer en `requirements.txt`
   - `README_HF.md` → renommer en `README.md`

### Option B: Via Git

```bash
# Cloner le repository
git clone https://huggingface.co/spaces/VOTRE_USERNAME/voice-cloning-ai
cd voice-cloning-ai

# Copier les fichiers
cp app.py voice-cloning-ai/
cp requirements_gradio.txt voice-cloning-ai/requirements.txt
cp README_HF.md voice-cloning-ai/README.md

# Commit et push
git add .
git commit -m "Initial commit: Voice cloning app"
git push
```

## 🔐 Étape 4: Configurer les secrets (IMPORTANT!)

1. Dans votre Space, allez dans **"Settings"**
2. Scrollez jusqu'à **"Repository secrets"**
3. Ajoutez vos clés API:

   Cliquez sur **"New secret"** et ajoutez:

   **Secret 1:**
   - Name: `ELEVENLABS_API_KEY`
   - Value: `votre_clé_elevenlabs`

   **Secret 2:**
   - Name: `OPENAI_API_KEY`
   - Value: `votre_clé_openai`

4. Cliquez sur **"Save"** pour chaque secret

## ✅ Étape 5: Vérifier le déploiement

1. Hugging Face va automatiquement builder votre Space
2. Attendez quelques minutes (la première build peut prendre 5-10 minutes)
3. Vous verrez des logs de construction dans l'onglet **"Logs"**
4. Une fois terminé, votre application sera accessible à l'URL:
   ```
   https://huggingface.co/spaces/VOTRE_USERNAME/voice-cloning-ai
   ```

## 🎯 Étape 6: Tester l'application

1. Ouvrez l'URL de votre Space
2. Testez les fonctionnalités:
   - Génération de script
   - Upload d'un fichier audio
   - Clonage et génération

## 🐛 Dépannage

### L'app ne démarre pas
- Vérifiez les logs dans l'onglet "Logs"
- Assurez-vous que les secrets sont bien configurés
- Vérifiez que `requirements.txt` est présent

### Erreur "API Key manquante"
- Vérifiez que vous avez bien ajouté les secrets `ELEVENLABS_API_KEY` et `OPENAI_API_KEY`
- Les noms doivent être EXACTEMENT comme indiqués (majuscules)

### Erreur de mémoire
- Le Space gratuit a des limites de mémoire
- Considérez upgrader vers un Space avec plus de RAM

## 💡 Optimisations

### Rendre l'app publique
Dans **Settings > Visibility**, changez vers **"Public"**

### Ajouter un badge
Ajoutez ce badge dans votre README GitHub:
```markdown
[![Open in Spaces](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue)](https://huggingface.co/spaces/VOTRE_USERNAME/voice-cloning-ai)
```

### Activer le partage
Dans `app.py`, changez `share=False` en `share=True` pour obtenir un lien public temporaire

## 📊 Monitoring

- Surveillez l'utilisation dans le dashboard Hugging Face
- Vérifiez les coûts des API (ElevenLabs et OpenAI)
- Limitez l'accès si nécessaire pour contrôler les coûts

## 🔒 Sécurité

- ⚠️ Ne commitez JAMAIS vos clés API dans le code
- Utilisez toujours les Secrets de Hugging Face
- Considérez ajouter une authentification si vous voulez limiter l'accès

## 📚 Ressources

- [Documentation Gradio](https://gradio.app/docs/)
- [Documentation Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [ElevenLabs API Docs](https://elevenlabs.io/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)

---

Bonne chance avec votre déploiement! 🎉
