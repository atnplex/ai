FROM node:20-alpine

WORKDIR /app

# Install MCP server package
RUN npm install -g @cloudflare/mcp-server-cloudflare

# Expose SSE port
EXPOSE 9003

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:9003/health || exit 1

# Start server with SSE transport
CMD ["npx", "@cloudflare/mcp-server-cloudflare", "--transport", "sse", "--port", "9003"]
