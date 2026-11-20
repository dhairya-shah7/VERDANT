#!/bin/bash
# ==============================================================================
# V.E.R.D.A.N.T. — One-Click Google Cloud Run Deployment Script
# Built for Google Cloud & DeepMind Startup Buildathon 2026
# ==============================================================================

set -e

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")
REGION="us-central1"
SERVICE_NAME="verdant-server"

echo "======================================================================"
echo "🌿 Deploying V.E.R.D.A.N.T. to Google Cloud Run"
echo "======================================================================"

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No Google Cloud project selected."
    echo "👉 Run: gcloud config set project <YOUR_GCP_PROJECT_ID>"
    exit 1
fi

echo "📍 GCP Project: $PROJECT_ID"
echo "📍 Region:      $REGION (92% Carbon Free Energy)"
echo "📍 Service:     $SERVICE_NAME"

# 1. Enable Required Google Cloud APIs
echo ""
echo "⚙️ Enabling Google Cloud APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    storage.googleapis.com \
    secretmanager.googleapis.com \
    --project="$PROJECT_ID"

# 2. Deploy directly to Google Cloud Run from source
echo ""
echo "🚀 Building & Deploying to Cloud Run via Buildpacks..."
gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region="$REGION" \
    --platform=managed \
    --allow-unauthenticated \
    --port=8000 \
    --cpu=2 \
    --memory=2Gi \
    --min-instances=0 \
    --max-instances=10 \
    --timeout=300 \
    --set-env-vars="GCP_PROJECT=$PROJECT_ID,GCP_REGION=$REGION,ENVIRONMENT=production,VERTEX_AI_ENABLED=true" \
    --project="$PROJECT_ID"

# 3. Retrieve Cloud Run Service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --platform=managed --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")

echo ""
echo "======================================================================"
echo "✅ V.E.R.D.A.N.T. LIVE ON GOOGLE CLOUD RUN!"
echo "======================================================================"
echo "🌐 Service URL: $SERVICE_URL"
echo "🔍 Health Check: $SERVICE_URL/health"
echo "📊 GCP Status:  $SERVICE_URL/api/gcp/status"
echo "======================================================================"
