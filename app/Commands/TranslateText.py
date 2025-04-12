import json

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.utils.LLMrequest import LLMrequest


class TranslateText(Command):
    language = "PL"
    prompt = f"не указывай на ошибки,не добавляй своего, ты google translate,не допускай грамматических ошибок," \
             f"переведи следующий текст на %s \nтекст:"

    def __init__(self, body_json):
        print("CommandExtractTitle")

        self.body_json = body_json


    def execute(self) -> Feedback:
        command_entity = json.loads(self.body_json)
        pur = command_entity['purpose']
        user = command_entity['id']
        payload = json.loads(command_entity["payload"])
        text=payload['text']
        language=payload['language']
        # Теперь используем синглтон для запроса к GPT
        llm_request = LLMrequest()  # Получаем существующий экземпляр синглтона
        prompt=self.prompt % language
        title = llm_request.translate_text(prompt, payload=text, languageAnswer=language)


        feed = Feedback(payload=title, ID_of_text=user, purpose=pur)
        print(f"RECIEVE TO CommandExtractTitle {self.body_json}")
        return feed


