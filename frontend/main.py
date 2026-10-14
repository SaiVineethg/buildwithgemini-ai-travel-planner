"""FastAPI proxy for the AI Travel Planner Agent (Agent Runtime, agents-cli 1.1.0+).

Provides:
- Credentialed login (user_brotherhood / userbro123@#$)
- Authenticated /chat proxying to deployed Agent Engine over A2A protocol
- Static asset serving and proxying for destination images and markdown itineraries
- Single-page application serving for the travel chat interface
"""

import hashlib
import hmac
import os
import time
import uuid
from pathlib import Path

import google.auth
import google.auth.transport.requests
import httpx
from a2a.client import ClientConfig, ClientFactory
from a2a.types import (
    AgentCard,
    FilePart,
    Message,
    Part,
    Role,
    TaskArtifactUpdateEvent,
    TextPart,
    TransportProtocol,
)
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

# Credentials configuration
AUTH_USERNAME = os.environ.get("AUTH_USERNAME", "user_brotherhood")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "userbro123@#$")
SECRET_KEY = os.environ.get("SESSION_SECRET", "travel-brotherhood-secret-key-2026")

RESOURCE = os.environ.get(
    "AGENT_ENGINE_RESOURCE_NAME",
    "projects/746450897275/locations/us-east1/reasoningEngines/6944089930033266688",
)
AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
LOCATION = RESOURCE.split("/locations/")[1].split("/")[0]

A2A_BASE = (
    f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
    f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
)
A2A_CARD_URL = f"{A2A_BASE}/.well-known/agent-card.json"
_A2UI_MIME = "application/json+a2ui"

# Local directories for development testing
LOCAL_STATIC_DIR = Path("/config/Desktop/BuildWithGemini/travel-planner-agent/app/static")

# Google ADC credentials
_creds, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)


def _auth_headers() -> dict[str, str]:
    _creds.refresh(google.auth.transport.requests.Request())
    return {
        "Authorization": f"Bearer {_creds.token}",
        "Content-Type": "application/json",
    }


def create_session_token(username: str) -> str:
    timestamp = str(int(time.time()))
    payload = f"{username}:{timestamp}"
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def verify_session_token(token: str) -> bool:
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return False
        username, timestamp, sig = parts
        if username != AUTH_USERNAME:
            return False
        payload = f"{username}:{timestamp}"
        expected_sig = hmac.new(
            SECRET_KEY.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return False
        # Valid for 14 days
        if time.time() - int(timestamp) > 14 * 86400:
            return False
        return True
    except Exception:
        return False


app = FastAPI(title="AI Travel Planner Frontend")


@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )


# A2A state caches
_contexts: dict[str, str] = {}
_card: AgentCard | None = None


async def _get_card(client: httpx.AsyncClient) -> AgentCard:
    global _card
    if _card is None:
        resp = await client.get(A2A_CARD_URL)
        resp.raise_for_status()
        card = AgentCard(**resp.json())
        card.url = A2A_BASE
        _card = card
    return _card


def _extract_parts(parts: list) -> list[dict]:
    out: list[dict] = []
    for p in parts:
        root = getattr(p, "root", p)
        if isinstance(root, TextPart) and getattr(root, "text", None):
            out.append({"kind": "text", "text": root.text})
        elif getattr(root, "data", None) is not None:
            meta = getattr(root, "metadata", None) or {}
            mime = meta.get("mimeType") if isinstance(meta, dict) else None
            if mime == _A2UI_MIME:
                out.append({"kind": "a2ui", "data": root.data})
        elif isinstance(root, FilePart):
            uri = getattr(getattr(root, "file", None), "uri", None)
            if uri:
                out.append({"kind": "text", "text": uri})
    return out


@app.post("/api/login")
async def login(req: Request):
    try:
        body = await req.json()
    except Exception:
        body = {}
    user = body.get("username", "").strip()
    pwd = body.get("password", "")

    if user == AUTH_USERNAME and pwd == AUTH_PASSWORD:
        token = create_session_token(user)
        return {"status": "ok", "token": token, "username": user}

    return JSONResponse(
        status_code=401,
        content={"status": "error", "message": "Invalid username or password."},
    )


@app.get("/api/auth-status")
async def auth_status(req: Request):
    auth_header = req.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    valid = verify_session_token(token)
    return {"authenticated": valid, "username": AUTH_USERNAME if valid else None}


@app.post("/chat")
async def chat(req: Request):
    try:
        body = await req.json()
    except Exception:
        body = {}

    message = (body.get("message") or "").strip()
    if not message:
        return JSONResponse({"parts": [{"kind": "text", "text": "Please provide a travel question or destination."}]})

    user_id = body.get("user_id") or "travel-planner-user"
    parts: list[dict] = []

    try:
        async with httpx.AsyncClient(headers=_auth_headers(), timeout=180) as client:
            card = await _get_card(client)
            factory = ClientFactory(
                ClientConfig(
                    supported_transports=[
                        TransportProtocol.jsonrpc,
                        TransportProtocol.http_json,
                    ],
                    httpx_client=client,
                )
            )
            a2a_client = factory.create(card)

            ctx = _contexts.get(user_id)
            msg = Message(
                message_id=str(uuid.uuid4()),
                role=Role.user,
                parts=[Part(root=TextPart(text=message))],
                context_id=ctx,
            )

            last_task = None
            got_artifact_update = False
            try:
                async for event in a2a_client.send_message(msg):
                    if not isinstance(event, tuple):
                        continue
                    task, update = event
                    if task is not None:
                        last_task = task
                        if getattr(task, "context_id", None):
                            _contexts[user_id] = task.context_id
                    if isinstance(update, TaskArtifactUpdateEvent):
                        got_artifact_update = True
                        parts.extend(_extract_parts(update.artifact.parts))
            except Exception as send_err:
                # If failed with existing context, retry once with a clean context
                if ctx is not None:
                    _contexts.pop(user_id, None)
                    msg.context_id = None
                    last_task = None
                    got_artifact_update = False
                    async for event in a2a_client.send_message(msg):
                        if not isinstance(event, tuple):
                            continue
                        task, update = event
                        if task is not None:
                            last_task = task
                            if getattr(task, "context_id", None):
                                _contexts[user_id] = task.context_id
                        if isinstance(update, TaskArtifactUpdateEvent):
                            got_artifact_update = True
                            parts.extend(_extract_parts(update.artifact.parts))
                else:
                    raise send_err

            # Non-streaming fallback: pull parts from the final task's artifacts.
            if not got_artifact_update and last_task is not None:
                for artifact in getattr(last_task, "artifacts", None) or []:
                    parts.extend(_extract_parts(artifact.parts))
                if not parts and getattr(last_task, "history", None):
                    for m in reversed(last_task.history):
                        if getattr(m, "role", None) == Role.agent:
                            parts.extend(_extract_parts(m.parts))
                            break

        if not parts:
            parts = [{"kind": "text", "text": "(The agent completed the request but returned no text parts.)"}]
        return JSONResponse({"parts": parts})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"parts": [{"kind": "text", "text": f"⚠️ Travel Agent error: {str(e)}"}]}
        )


# Static assets routes for images & markdown itineraries
LOCAL_STATIC_DIRS = [
    Path(__file__).parent / "static",
    Path("/config/Desktop/BuildWithGemini/travel-planner-agent/app/static"),
]


def find_local_file(subdir: str, filename: str) -> Path | None:
    for base in LOCAL_STATIC_DIRS:
        cand = base / subdir / filename
        if cand.is_file():
            return cand
    return None


@app.get("/static/images/{filename}")
async def get_static_image(filename: str):
    # Check local static directory
    local_file = find_local_file("images", filename)
    if local_file:
        return FileResponse(local_file)

    # Proxy from deployed agent runtime
    url = f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/{RESOURCE}/api/static/images/{filename}"
    try:
        async with httpx.AsyncClient(headers=_auth_headers(), timeout=30) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                media_type = resp.headers.get("content-type", "image/png")
                return Response(content=resp.content, media_type=media_type)
    except Exception:
        pass
    return Response(status_code=404, content=b"Image not found")


@app.get("/static/itineraries/{filename}")
async def get_static_itinerary(filename: str):
    # Check local static directory
    local_file = find_local_file("itineraries", filename)
    if local_file:
        return FileResponse(
            local_file,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    # Proxy from deployed agent runtime
    url = f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/{RESOURCE}/api/static/itineraries/{filename}"
    try:
        async with httpx.AsyncClient(headers=_auth_headers(), timeout=30) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                return Response(
                    content=resp.content,
                    media_type="text/markdown",
                    headers={
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    },
                )
    except Exception:
        pass
    return Response(status_code=404, content=b"Itinerary not found")


# Serve the Single Page Web Application
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
