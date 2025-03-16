import httpx
from app.config import settings


def get_instagram_followers(instagram_user_id: str = None):
    if instagram_user_id is None:
        instagram_user_id = settings.instagram_user_id
    if settings.mock:
        url = f"http://localhost:8001/{instagram_user_id}"
        params = {
            "fields": "followers_count",
            "access_token": "dummy",
        }
    else:
        url = f"https://graph.instagram.com/{instagram_user_id}"
        params = {
            "fields": "followers_count",
            "access_token": settings.instagram_access_token,
        }
    try:
        response = httpx.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("followers_count")
    except Exception as e:
        print(f"instagram error: {e}")
        return None
