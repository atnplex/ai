import express from 'express';
import fetch from 'node-fetch';
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
      tools: {
        search: {
          description: "Perform a deep search across the web via Perplexity Pro (rotates keys).",
          inputSchema: {
            type: "object",
            properties: {
              query: { type: "string", description: "The search query" }
            },
            required: ["query"]
          }
        }
      },
    },
  }
);

// Type guards for request parameters
interface ToolCallParams {
  name: string;
  arguments?: {
    query?: string;
  };
}

server.setRequestHandler(async (request: any) => {
  if (request.method === "tools/call") {
    const params = request.params as ToolCallParams;
    if (params.name === "search") {
      const query = params.arguments?.query;
      if (!query) throw new Error("Query is required.");

      const key = getRotatedKey();
      if (!key) throw new Error("No Perplexity API keys configured.");

      console.log(`Searching for: ${query} using key index ${currentKeyIndex}`);

      const response = await fetch("https://api.perplexity.ai/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${key}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "sonar-reasoning-pro",
          messages: [{ role: "user", content: query }]
        })
      });

      if (!response.ok) {
        const error = await response.text();
        return {
          content: [{ type: "text", text: `Search failed with status ${response.status}: ${error}` }],
          isError: true
        };
      }

      const data: any = await response.json();
      return {
        content: [{ type: "text", text: data.choices[0].message.content }]
      };
    }
  }
  throw new Error(`Method ${request.method} not implemented.`);
});

app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/message", res);
  await server.connect(transport);
});

app.post("/message", async (req, res) => {
  // Handle incoming MCP messages
  // This would typically involve delegating to the server's internal mechanisms
});

app.listen(port, () => {
  console.log(`Search Gateway listening on port ${port}`);
  console.log(`Active keys: ${API_KEYS.length}`);
});
