FROM python:3.11-slim

WORKDIR /app

# Install runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy wheelhouse and install requirements
COPY wheelhouse ./wheelhouse
COPY requirements.txt .
RUN pip install --no-cache-dir --find-links ./wheelhouse -r requirements.txt

# Copy app code
COPY . .

# ✅ Create writable DeepFace cache folder
RUN mkdir -p /app/.deepface && chmod -R 777 /app/.deepface

# ✅ Tell DeepFace to use it
ENV DEEPFACE_HOME=/app/.deepface

EXPOSE 5000

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-t", "120", "-b", "0.0.0.0:7860", "app:app"]
