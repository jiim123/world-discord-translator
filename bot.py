import os
import discord
from discord import app_commands
from discord.ui import Select, View
from dotenv import load_dotenv
import deepl

# ////////////////////////////////////////////////////////
# TBOT IS MADE SPECIFICALLY FOR THE WORLD DISCORD SERVER.
# CREATED BY JIM (WORLDID: JIIM#0001) + (DISCORD: JIIM)
# ////////////////////////////////////////////////////////

# LETS START
# LOAD ENVIRONMENT VARIABLES
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
TRANSLATOR_ROLE = os.getenv('TRANSLATOR_ROLE')

# AVAILABLE LANGUAGES FOR TRANSLATION
LANGUAGES = {
    '🇺🇸 English': 'EN-US',
    '🇦🇪 Arabic': 'AR',
    '🇩🇪 German': 'DE',
    '🇫🇷 French': 'FR',
    '🇪🇸 Spanish': 'ES',
    '🇮🇹 Italian': 'IT',
    '🇳🇱 Dutch': 'NL',
    '🇵🇱 Polish': 'PL',
    '🇵🇹 Portuguese': 'PT',
    '🇷🇺 Russian': 'RU',
    '🇯🇵 Japanese': 'JA',
    '🇨🇳 Chinese (simplified)': 'ZH-HANS',
    '🇹🇼 Chinese (traditional)': 'ZH-HANT'
}

class LanguageSelect(Select):
    def __init__(self, message_content: str):
        self.message_to_translate = message_content
        options = [
            discord.SelectOption(label=name, value=code)
            for name, code in LANGUAGES.items()
        ]
        super().__init__(
            placeholder="Choose a language:",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        target_lang = self.values[0]
        
        try:
            # INITIALIZE DEEPL TRANSLATOR
            translator = deepl.Translator(DEEPL_API_KEY)
            
            # TRANSLATE THE USER MESSAGE
            result = translator.translate_text(
                self.message_to_translate,
                target_lang=target_lang
            )
            
            # SEND TRANSLATION AS EPHEMERAL MESSAGE
            await interaction.response.send_message(
                f"Translation ({target_lang}): {result.text}",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Translation error: {e}")
            await interaction.response.send_message(
                "An error occurred while translating the message.",
                ephemeral=True
            )

class LanguageView(View):
    def __init__(self, message_content: str):
        super().__init__()
        self.add_item(LanguageSelect(message_content))

class TranslatorBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # REGISTER THE CONTEXT MENU COMMAND
        @self.tree.context_menu(name="Translate")
        async def translate_message(interaction: discord.Interaction, message: discord.Message):
            # CHECK IF USER HAS THE REQUIRED ROLE
            if not any(role.name == TRANSLATOR_ROLE for role in interaction.user.roles):
                await interaction.response.send_message(
                    "You do not have permission to use this command.",
                    ephemeral=True
                )
                return

            # LANGUAGE SELECTION VIEW
            view = LanguageView(message.content)
            await interaction.response.send_message(
                "Select the target language for translation:",
                view=view,
                ephemeral=True
            )

        # SYNC COMMANDS WITH DISCORD YO
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} INITIATED (ID: {self.user.id})')
        print('beep boop')

def main():
    # CREATE BOT INSTANCE
    client = TranslatorBot()
    
    # KICK IT OFF
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()