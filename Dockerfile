FROM python:3.13.2-slim

RUN apt update && \
    apt install -y --no-install-recommends \
        default-mysql-client \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
