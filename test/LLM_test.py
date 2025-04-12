import time
from app.utils.LLMrequest import LLMrequest

llm_request = LLMrequest()

# Измеряем время для первого запроса
start_time = time.time()
print("1")
response1 = llm_request.translate("Привет, как дела?", "Вот мой запр1ыуауос!", languageAnswer="PL")
print("2")
end_time = time.time()
print(f"Ответ на первый запрос: {response1}")
print(f"Время выполнения первого запроса: {end_time - start_time} секунд")

# Измеряем время для второго запроса (будет загружен из кэша)
start_time = time.time()
response2 = llm_request.translate("Привет, как дела?", "Вот мой запр1ыуауос!", languageAnswer="PL")
end_time = time.time()
print(f"Ответ на второй запрос (из кэша): {response2}")
print(f"Время выполнения второго запроса (из кэша): {end_time - start_time} секунд")


# Измеряем время для первого запроса
start_time = time.time()
print("1")
response1 = llm_request.translate("Привет, как дела?", "Вот мой запр1ыуауос!", languageAnswer="ru")
print("2")
end_time = time.time()
print(f"Ответ на первый запрос: {response1}")
print(f"Время выполнения первого запроса: {end_time - start_time} секунд")

# Измеряем время для второго запроса (будет загружен из кэша)
start_time = time.time()
response2 = llm_request.translate("Привет, как дела?", "Вот мой запр1ыуауос!", languageAnswer="ru")
end_time = time.time()
print(f"Ответ на второй запрос (из кэша): {response2}")
print(f"Время выполнения второго запроса (из кэша): {end_time - start_time} секунд")
