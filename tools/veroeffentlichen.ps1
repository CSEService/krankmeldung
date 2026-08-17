# veroeffentlichen.ps1 — laedt die App zu Cloudflare Pages hoch.
# Aufruf:  pwsh -File tools\veroeffentlichen.ps1
# Adresse: https://cse-krankmeldung.pages.dev/
#
# Hochgeladen wird nur, was der Browser braucht. Aushang, QR-Code, Werkzeuge
# und die Anleitung bleiben bewusst draussen.

$ErrorActionPreference = 'Stop'
$basis = Split-Path -Parent $PSScriptRoot
$dist  = Join-Path $basis '_dist'

$seiten = @('index.html', 'manifest.json', 'sw.js', '_headers')
$bilder = @('logo-quelle.png', 'icon-192.png', 'icon-512.png', 'icon-180.png', 'icon-maskable-512.png')

if (Test-Path $dist) { Remove-Item $dist -Recurse -Force }
New-Item -ItemType Directory -Force (Join-Path $dist 'bilder') | Out-Null

foreach ($d in $seiten) { Copy-Item (Join-Path $basis $d) (Join-Path $dist $d) }
foreach ($d in $bilder) { Copy-Item (Join-Path $basis "bilder\$d") (Join-Path $dist "bilder\$d") }

Write-Host "Lade hoch: $((Get-ChildItem $dist -Recurse -File).Count) Dateien"
npx --yes wrangler@latest pages deploy $dist --project-name cse-krankmeldung --branch main --commit-dirty=true
