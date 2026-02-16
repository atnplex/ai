FROM python:3.11-alpine

WORKDIR /app

# Install bws CLI (statically linked binary)
RUN apk add --no-cache curl && \
    curl -Lo /usr/local/bin/bws "https://github.com/bitwarden/sdk/releases/latest/download/bws-x86_64-unknown-linux-musl" && \
    chmod +x /usr/local/bin/bws && \
    apk del curl

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-sse requests

# Copy MCP server code
COPY server.py /app/

# Expose SSE port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:9000/health')"

# Start server
CMD ["python", "server.py"]
