from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os


# Get the verify token from environment variable
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "11111")

app = FastAPI()


@app.get("/webhook")
async def verify_webhook(request: Request):
    # Get query params
    query_params = dict(request.query_params)
    
    # Check if this is a verification request
    mode = query_params.get("hub.mode")
    token = query_params.get("hub.verify_token")
    challenge = query_params.get("hub.challenge")

    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == VERIFY_TOKEN:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return int(challenge)
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            raise HTTPException(status_code=403, detail="Verification failed")

    return HTTPException(status_code=400, detail="Missing parameters")


@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    
    # Check if this is a WhatsApp message notification
    if body.get("object"):
        if body.get("entry") and body["entry"][0].get("changes") and body["entry"][0]["changes"][0].get("value"):
            if body["entry"][0]["changes"][0]["value"].get("messages"):
                # Handle the message here
                try:
                    message_body = body["entry"][0]["changes"][0]["value"]["messages"][0].get("text", {}).get("body", "")
                    phone_number = body["entry"][0]["changes"][0]["value"]["messages"][0].get("from", "")
                    
                    print(f"Received message from {phone_number}: {message_body}")
                    
                    # Return a 200 OK response to acknowledge receipt of the event
                    return JSONResponse(content={"status": "ok"})
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    return HTTPException(status_code=500, detail="Error processing message")
    
    # Return a '404 Not Found' if event is not from a WhatsApp API
    raise HTTPException(status_code=404, detail="Not a WhatsApp API event")