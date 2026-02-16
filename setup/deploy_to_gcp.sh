#!/bin/bash
set -e

# One-Liner Deploy to GCP
# Wraps gcloud run deploy with best-practice flags for MCP servers.

echo "=== MCP GCP Deployer ==="

# 1. Config Detection
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
REGION=$(gcloud config get-value run/region 2>/dev/null || echo "us-central1")

if [ -z "$PROJECT_ID" ]; then
    echo "Error: No gcloud project detected. Run 'gcloud init' first."
    exit 1
fi

echo "Project: $PROJECT_ID"
echo "Region:  $REGION"

# 2. Service Name
read -p "Enter Service Name [mcp-server]: " SERVICE_NAME
SERVICE_NAME=${SERVICE_NAME:-mcp-server}

# 3. Security Mode Selection
echo ""
echo "Select Security Mode:"
echo "1) Private (Internal Only) - Accessible ONLY via VPC/Tailscale. No public internet."
echo "2) Public (IAM Auth)       - Accessible via internet, but requires IAM Authentication."
read -p "Choose [1]: " MODE
MODE=${MODE:-1}

INGRESS_FLAG="--ingress=internal"
AUTH_FLAG="--no-allow-unauthenticated"

if [ "$MODE" -eq 2 ]; then
    INGRESS_FLAG="--ingress=all"
    echo "Selected: Public access with IAM + Token Auth."
else
    echo "Selected: Private Internal access (VPC/Tailscale required)."
fi

# 4. Deploy
echo ""
echo "Deploying $SERVICE_NAME..."
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --platform managed \
  --region "$REGION" \
  $INGRESS_FLAG \
  $AUTH_FLAG \
  --memory 512Mi \
  --cpu 1 \
  --quiet

echo ""
echo "=== Deployment Complete ==="
echo "Service URL: $(gcloud run services describe "$SERVICE_NAME" --platform managed --region "$REGION" --format 'value(status.url)')"
if [ "$MODE" -eq 1 ]; then
    echo "Note: URL is only accessible from within the VPC or Tailscale network."
fi
