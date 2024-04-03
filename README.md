# kibernikto-planner

Basic telegram AI planner. Can use voice messages.  
Can be updated to retrieve plans etc, just a demo functionality for now.
Reminds of planned messages.
Uses [Kibernikto library](https://github.com/solovieff/kibernikto) as a core and is mostly here to show it's
capabilities.

Mostly a set of tools and extended Kibernikto bots.

<img width="526" alt="image" src="https://github.com/solovieff/kibernikto-planner/assets/5033247/c3801b89-fa7f-4840-963b-db1a1c439214">


**run code**
(assuming you set the environment yrself)

Install the requirements  
`pip install -r requirements.txt`  
Run `main.py` file using the environment provided.

**Minimal Environment**

```dotenv
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXX
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_MODEL=gpt-4-turbo-preview
#OPENAI_API_MODEL=gpt-4
#OPENAI_API_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=850
OPENAI_MAX_MESSAGES=5
OPENAI_TEMPERATURE=0.1

VOICE_PROCESSOR=openai
VOICE_FILE_LOCATION=/tmp
VOICE_OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXX
VOICE_OPENAI_API_MODEL=whisper-1
VOICE_OPENAI_API_BASE_URL=https://api.openai.com/v1

TG_REACTION_CALLS=["hi","hola", "plan", "schedule"]
TG_STICKER_LIST=["CAACAgIAAxkBAAELx29l_2OsQzpRWhmXTIMBM4yekypTOwACdgkAAgi3GQI1Wnpqru6xgTQE"]
TG_BOT_KEY=XXXXXXXXXX:XXXxxxXXXxxxxXXXxxx
TG_MASTER_ID=XXXXXXXXX
TG_SAY_HI=true
TG_CHUNK_SENTENCES=5

```
