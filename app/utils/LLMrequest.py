from g4f.client import Client
from functools import lru_cache

from app.interfaces.translator import Translator


class LLMrequest(Translator):
    def __init__(self):
        self.client = Client()  # Инициализация клиента для каждого экземпляра

    @lru_cache(maxsize=128)  # Ограничиваем кэш 128 уникальными запросами
    def translate(self, prompt: str, payload: str, languageAnswer="PL", model: str = "gpt-4o-mini") -> str:
        # Объединяем prompt и payload
        message_content = f"твоим языком ответа должен быть:{languageAnswer}\n,{prompt}\n{payload}"

        # Отправляем запрос
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message_content}],
            web_search=False
        )
        return response.choices[0].message.content

    def clear_cache(self):
        self.translate.cache_clear()



