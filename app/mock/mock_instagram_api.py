from fastapi import FastAPI, HTTPException, Request
from random import randint

app = FastAPI()

follower_data = {}


@app.get("/{instagram_user_id}")
async def get_followers(instagram_user_id: str, request: Request):
    fields = request.query_params.get("fields")
    if fields != "followers_count":
        raise HTTPException(status_code=400, detail="missing 'followers_count' field")
    current_count = follower_data.get(instagram_user_id, 500)
    change = randint(5, 20)
    current_count += change
    follower_data[instagram_user_id] = current_count
    return {"followers_count": current_count}
