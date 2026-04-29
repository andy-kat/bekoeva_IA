import requests
import json

def get_random_quote():
    """
    Запрашивает случайную цитату с Forismatic API.
    Возвращает словарь с цитатой и автором или сообщение об ошибке.
    """
    url = "http://api.forismatic.com/api/1.0/"
    
    # Параметры запроса
    params = {
        "method": "getQuote",
        "format": "json", # Запрашиваем ответ в формате JSON
        "lang": "ru"      # Запрашиваем цитаты на русском языке
    }
    
    try:
        # Отправляем GET-запрос
        response = requests.get(url, params=params, timeout=5)
        
        # Проверяем, успешно ли выполнился запрос (код 200)
        response.raise_for_status()
        
        # Преобразуем ответ в JSON-объект
        data = response.json()
        
        # Проверяем, есть ли в ответе нужные ключи.
        # Иногда API может вернуть ответ без текста.
        if "quoteText" in data:
            
            return {
                "text": data["quoteText"],
                "author": data["quoteAuthor"] if data["quoteAuthor"] else "Неизвестный автор"
            }
        else:
            return {"error": "Получен неполный ответ от сервера."}

    except requests.exceptions.RequestException as e:
        # Обрабатываем ошибки сети, таймаута и т.д.
        return {"error": f"Ошибка сети: {e}"}
    except json.JSONDecodeError:
        return {"error": "Не удалось распознать ответ сервера как JSON."}


quote = get_random_quote()
    
if "error" in quote:
        print(f"Произошла ошибка: {quote['error']}")
else:
        print("--- Случайная цитата ---")
        print(f'"{quote["text"]}"')
        print(f"— {quote['author']}")
