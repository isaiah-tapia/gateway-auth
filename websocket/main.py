from adapters import webAdapter
from endpoint.session import Session, SessionStore
from endpoint.auth import create_token, auth_token
from adapters.webAdapter import WebAdapter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

import json
import logging
import uuid
import asyncio

logger = logging.getLogger("gateway")
app = FastAPI("gateway")
sessionStore = SessionStore()
adapter = WebAdapter()

class TokenRequest(BaseModel):
    user_id: str

@app.post("/auth/token")
def take_user_return_jwt(req: TokenRequest):
    token = create_token(user_id=req.user_id)
    return token

@app.websocket("/ws")
async def handle_websocket_connections(websocket: WebSocket):
    """
    This funciton will handle our websocket connections. Immediatly after accepting our websocket we should 
    """
    await websocket.accept()
    data_string = await websocket.receive_text()
    data_dict = json.loads(data_string)
    
    # while True:
        # await websocket.send_text(data)


# class main():
#     """
#     Main is where our websocket server should exist, therefore it is where fastAPI attaches to a session?
#     """
#     pass