import os
import json
from pathlib import Path
import discord
from discord import app_commands
from discord.ui import Select, View
from dotenv import load_dotenv
import deepl
import asyncio

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
    '🇦🇪 Arabic': 'AR',
    '🇨🇳 Chinese (simplified)': 'ZH-HANS',
    '🇹🇼 Chinese (traditional)': 'ZH-HANT',
    '🇺🇸 English': 'EN-US',
    '🇫🇷 French': 'FR',
    '🇩🇪 German': 'DE',
    '🇯🇵 Japanese': 'JA',
    '🇵🇹 Portuguese': 'PT',
    '🇪🇸 Spanish': 'ES'
}

# STORE LANGUAGE PREFERENCES
class UserPreferences:
    def __init__(self):
        self.file_path = Path('user_preferences.json')
        self.preferences = self.load_preferences()

    def load_preferences(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def save_preferences(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.preferences, f)

    def get_preferred_language(self, user_id: str) -> str:
        return self.preferences.get(str(user_id), 'EN-US')

    def set_preferred_language(self, user_id: str, language: str):
        self.preferences[str(user_id)] = language
        self.save_preferences()

class PreferredLanguageSelect(Select):
    def __init__(self, user_preferences: UserPreferences):
        self.user_preferences = user_preferences
        options = [
            discord.SelectOption(label=name, value=code)
            for name, code in LANGUAGES.items()
        ]
        super().__init__(
            placeholder="Choose your preferred language:",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selected_lang = self.values[0]
        self.user_preferences.set_preferred_language(str(interaction.user.id), selected_lang)
        await interaction.response.send_message(
            f"Your preferred language has been set to {selected_lang}",
            ephemeral=True
        )

class PreferredLanguageView(View):
    def __init__(self, user_preferences: UserPreferences):
        super().__init__()
        self.add_item(PreferredLanguageSelect(user_preferences))

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
        self.user_preferences = UserPreferences()
        self.translator = deepl.Translator(DEEPL_API_KEY)

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

        # REGISTER THE AUTO-TRANSLATION CONTEXT MENU COMMAND
        @self.tree.context_menu(name="Auto-Translate")
        async def auto_translate_message(interaction: discord.Interaction, message: discord.Message):
            if not any(role.name == TRANSLATOR_ROLE for role in interaction.user.roles):
                await interaction.response.send_message(
                    "You do not have permission to use this command.",
                    ephemeral=True
                )
                return

            try:
                target_lang = self.user_preferences.get_preferred_language(str(interaction.user.id))
                result = self.translator.translate_text(
                    message.content,
                    target_lang=target_lang
                )
                
                source_lang = result.detected_source_lang
                await interaction.response.send_message(
                    f"Translation ({source_lang} → {target_lang}): {result.text}",
                    ephemeral=True
                )
                
            except Exception as e:
                print(f"Auto-translation error: {e}")
                await interaction.response.send_message(
                    "An error occurred while translating the message.",
                    ephemeral=True
                )

        # REGISTER THE SET PREFERRED LANGUAGE COMMAND
        @self.tree.command(name="set-language", description="Set your preferred language for auto-translation")
        async def set_preferred_language(interaction: discord.Interaction):
            if not any(role.name == TRANSLATOR_ROLE for role in interaction.user.roles):
                await interaction.response.send_message(
                    "You do not have permission to use this command.",
                    ephemeral=True
                )
                return

            view = PreferredLanguageView(self.user_preferences)
            await interaction.response.send_message(
                "Select your preferred language for auto-translation:",
                view=view,
                ephemeral=True
            )

        # SYNC COMMANDS WITH DISCORD YO
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} AUTHORIZED (ID: {self.user.id})')
        await asyncio.sleep(0)
        print('\033[91m....15%\033[0m')  
        await asyncio.sleep(1)
        print('\033[93m....30%\033[0m')  
        await asyncio.sleep(0)
        print('\033[38;5;208m....60%\033[0m')  
        await asyncio.sleep(1)
        print('\033[92m....90%\033[0m')  
        await asyncio.sleep(0)
        print('\033[32m....100%\033[0m')  
        await asyncio.sleep(1)
        print('\033[32;1mBOT ONLINE\033[0m')  

def main():
    # CREATE INSTANCE
    client = TranslatorBot()
    
    # RUN OPERATION
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()