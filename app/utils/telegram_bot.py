import httpx
from app.config import settings


def send_telegram_message(message: str):
    if settings.mock:
        url = f"http://localhost:8002/bot{settings.telegram_bot_token}/sendMessage"
    else:
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    params = {
        "chat_id": settings.telegram_chat_id,
        "text": message,
    }
    try:
        response = httpx.post(url, data=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"telegram error: {e}")
        return None
