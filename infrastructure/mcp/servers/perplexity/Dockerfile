FROM node:20-alpine

WORKDIR /app

# Install MCP server package
RUN npm install -g server-perplexity-ask

# Expose SSE port
EXPOSE 9002

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:9002/health || exit 1

# Start server with SSE transport
CMD ["npx", "server-perplexity-ask", "--transport", "sse", "--port", "9002"]
