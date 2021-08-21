from models.chatbot import Chatbot
from models.corpus import Corpus

VERSION = "0.0.1"

corpus = Corpus("es")
chatbot = Chatbot(corpus)

print(f"WaffleBot Release v{VERSION}")

while True:
    context = input(">> ")
    
    if context.lower() == "exit":
        break

    chatbot.chat(context)