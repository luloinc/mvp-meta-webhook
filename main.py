from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/webhook")
async def webhook(request: Request):
    # Get quary params and headers as a dict
    query_params = dict(request.query_params)
    headers = dict(request.headers)

    print("Query params:", query_params)
    print("Headers:", headers)

    return {"message": "OK"}


@app.post("/webhook")
async def webhook(request: Request):
    # Get quary params and headers as a dict
    query_params = dict(request.query_params)
    headers = dict(request.headers)
    
    # Get body as JSON (this will raise an error if body is not valid JSON)
    try:
        body = await request.json()
    except Exception:
        body = {"error": "Body is not valid JSON"}

    print("Query params:", query_params)
    print("Headers:", headers)
    print("Body:", body)

    return {"message": "OK"}