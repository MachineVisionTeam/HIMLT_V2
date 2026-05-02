# Chat API only (Flask: /api/models, /api/chat).
# Ollama/OpenAI are not inside this image: run Ollama on the host or another
# container and set OLLAMA_HOST / OPENAI_API_KEY at runtime.

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/

ENV PORT=5009
EXPOSE 5009

CMD ["python3", "chat_api_app.py"]
