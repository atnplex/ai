FROM python:3.11-alpine

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir flask requests gql[all]

# Copy MCP server code
COPY server.py /app/

# Expose SSE port
EXPOSE 9007

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:9007/health')"

# Start server
CMD ["python", "server.py"]
