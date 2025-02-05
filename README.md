# Translate Bot for World Discord Server

Built with discord.py and DeepL's translation API, this bot makes it super easy to translate messages on the fly.

## What Can It Do?

- **Quick Translation**: Right-click any message, go to Apps > "Translate", and pick your target language from a dropdown menu.
- **Smart Auto-Translation**: Use Apps > "Auto-Translate" to instantly translate messages to your preferred language.
- **Personal Preferences**: Set your go-to language with `/set-language` - the bot remembers it for future auto-translations.
- **Private Responses**: All translations are sent as private messages, keeping your chat clean.

## Setting It Up

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your tokens:
```
DISCORD_TOKEN=your-discord-bot-token
DEEPL_API_KEY=your-deepl-api-key
TRANSLATOR_ROLE=set-role
```

3. Run the bot:
```bash
python bot.py
```

## Using the Bot

1. **Manual Translation**
   - Right-click any message
   - Select Apps > "Translate"
   - Pick your target language
   - Get your translation!

2. **Auto-Translation**
   - Set your preferred language with `/set-language`
   - Right-click messages and use Apps > "Auto-Translate"
   - The bot detects the language and translates it to your preferred one

3. **Permissions**
   - Users need the "Translator" role (or whatever you set in .env) to use translation features

## Supported Languages
[DeepL Supported Languages](https://developers.deepl.com/docs/zh/resources/supported-languages?utm_term=&utm_campaign=SE%7CPMAX%7CC%7CEnglish&utm_source=google&utm_medium=paid&hsa_acc=1083354268&hsa_cam=21579551002&hsa_grp=&hsa_ad=&hsa_src=x&hsa_tgt=&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=CjwKCAiAtYy9BhBcEiwANWQQL4e7Q8ia5O9_ikiz19WoX0gpPJsb4yVIept0hp78qFxD4xnCvf_dvBoCWaMQAvD_BwE)
