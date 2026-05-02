#!/usr/bin/env python3
"""
Standalone API for the HIMLT chat popup: GET /api/models, POST /api/chat.
Same behaviour as the routes in /opt/tab/llm/web_app.py (no slide proxy, no HIMLT static).

Run from this directory:
  pip install -r requirements.txt
  export OPENAI_API_KEY=...   # if using online model
  PORT=5009 python3 chat_api_app.py
"""

from __future__ import annotations

import logging
import os
import sys

# Local imports: models/, utils/ live next to this file
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from dotenv import load_dotenv
    for _env in (
        os.path.join(_ROOT, ".env"),
        os.path.join(os.path.dirname(_ROOT), ".env"),
        "/opt/tab/llm/.env",
    ):
        if os.path.isfile(_env):
            load_dotenv(_env)
            break
except ImportError:
    pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("chat_api")

from flask import Flask, jsonify, request

from models.registry import get_registry
from prompts import DEFAULT_SYSTEM, HIMLT_SYSTEM
from utils.network import is_internet_available

app = Flask(__name__)


@app.after_request
def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.errorhandler(500)
def _handle_500(e):
    return jsonify({"error": str(e) if str(e) else "Internal server error"}), 500


def _resolve_model(model_id, registry):
    if model_id == "auto":
        online = registry.get_model_by_id("gpt-4o-mini")
        offline = registry.get_model_by_id("medllama3")
        has_key = bool(os.getenv("OPENAI_API_KEY", "").strip())
        if has_key and is_internet_available() and online and online.is_available():
            return online
        if offline and offline.is_available():
            return offline
        if online and online.is_available():
            return online
        return offline
    return registry.get_model_by_id(model_id)


def _generate_with_fallback(model, messages, is_auto, registry):
    try:
        out = model.generate(messages)
        return out, False
    except BaseException as e:
        log.warning("model %s failed: %s", model.id, e)
        if not is_auto:
            raise
        offline = registry.get_model_by_id("medllama3")
        if offline and offline.is_available() and model.id != offline.id:
            try:
                out = offline.generate(messages)
                return out, True
            except BaseException as e2:
                log.warning("fallback model failed: %s", e2)
                raise e from e2
        raise


@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"ok": True})


@app.route("/api/models", methods=["GET", "OPTIONS"])
def list_models():
    if request.method == "OPTIONS":
        return "", 204
    try:
        registry = get_registry()
        models = []
        for m in registry.list_models():
            models.append({
                "id": m.id,
                "name": m.name,
                "available": m.is_available(),
                "needs_api_key": m.is_online,
                "is_offline": not m.is_online,
            })
        models.sort(key=lambda x: (0 if x["needs_api_key"] else 1, x["name"]))
        models.insert(0, {
            "id": "auto",
            "name": "Auto (recommended)",
            "available": True,
            "needs_api_key": False,
            "is_offline": True,
        })
        return jsonify({"models": models})
    except Exception as e:
        log.exception("list_models: %s", e)
        return jsonify({"error": str(e), "models": []}), 500


@app.route("/api/chat/echo", methods=["POST", "OPTIONS"])
def chat_echo():
    if request.method == "OPTIONS":
        return "", 204
    body = request.get_json(silent=True) or {}
    msg = (body.get("messages") or [{}])[-1].get("content", "hello")
    return jsonify({"response": "Echo: " + str(msg), "model_used": "echo", "fallback": False})


@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 204
    log.info("chat request received")
    try:
        body = request.get_json(silent=True) or {}
        model_id = body.get("model_id", "auto")
        messages = body.get("messages", [])
        context = body.get("context", "")
        if not messages:
            return jsonify({"error": "messages required"}), 400

        system_content = HIMLT_SYSTEM if context == "himlt" else DEFAULT_SYSTEM
        if not any(m.get("role") == "system" for m in messages):
            messages = [{"role": "system", "content": system_content}] + messages

        registry = get_registry()
        model = _resolve_model(model_id, registry)
        if not model:
            return jsonify({"error": f"Model not found: {model_id}"}), 400
        if not model.is_available():
            hint = ""
            if model.is_online:
                hint = " Set OPENAI_API_KEY in .env or: export OPENAI_API_KEY=sk-..."
            else:
                hint = " Run: ollama serve  and  ollama pull <model>"
            return jsonify({"error": f"Model {model.name} not available.{hint}"}), 503

        log.info("calling model=%s", model.id)
        is_auto = model_id == "auto"
        resp_text, fallback = _generate_with_fallback(model, messages, is_auto, registry)
        log.info("model=%s done", model.id)
        return jsonify({
            "response": resp_text,
            "model_used": model.id,
            "fallback": fallback,
        })
    except BaseException as e:
        log.exception("chat error: %s", e)
        try:
            return jsonify({"error": str(e)}), 500
        except BaseException:
            return jsonify({"error": "Internal server error"}), 500


def _port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


if __name__ == "__main__":
    base_port = int(os.getenv("PORT", "5009"))
    port = base_port
    for _ in range(10):
        if _port_in_use(port):
            port += 1
            continue
        break
    print("Chat API listening on http://0.0.0.0:{}".format(port))
    print("  GET  /api/models   POST /api/chat")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
