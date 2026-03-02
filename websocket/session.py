import asyncio
import json
import logging
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta
from datetime import timezone 
from typing import Dict, Optional, Set

import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SIGNKEY = "foo"
ALGO = "HS256"
TOKEN_EXPIRY = 15
RATE_LIMIT_SESSION = 10
RATE_LIMIT_WINDOW = 60
MAX_MISSED = 100

class Session():
    """
    Each individual session corresponds to an individual process (i.e a unique user is signed in multiple times across
    devices or apps). 
    """
    def __init__(self, session_id: str, user_id: str, channel: str):
        self.session_id = session_id
        self.user_id = user_id
        self.channel = channel
        self.connected_at =  datetime.now(timezone.utc).isoformat()
        self.websocket: Optional[WebSocket] = None
        self.missed_messages: deque = deque(maxlen=MAX_MISSED)
        self.message_timestamps: deque = deque()

class SessionStore():
    """
    We need to keep track of the session which are on going, this is our trusted computing base.
    """

    def __init__(self):
        # maps a user to their session id
        self._sessions: Dict[str, Session] = {}
        pass

    def create(self, ):
        pass

    def get(self):
        pass
    
    def get_session_by_user(self):
        pass

    def attach_websocket(self):
        pass

    def detach_websocket(self):
        pass

