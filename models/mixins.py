from datetime import datetime
from re import search


class CommandsMixin:
    """
    This class will have all commands
    """

    def get_time(self, response, *args):
        time = datetime.now()
        time_str = time.strftime("%I:%M%p")

        return response.replace("$TIME", time_str)

    def do_math(self, response, *args):
        label, context = args

        for pattern in self.patterns[label]:
            if match := search(pattern, context.lower()):
                try:
                    expression = match.group(1)
                    evaluation = round(eval(expression), 2)
                    response = response.replace("$EXPR", expression)
                    response = response.replace("$EVAL", str(evaluation))

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
