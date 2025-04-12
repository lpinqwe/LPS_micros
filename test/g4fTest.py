from g4f.client import Client


def ask_gpt(prompt: str, payload: dict, model: str = "gpt-4o-mini") -> str:
    # Объединяем prompt и payload
    message_content = f"{prompt}{payload}"

    # Инициализируем клиента
    client = Client()

    # Отправляем запрос
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message_content}],
        web_search=False
    )

    # Возвращаем текст ответа
    return response.choices[0].message.content


language = "PL"
prompt = f"не указывай на ошибки,не добавляй своего, ты google translate,не допускай грамматических ошибок," \
         f"переведи следуущий текст на {language}\nтекст:"
text = "Cześć, nazywam się oacnaoin"
print(ask_gpt(prompt, text))
