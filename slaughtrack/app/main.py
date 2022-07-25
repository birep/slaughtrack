from fastapi import Request
from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime as dt
import time
import hashlib



def private_to_public(plaintext: str):
    return hashlib.md5(plaintext.encode("utf-8")).hexdigest()

def utc_ts():
    return time.mktime(dt.now().timetuple()) * 1000.0

test_uuid = "secret-uuid"

pubkeys = {private_to_public(test_uuid): {'exists': True, 'user_id': 0, 'latest_event': {'timestamp': 1658388029, "event_id": 0 }}}

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@app.get("/u/{uuid_hash}")
async def workspace(uuid_hash, response: Response):
    try:
        return pubkeys[uuid_hash]['latest_event']
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return 

@app.post("/u/{uuid}/{eid}")
async def root(uuid,eid):
    pubkey = private_to_public(uuid)
    pubkeys[pubkey]['latest_event'] = {'timestamp':utc_ts(),'event_id':eid}
    return pubkeys[pubkey]['latest_event']
