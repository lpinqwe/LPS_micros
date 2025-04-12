import json
import os
from app.prompts import prompts

class Configurator:
    def __init__(self, config_file="config.json"):
        """Инициализация конфигуратора и загрузка параметров из JSON файла"""
        self.config_file = config_file
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """Загружает конфигурацию из JSON файла"""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Конфигурационный файл {config_file} не найден.")

        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    def configure(self):
        prompts.prompt_translate = self.config("prompt_translate")
        prompts.prompt_extract_title=self.config("prompt_extract_title")

        None
    def get(self, key, default=None):
        """Получение значения конфигурации по ключу"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value else default

    def get_database_config(self):
        """Получение конфигурации базы данных"""
        return self.config.get('database', {})

    def get_logging_config(self):
        """Получение конфигурации логирования"""
        return self.config.get('logging', {})
