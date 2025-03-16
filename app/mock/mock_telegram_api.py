from fastapi import FastAPI, Request, HTTPException

app = FastAPI()


@app.post("/bot{token}/sendMessage")
async def send_message(token: str, request: Request):
    form_data = await request.form()
    chat_id = form_data.get("chat_id")
    text = form_data.get("text")
    if not chat_id or not text:
        raise HTTPException(status_code=400, detail="missing chat_id or text")
    return {"ok": True, "result": {"message_id": 123, "chat": {"id": chat_id}, "text": text}}
