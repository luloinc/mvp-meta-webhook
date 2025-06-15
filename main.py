from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    # Get headers as a dict
    headers = dict(request.headers)
    
    # Get body as JSON (this will raise an error if body is not valid JSON)
    try:
        body = await request.json()
    except Exception:
        body = {"error": "Body is not valid JSON"}

    print("Headers:", headers)
    print("Body:", body)

    return {"message": "Hello World"}