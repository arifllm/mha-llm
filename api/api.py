import httpx
from typing import Union
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File
from fastapi import FastAPI, Request, Depends, UploadFile, status, Response, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import sys
from datetime import datetime  # Import the date type
import traceback
from typing import List
import json

app = FastAPI()

# CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=200)
def welcome(request: Request, response: Response):
    response.status_code = status.HTTP_200_OK
    return "Welcome to webhook"

@app.get("/webhook", status_code=200)
def webhook_callback(request: Request, response: Response):
    request_param = {
        "mode": request.query_params.get("hub.mode"),
        "challenge": request.query_params.get("hub.challenge"),
        "verify_token": request.query_params.get("hub.verify_token")
    }

    my_token = "EEEE0-0289747-SC-820479"
    
    if request_param["mode"] and request_param["verify_token"]:

        if request_param["mode"] == "subscribe" and request_param["verify_token"] == my_token:
            response.status_code = status.HTTP_200_OK
            return request_param["challenge"]
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    

async def send_message(to, message):
    token = "EAAW70TyVLb8BO88ZAvNgZCCy0N0dkWaJcqgOqmSvNv7Ii7SBNdAKMdEliIT9OQ8Xqsum9nKTk4mlRnd7ZATVzQQb8gCVsgoXHFxAgGSraVCEq8ZAY8fMZCignxKsZBQlNjXdmCm4sBZAFz3gsZBZB0jrZBODT99HXZA3RCRSwOzVCx5G4P3Em0YoigXF4dZCHZAnhQ04xcIPhbzKJayL58ly0sAxOQQZDZD"
    async with httpx.AsyncClient() as client:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
            "name": "mentor_temp",
            "language": {
                "code": "en_US",
                "policy": "deterministic"
            },
            "components": [
                {
                "type": "body",
                "parameters": [
                    {
                        "type": "text","text": message
                    }
                ]
                }
            ]
            }
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = await client.post("https://graph.facebook.com/v19.0/336244906239007/messages", json=payload, headers=headers)
        data = response.json()
        print("message sent: ", data)
        return {"data": data}

@app.post("/webhook", status_code=200)
async def webhook_msg(request: Request, response: Response):
    request_body = await request.body()
    request_body_json = request_body.decode("utf-8")  # Decode byte string to UTF-8
    request_body_data = json.loads(request_body_json)  # Parse JSON data
    print(request_body_data)  # Print the request body

    if request_body_data['entry'] and request_body_data['entry'][0]['changes'] \
        and request_body_data['entry'][0]['changes'][0]['value'] and request_body_data['entry'][0]['changes'][0]['value']['messages']:
        print("messages: ")
        print(request_body_data['entry'][0]['changes'][0]['value']['messages'])

        msg_from = request_body_data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        msg_body = request_body_data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']


        user_message = {
            'from': msg_from,
            'text': msg_body
        }
        print("user_message = ", user_message)


        answer = "Hi, I am Vaibhav"

        await send_message(msg_from, answer)

    return {"message": "Request received"}