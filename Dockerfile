FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./server.py
COPY public/index.html ./index.html

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD ["sh", "-c", "exec python server.py --host 0.0.0.0 --port ${PORT:-8080}"]
