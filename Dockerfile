FROM python:3.11-slim

WORKDIR /app

# Install required runtime libraries
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

# Copy all app files
COPY . .

# ✅ Set DeepFace to store models/data in a writable folder
ENV DEEPFACE_HOME=/app/.deepface

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-t", "120", "-b", "0.0.0.0:5000", "app:app"]
