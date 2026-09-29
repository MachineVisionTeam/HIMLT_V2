# Troubleshooting

| Problem | Solution |
|---|---|
| Docker Desktop not starting | Restart laptop and reopen Docker Desktop |
| `docker-compose` not found | Restart Command Prompt after Docker installation |
| Containers not starting | Run `docker-compose logs` |
| Image not loading in browser | Run `docker-compose restart iipimage` |
| Nuclei not showing | Run `docker-compose logs web` |
| Worker keeps restarting | Run `docker-compose logs worker` |
| Port 8080 already in use | Change `"8080:80"` to `"9090:80"` in `docker-compose.yml` |
| Need a fresh start | Run `docker-compose down -v` then `docker-compose up -d` |

## Deeper diagnostics

If the quick fixes above don't resolve it, these more targeted commands can
help narrow down the cause:

```cmd
:: Test the IIPImage tile server directly
curl "http://localhost:8080/iiif/info.json"
:: Expect a JSON response with image width/height.
:: A 404 means iipimage isn't responding — check its logs, then restart it:
docker-compose logs iipimage
docker-compose restart iipimage

:: Confirm the nuclei import actually completed
docker-compose logs web | grep -E "nuclei|import|count"
```

!!! note
    This deployment uses `iipsrv/iipsrv:latest` (v1.3), which only supports
    the `/iiif/` and `/fcgi-bin/iipsrv.fcgi` endpoints. The Nginx
    configuration handles all URL rewrites automatically — no manual
    configuration needed.

## Checking Docker status

```cmd
:: Confirm the Docker engine is healthy
docker info

:: See what's currently running (should be empty before Step 6)
docker ps

:: Confirm your images are present locally
docker images
```

