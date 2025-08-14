FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    libxml2 \
    libxslt1.1 \
    libglib2.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    fonts-liberation \
    fonts-freefont-ttf \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
COPY Cairo-Regular.ttf /usr/share/fonts/truetype/
COPY Cairo-Bold.ttf /usr/share/fonts/truetype/
RUN fc-cache -fv

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
