import logging
from g4f.client import Client
from functools import lru_cache
from app.interfaces.translator import Translator
from app.utils.logger import get_logger

# Initialize the logger
logger = get_logger('app.LLMrequest')


class LLMrequest(Translator):
    def __init__(self):
        self.client = Client()  # Инициализация клиента для каждого экземпляра
        logger.info("LLMrequest client initialized")

    @lru_cache(maxsize=128)  # Ограничиваем кэш 128 уникальными запросами
    def translate_text(self, prompt: str, payload: str, languageAnswer="PL", model: str = "gpt-4o-mini") -> str:
        # Объединяем prompt и payload
        message_content = f"твоим языком ответа должен быть:{languageAnswer}\n,{prompt}\n{payload}"

        logger.info(f"Preparing translation request with model {model}")
        logger.debug(f"Message content for translation: {message_content}")

        # Отправляем запрос
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message_content}],
                web_search=False
            )
            translated_text = response.choices[0].message.content
            logger.info("Received translation response successfully")
            logger.debug(f"Translated text: {translated_text}")
            return translated_text
        except Exception as e:
            logger.error(f"Error while sending translation request: {str(e)}")
            return f"Error: {str(e)}"

    def clear_cache(self):
        logger.info("Clearing translation cache")
        self.translate_text.cache_clear()
