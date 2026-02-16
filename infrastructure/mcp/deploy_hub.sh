#!/bin/bash
set -e

# Deploy MCP Hub to VPS
# Usage: ./deploy_hub.sh [vps_hostname]

VPS_HOST=${1:-"vps1"}
DEPLOY_PATH="/opt/mcp-hub"

echo "=== MCP Hub Deployer ==="
echo "Target: $VPS_HOST:$DEPLOY_PATH"
echo ""

# 1. Check VPS connectivity
echo "→ Checking VPS connectivity..."
if ! ssh -o ConnectTimeout=5 "$VPS_HOST" "echo 'Connected'" >/dev/null 2>&1; then
    echo "Error: Cannot connect to $VPS_HOST. Is Tailscale running?"
    exit 1
fi

# 2. Create deployment directory
echo "→ Creating deployment directory..."
ssh "$VPS_HOST" "sudo mkdir -p $DEPLOY_PATH && sudo chown \$USER:\$USER $DEPLOY_PATH"

# 3. Copy Docker compose and Dockerfiles
echo "→ Copying Docker compose files..."
scp docker-compose.yml "$VPS_HOST:$DEPLOY_PATH/"
scp -r servers/ "$VPS_HOST:$DEPLOY_PATH/"

# 4. Copy secrets
echo "→ Copying environment secrets..."
if [ -f .env ]; then
    scp .env "$VPS_HOST:$DEPLOY_PATH/"
else
    echo "Warning: .env file not found. Creating template..."
    ssh "$VPS_HOST" "cat > $DEPLOY_PATH/.env << 'EOF'
# MCP Hub Environment Variables
GITHUB_TOKEN=your_github_pat_here
PERPLEXITY_KEY=your_perplexity_key_here
CF_TOKEN=your_cloudflare_token_here
CF_ACCOUNT_ID=your_cloudflare_account_id_here
EOF"
    echo "⚠️  Please edit $DEPLOY_PATH/.env on $VPS_HOST before starting services!"
fi

# 5. Build and start services
echo "→ Building and starting MCP Hub..."
ssh "$VPS_HOST" "cd $DEPLOY_PATH && docker-compose build && docker-compose up -d"

# 6. Health check
echo "→ Checking service health..."
sleep 5
ssh "$VPS_HOST" "cd $DEPLOY_PATH && docker-compose ps"

echo ""
echo "✅ MCP Hub deployed successfully!"
echo ""
echo "Service URLs (via Tailscale):"
echo "  - GitHub: http://$(ssh $VPS_HOST 'tailscale ip -4'):9001/sse"
echo "  - Perplexity: http://$(ssh $VPS_HOST 'tailscale ip -4'):9002/sse"
echo "  - Cloudflare: http://$(ssh $VPS_HOST 'tailscale ip -4'):9003/sse"
echo "  - Memory: http://$(ssh $VPS_HOST 'tailscale ip -4'):9004/sse"
echo "  - Playwright: http://$(ssh $VPS_HOST 'tailscale ip -4'):9005/sse"
echo ""
echo "Next steps:"
echo "  1. Update mcp_config.json to use remote URLs"
echo "  2. Test connection: curl http://<tailscale_ip>:9001/health"
