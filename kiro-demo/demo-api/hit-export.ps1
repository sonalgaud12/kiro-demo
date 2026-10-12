# Calls /reports/export several times in a row and prints each HTTP status.
# Before rate limiting: all 200. After: 200s, then 429s.
# Usage: .\hit-export.ps1 [-Count 6]   (the server must be running)

param([int]$Count = 6)

for ($i = 1; $i -le $Count; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:8000/reports/export" `
            -Headers @{ "X-API-Key" = "demo-key-alpha" } -UseBasicParsing
        $code = $r.StatusCode
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
    }
    Write-Output "Request $i -> $code"
}
