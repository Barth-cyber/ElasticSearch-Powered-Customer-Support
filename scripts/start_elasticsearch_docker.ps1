# Helper PowerShell script to start Elasticsearch using Docker
# Run: ./scripts/start_elasticsearch_docker.ps1

param()

Write-Host "Checking for Docker..."
try {
    docker --version | Out-Null
} catch {
    Write-Host "Docker is not installed or not in PATH. Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Elasticsearch container..."

docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.11.0

Write-Host "Waiting for Elasticsearch to become healthy (this may take ~30s)..."
$healthy = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $resp = Invoke-RestMethod -Uri 'http://localhost:9200/_cluster/health' -UseBasicParsing -TimeoutSec 3
        if ($resp.status -eq 'green' -or $resp.status -eq 'yellow') {
            $healthy = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}

if (-not $healthy) {
    Write-Host "Elasticsearch did not become healthy in time." -ForegroundColor Yellow
    exit 1
}

Write-Host "Elasticsearch is healthy and ready at http://localhost:9200" -ForegroundColor Green
Write-Host "You can now run: python setup.py to index the sample knowledge base."
