# Miaw-bot
Un pequeño agente que funcione de forma más segura que OpenClaw

# Como instalar
## 1. Crear el entorno virtual (llamado 'venv')
python -m venv .venv

## 2. Activarlo
Windows: .venv\Scripts\activate

macOS/Linux: source .venv/bin/activate

## 3. Instalar los requisitos
pip install -r requirements.txt

## Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

## Instalar dependencias usando UV
uv sync

## Instalar como comando en tu terminal
uv tool install .

## Lanzar el bot
escribe miaw-bot desde tu terminal e iniciará el espacio de chat en terminal. (si tienes ollama en local)
escribe miaw-bot --ip X.X.X.X, para iniciarlo definiendo la ip del equipo donde tienes corriendo ollama.

# Modificar personalidad y forma de responder del bot:
Modifica miaw-bot-personality.md a tu gusto para definir si quieres respuestas con una personalidad especifica para miaw-bot, si quieres respuestas cortas o algo más en cada interacción.
