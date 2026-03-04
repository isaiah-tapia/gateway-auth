from adapters import webAdapter
from endpoint.session import Session, SessionStore, RATE_LIMIT_SESSION
from endpoint.auth import create_token, auth_token
from adapters.webAdapter import WebAdapter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import HTTPException, WebSocketException
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
def take_user_return_jwt(req: TokenRequest) -> str:
    token = create_token(user_id=req.user_id)
    return token

@app.websocket("/ws")
async def handle_websocket_connections(websocket: WebSocket) -> None:
    """
    This funciton will handle our websocket connections.
    """
    await websocket.accept()
    data_string = await websocket.receive_text()
    data_dict = json.loads(data_string)
    token = data_dict.get("token")
    authenticated_dic = auth_token(token=token)

    if authenticated_dic is None:
        await websocket.close(code=401, reason="unauthorized, token is invalid")
        return
    
    user_id = authenticated_dic.get("sub")
    session_id = data_dict.get("session_id")
    valid_session = sessionStore.get(session_id)
    channel = data_dict.get("channel")

    if valid_session and valid_session.user_id == user_id:
        sessionStore.attach_websocket(session=valid_session, websocket=websocket)
    else:
        valid_session = sessionStore.create(user_id=user_id, channel=channel)
        sessionStore.attach_websocket(session=valid_session, websocket=websocket)

    # send back to client an acknowledgement, session_id and channel
    ack = json.dumps({"ack":1,"session_id":valid_session.session_id,"channel":channel})
    await websocket.send_text(ack)
    while True:
        # check rate limiting
        data = await websocket.receive_text()
        under_rate_limit = valid_session.is_under_rate_limit()
        if under_rate_limit:
            adapter.normalize(data)
        else:
            await websocket.send_text(json.dumps({"error": "rate_limited"}))
            continue


# class main():
#     """
#     Main is where our websocket server should exist, therefore it is where fastAPI attaches to a session?
#     """
#     pass