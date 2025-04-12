import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from prometheus_client import Counter, Summary
import time

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.prompts import prompts
from app.utils import SettingsTMP
from app.utils.LLMrequest import LLMrequest

# Определяем метрики для Prometheus
TRANSLATION_REQUEST_COUNT = Counter('multi_translation_requests_total', 'Total number of translation requests', ['status', 'language'])
TRANSLATION_REQUEST_DURATION = Summary('multi_translation_request_duration_seconds', 'Duration of translation requests in seconds', ['language'])

class MultiTranslate(Command):
    languages = ["polish", "english", "russian"]
    ans_multi_language = []

    def __init__(self, body_json):
        print("CommandExtractTitle")
        self.body_json = body_json

    def process_language(self, language, text, llm_request):
        """Процесс перевода и извлечения заголовка для одного языка."""
        print(f"language: {language}")

        # Обрабатываем время для запроса перевода
        start_time = time.time()

        # Перевод и извлечение заголовка
        prompt = prompts.prompt_extract_title % language.upper()
        title = llm_request.translate_text(prompt, payload=text, languageAnswer=language)

        prompt = prompts.prompt_translate % language.upper()
        translated = llm_request.translate_text(prompt, payload=text, languageAnswer=language)

        # Замеряем время выполнения
        duration = time.time() - start_time
        TRANSLATION_REQUEST_DURATION.labels(language=language).observe(duration)

        # Создаем объект ответа
        tmpjson = {
            "title": title,
            "language": language,
            "message": translated
        }

        # Увеличиваем счетчик успешных запросов
        TRANSLATION_REQUEST_COUNT.labels(status='success', language=language).inc()

        return tmpjson

    def execute(self) -> Feedback:
        print("multi translating")
        command_entity = json.loads(self.body_json)
        pur = command_entity['purpose']
        id_msg = command_entity['id']
        text = command_entity['message']

        # Инициализируем LLMrequest для каждого потока
        llm_request = LLMrequest()

        # Список для хранения будущих задач (результатов)
        ans_multi_language = []

        # Запуск многозадачности с помощью ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.process_language, language, text, llm_request)
                for language in self.languages
            ]
            # Получаем результаты из будущих задач
            for future in as_completed(futures):
                result = future.result()
                ans_multi_language.append(result)

        # Создаем объект Feedback с результатами
        feed = Feedback(payload=ans_multi_language, ID_of_text=id_msg, purpose=pur)
        print(f"RECIEVE TO CommandExtractTitle {self.body_json}")

        return feed
