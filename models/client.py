import discord

from models.corpus import Corpus
from models.chatbot import Chatbot
from models.mixins import DiscordCommandsMixin

class Client(discord.Client, DiscordCommandsMixin):
    def __init__(self, **kargs):
        super().__init__()
        self.config = kargs.get("config")
        
        self.main_path = kargs.get("main_path")
        
        self.name = self.config.get("BotName")
        self.chatbot = Chatbot(
            Corpus(self.config.get("CorpusName")))

    async def on_ready(self) -> None:
        print(f"@ Logged as {self.user}")

    async def on_message(self, message: object) -> None:
        if not message.author.bot and not self.is_DMChannel(message):
            if self.is_Mentioned(message):
                await self.chat(message) 
            
            self.log_Message(message)
