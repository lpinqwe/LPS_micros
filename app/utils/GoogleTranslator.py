from googletrans import Translator as GoogleTranslator
from app.interfaces.translator import Translator


class GoogleTranslateRequest(Translator):
    def __init__(self):
        self.translator = GoogleTranslator()  # Инициализация клиента для Google Translate

    def translate(self, prompt: str, payload: str, languageAnswer="PL", model: str = None) -> str:
        """
        Переводит текст с использованием Google Translate API.

        :param prompt: Описание задачи перевода (используй для нейронок)
        :param payload: Исходный текст для перевода
        :param languageAnswer: Язык, на который нужно перевести текст
        :param model: Не используется в данном примере, но оставлен для совместимости
        :return: Переведённый текст
        """
        # Переводим текст с исходного языка на целевой
        translated = self.translator.translate(payload, dest=languageAnswer)
        return translated.text  # Возвращаем переведённый текст

    def clear_cache(self):
        # Для Google Translate нет необходимости в кэше, так как это API-сервис.
        pass
