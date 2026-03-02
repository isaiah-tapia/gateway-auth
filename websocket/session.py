import asyncio
import json
import logging
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Optional, Set

import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Session():
    """
    Each individual session corresponds to an individual process (i.e a unique user is signed in multiple times across
    devices or apps). 
    """
    def __init__(self, session_id: str, user_id: str, channel: str):
        self.session_id = session_id
        self.user_id = user_id
        self.channel = channel
        self.connected_at = datetime.utcnow()
        self.websocket: Optional[WebSocket] = None
        self.missed_messages: deque = deque(maxlen=MAX_MISSED_MESSAGES)
        # Rate limiting
        self.message_timestamps: deque = deque()

class SessionStore():
    """
    We need to keep track of the session which are on going, this is our trusted computing base. lets assume 
    that this cannot be penetrated
    """