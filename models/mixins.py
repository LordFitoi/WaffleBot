import discord, json

from datetime import datetime
from re import search 
from os.path import join


class UtilsMixin:    
    def is_DMChannel(self, message: str) -> bool:
        return isinstance(message.channel, discord.channel.DMChannel)

    def is_Command(self, message: str) -> list:
        prefix = self.config.get("Prefix")
        content = message.content

        if content.startswith(prefix):
            arguments = content[len(prefix):].lower().split()
            
            if arguments:
                command = arguments.pop(0)
                
                return command, arguments

    def log_Message(self, message: str) -> None: 
        if self.config["DebugMode"]:
            print(f"{message.author} : {message.content}")


class ViewsMixin:
    def load_embed(self, name: str) -> dict:
        """
        Load a embed content from assets/embeds
        """

        dir_path = join(self.main_path, f"assets/embeds")
        path = join(dir_path, f"{name}.json")

        with open(path, "r", encoding = "utf-8") as jsonfile:
            content = json.load(jsonfile)

        return content

    def create_embed(self, embed_data: dict) -> object:
        """
        Create a embed object
        """
        
        body    = embed_data.get("description")
        thumb   = embed_data.get("thumbnail")
        title   = embed_data.get("title")
        content = embed_data.get("content")
        inline  = embed_data.get("inline")
        color   = embed_data.get("color")

        version = self.config.get("Version")
        footer  = f'WaffleBot Release v{version}'

        embed = discord.Embed(
            title = title,
            description = body,
            color = int(color, 16),
        )

        embed.set_thumbnail(url = thumb)

        for key, value in content.items():
            embed.add_field(
                name = key,
                value = value,
                inline = inline
            )
        
        embed.set_footer(text = footer)
        
        return embed


class DiscordCommandsMixin(UtilsMixin, ViewsMixin):
    async def chat(self, message: str, arguments: list):
        context = " ".join(arguments)
        content = self.load_embed("dialog")
        content["description"] = f"`{self.chatbot.chat(context)}`"
        embed = self.create_embed(content)

        await message.channel.send(embed = embed)


class CommandsMixin:
    """
    This class will have all commands
    """

    def get_time(self, response, *args):
        time = datetime.now()
        time_str = time.strftime("%I:%M%p %z")

        return response.replace("$TIME", time_str)

    def do_math(self, response, *args):
        label, context = args

        for pattern in self.patterns[label]:
            if match := search(pattern, context.lower()):
                try:
                    expression = match.group(1)
                    evaluation = round(eval(expression), 2)
                    response   = response.replace("$EXPR", expression)
                    response   = response.replace("$EVAL", str(evaluation))

                except SyntaxError:
                    response = self.get_error_message("Math")
                
                break

        return response

    def repeat_user(self, response, *args):
        label, context = args

        for pattern in self.patterns[label]:
            if match := search(pattern, context.lower()):
                expression = match.group(1).capitalize()
                response = response.replace("$MSG", f'"{expression}"')

                break 
        
        return response
 
