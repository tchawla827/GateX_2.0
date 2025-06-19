FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for dlib, opencv, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default port for the Flask app. Render will override this with the PORT
# environment variable it provides.
ENV PORT=5000

# Expose the port so docker users know which port is intended to be published
EXPOSE ${PORT}

# Run the application with Gunicorn using the eventlet worker. Using `sh -c`
# allows environment variable expansion so the container binds to whichever
# port is provided via the `PORT` environment variable.
CMD ["sh", "-c", "gunicorn -k eventlet -w 1 -b 0.0.0.0:${PORT} app:app"]
