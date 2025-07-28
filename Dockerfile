FROM python:3.10-slim

WORKDIR /app

# Install minimal dependencies and system tools
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies (CPU-only, fast)
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Now copy the rest of your project files
COPY . .

# Ensure model is available offline inside image (under model/)
# Optional: Verify or print a log to confirm it's present
RUN ls model

CMD ["python", "main.py"]
