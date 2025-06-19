FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port used by the Flask app
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
