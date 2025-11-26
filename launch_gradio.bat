@echo off
echo ============================================
echo   Lancement de l'application Gradio
echo   Voice Cloning AI
echo ============================================
echo.

cd /d "%~dp0"

echo Verification de l'environnement...
python test_setup.py

echo.
echo Lancement de l'application Gradio...
echo.
echo L'application sera accessible dans votre navigateur
echo URL: http://localhost:7861
echo.
echo Appuyez sur Ctrl+C pour arreter l'application
echo.

python app.py

pause
