from abc import ABC, abstractmethod


class Translator(ABC):
    @abstractmethod
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Переводит текст с указанного языка на целевой язык.

        :param text: Исходный текст
        :param source_lang: Исходный язык (например, 'EN', 'PL', 'RU')
        :param target_lang: Целевой язык (например, 'EN', 'PL', 'RU')
        :return: Переведённый текст
        """
        pass
