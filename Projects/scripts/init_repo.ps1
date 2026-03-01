# BOTCOP Repository Initialization Script
git init
echo "# Project BOTCOP" > README.md
git add .
git commit -m "Initial commit: Project BOTCOP Backbone"
git branch -M main
git branch dev
git commit -m "chore: setup project structure and baseline modules"
Write-Host "GitHub-ready repository initialized. Branch strategy: main (prod) + dev (development)." -ForegroundColor Green
