FROM python:3.10-slim

# Install system dependencies for dlib and opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        libgl1-mesa-glx \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for flask
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# physical webcam support under Docker Desktop/WSL2
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 v4l-utils
ENV OPENCV_VIDEOIO_PRIORITY_MSMF=0

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
