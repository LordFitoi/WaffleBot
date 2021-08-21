import discord

from models.corpus import Corpus
from models.chatbot import Chatbot
from models.mixins import DiscordCommandsMixin

class Client(discord.Client, DiscordCommandsMixin):
    def __init__(self, **kargs):
        super().__init__()
        self.config = kargs.get("config")
        self.main_path = kargs.get("main_path")
        self.chatbot = Chatbot(
            Corpus(self.config.get("CorpusName")))

        self.commands = {
            ".": self.chat,
        }

    async def eval_commands(self, message: str) -> None:
        command, arguments = self.is_Command(message)

        if command and command in self.commands:
            await self.commands[command](message, arguments)
            self.log_Message(message)

    async def on_ready(self) -> None:
        print(f"@ Logged as {self.user}")

    async def on_message(self, message: object) -> None:
        if not message.author.bot and not self.is_DMChannel(message):
            await self.eval_commands(message)