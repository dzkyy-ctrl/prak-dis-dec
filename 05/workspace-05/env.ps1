function dcu  { docker compose up --build -d --scale bs_app=2 }
function dcd  { docker compose down }
function dps  { docker ps --format "{{.Image}} {{.Names}}" }
function dcln { docker logs nginx }
