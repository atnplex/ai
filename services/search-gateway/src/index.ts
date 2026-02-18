import express from 'express';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';

const app = express();
const port = process.env.PORT || 3000;

// Configuration: Multiplexed Perplexity Keys
const API_KEYS = [
  process.env.PERPLEXITY_KEY_1,
  process.env.PERPLEXITY_KEY_2,
  process.env.PERPLEXITY_KEY_3
].filter(Boolean) as string[];

let currentKeyIndex = 0;

function getRotatedKey() {
  if (API_KEYS.length === 0) return null;
  const key = API_KEYS[currentKeyIndex];
  currentKeyIndex = (currentKeyIndex + 1) % API_KEYS.length;
  return key;
}

const server = new Server(
  {
    name: "search-gateway",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(async (request) => {
  // Logic to proxy search requests to Perplexity with rotated keys
  // placeholder for specific tool implementation
  throw new Error("Method not implemented.");
});

app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/message", res);
  await server.connect(transport);
});

app.post("/message", async (req, res) => {
  // Handle incoming MCP messages
});

app.listen(port, () => {
  console.log(`Search Gateway listening on port ${port}`);
  console.log(`Active keys: ${API_KEYS.length}`);
});
