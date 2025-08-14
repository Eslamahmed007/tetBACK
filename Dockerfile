FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    libssl-dev \
    libxml2 \
    libxslt1.1 \
    libglib2.0-0 \
    fonts-liberation \
    fonts-freefont-ttf \
    shared-mime-info \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]


