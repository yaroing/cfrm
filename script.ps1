# Login
$loginBody = @{ username = "admin"; password = "admin123" } | ConvertTo-Json
$r = Invoke-WebRequest -Method Post -Uri "http://localhost:8000/api/v1/auth/login/" -ContentType "application/json" -Body $loginBody -SkipHttpErrorCheck
"Status: $($r.StatusCode)"
$r.Content

# Parse JSON and extract tokens
$resp = $r.Content | ConvertFrom-Json
$access  = $resp.access
$refresh = $resp.refresh

# Quick sanity
$access.Substring(0,30) + "..."
$refresh.Substring(0,30) + "..."