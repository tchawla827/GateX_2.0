FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required runtime libraries (no build tools needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy prebuilt wheel and requirements
COPY wheelhouse ./wheelhouse
COPY requirements.txt .

# Install Python dependencies using the local wheel
RUN pip install --no-cache-dir --find-links ./wheelhouse -r requirements.txt

# Copy the full application code
COPY . .

# Expose port used by the Flask app
EXPOSE 5000

# Run the app using Gunicorn with Eventlet worker
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-t", "120", "-b", "0.0.0.0:5000", "app:app"]
