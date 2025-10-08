# Build a lightweight image for the Binance bot
FROM python:3.11-slim

# Environment settings for Python in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory
WORKDIR /app

# Install dependencies first (leverage Docker layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY . .

# Create a directory for persistent data (SQLite DB)
RUN mkdir -p /data
VOLUME ["/data"]

# Expose the Bottle web UI port
EXPOSE 5311

# Run the bot
CMD ["python", "run.py"]
