import requests
import json
import os
from django.conf import settings

# URL для генерации текста (Yandex Foundation Models)
YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def suggest_bug_title(text_description: str) -> str:
    """
    Функция-сервис. Принимает 'грязное' описание, возвращает чистый заголовок.
    Никакой связи с БД или HTTP-запросами Django здесь нет.
    """

    # Достаем ключи из переменных окружения
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')

    # Если ключей нет, возвращаем заглушку (чтобы не крешить приложение)
    if not api_key or not folder_id:
        return "[MOCK] AI не настроен. Проверьте .env файл."

    # Формируем промпт (инструкцию для нейросети)
    prompt_data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,  # Низкая температура для точности
            "maxTokens": 100  # Нам нужен только заголовок, много токенов не надо
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — QA Team Lead. Твоя задача: переписать входной текст в идеальный заголовок баг-репорта. Формат: 'Что? Где? Когда?'. Сделай его кратким (до 10 слов), сухим и понятным. Не пиши вводных фраз."
            },
            {
                "role": "user",
                "text": text_description
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key}"
    }

    try:
        response = requests.post(YANDEX_GPT_URL, headers=headers, json=prompt_data, timeout=5)

        if response.status_code == 200:
            result = response.json()
            # Достаем текст из ответа Яндекса
            return result['result']['alternatives'][0]['message']['text']
        else:
            return f"Ошибка YandexGPT: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Ошибка соединения с AI: {str(e)}"