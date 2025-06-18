FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System deps
RUN apt-get update && \
    apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Add only necessary code
COPY backend ./backend
COPY main.py ./main.py  # if used

CMD ["uvicorn", "backend.api.qa_api:app", "--host", "0.0.0.0", "--port", "8000"]
