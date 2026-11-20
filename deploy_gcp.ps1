# ==============================================================================
# V.E.R.D.A.N.T. — One-Click Google Cloud Run Deployment Script (PowerShell)
# Built for Google Cloud & DeepMind Startup Buildathon 2026
# ==============================================================================

$ErrorActionPreference = "Stop"

$ProjectId = (gcloud config get-value project 2>$null)
$Region = "us-central1"
$ServiceName = "verdant-server"

Write-Host "======================================================================" -ForegroundColor Green
Write-Host "🌿 Deploying V.E.R.D.A.N.T. to Google Cloud Run (Windows / PowerShell)" -ForegroundColor Green
Write-Host "======================================================================"

if (-not $ProjectId) {
    Write-Host "❌ Error: No Google Cloud project selected." -ForegroundColor Red
    Write-Host "👉 Run: gcloud config set project <YOUR_GCP_PROJECT_ID>" -ForegroundColor Yellow
    exit 1
}

Write-Host "📍 GCP Project: $ProjectId" -ForegroundColor Cyan
Write-Host "📍 Region:      $Region (92% Carbon Free Energy)" -ForegroundColor Cyan
Write-Host "📍 Service:     $ServiceName" -ForegroundColor Cyan

# 1. Enable Required Google Cloud APIs
Write-Host "`n⚙️ Enabling Google Cloud APIs..." -ForegroundColor Yellow
gcloud services enable `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com `
    aiplatform.googleapis.com `
    storage.googleapis.com `
    secretmanager.googleapis.com `
    --project=$ProjectId

# 2. Deploy directly to Google Cloud Run from source
Write-Host "`n🚀 Building & Deploying to Cloud Run via Buildpacks..." -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --source . `
    --region=$Region `
    --platform=managed `
    --allow-unauthenticated `
    --port=8000 `
    --cpu=2 `
    --memory=2Gi `
    --min-instances=0 `
    --max-instances=10 `
    --timeout=300 `
    --set-env-vars="GCP_PROJECT=$ProjectId,GCP_REGION=$Region,ENVIRONMENT=production,VERTEX_AI_ENABLED=true" `
    --project=$ProjectId

# 3. Retrieve Cloud Run Service URL
$ServiceUrl = (gcloud run services describe $ServiceName --platform=managed --region=$Region --format="value(status.url)" --project=$ProjectId)

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host "✅ V.E.R.D.A.N.T. LIVE ON GOOGLE CLOUD RUN!" -ForegroundColor Green
Write-Host "======================================================================"
Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "🔍 Health Check: $ServiceUrl/health" -ForegroundColor Cyan
Write-Host "📊 GCP Status:  $ServiceUrl/api/gcp/status" -ForegroundColor Cyan
Write-Host "======================================================================"
