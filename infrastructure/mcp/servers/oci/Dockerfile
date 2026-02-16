FROM python:3.11-alpine

WORKDIR /app

# Install OCI CLI
RUN apk add --no-cache bash curl && \
    curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh | bash -s -- --accept-all-defaults && \
    ln -s /root/bin/oci /usr/local/bin/oci

# Install Python dependencies
RUN pip install --no-cache-dir flask requests

# Copy MCP server code  
COPY server.py /app/

# Expose SSE port
EXPOSE 9006

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:9006/health')"

# Start server
CMD ["python", "server.py"]
