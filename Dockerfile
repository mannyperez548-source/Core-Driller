FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY relay_server.py launch.py ./
COPY public ./public

ENV PORT=8080
EXPOSE 8080

CMD ["python", "relay_server.py"]
