FROM python:3.10-slim

# Install system dependencies for building and running dlib/opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5000

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
