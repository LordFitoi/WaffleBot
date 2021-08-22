from random import choice

from models.dataset import Dataset
from models.classifiers import IntentClassifier
from models.mixins import CommandsMixin


class Chatbot(IntentClassifier, CommandsMixin):
    def __init__(self, corpus):
        dataset = Dataset(corpus.data)
        super().__init__(dataset)

        self.replies = dataset.replies
        self.patterns = dataset.patterns

        # Here you will add the command that will call the intent
        self.callbacks = {
            "GetTime": self.get_time,
            "DoMath":  self.do_math,
            "RepeatUser": self.repeat_user
        }

    def get_error_message(self, label):
        warning = choice(self.replies[f"Error"])
        error = choice(self.replies[f"Error{label}"]) 
        
        return f"{warning} {error}"

    def chat(self, context):
        label = self.predict(context)

        response = ""
         
        if label != "NoContext":
            response = choice(self.replies[label])
            response = self.callbacks[label](response, label, context)

        return response
