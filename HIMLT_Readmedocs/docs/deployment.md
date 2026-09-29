# Deployment Guide

Deploying HIMLT with Docker Desktop on Windows and MAC, from installation through
opening the app in your browser.

## Windows System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| Disk space | 15 GB free | 20 GB+ free (25–30 GB recommended in practice) |
| OS | Windows 10/11 | Windows 11 |
| CPU | 4 cores | 8+ cores |

## MAC System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| Disk space | 15 GB free | 20 GB+ free (25–30 GB recommended in practice) |
| OS | macOS 12 Monterey | macOS 13 Ventura or later |
| CPU | 4 cores (Intel or Apple Silicon) | Apple M1/M2/M3 or 8+ core Intel |


 "Check free disk space first"
    The images total roughly 9.5 GB uncompressed, plus room for the imported
    database and Docker Desktop's own virtual disk overhead. In Command
    Prompt, run `dir C:\` and check the "bytes free" line at the bottom
    before starting.

## Docker Hub Repository

Images are pulled from the `deepcse/himlt` repository on Docker Hub.

| Image | Tag |
|---|---|
| Web (Flask + Nginx + React) | `deepcse/himlt:web` |
| ML Worker (Random Forest) | `deepcse/himlt:worker` |
| Database (MySQL) | `deepcse/himlt:db` |

## Step 1 — Install Docker Desktop 
**WINDOWS**

1. Download from: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run the installer — during installation check both:
      - Use WSL2 instead of Hyper-V
      - Add shortcut to desktop
3. Restart your laptop when prompted
4. Open **Docker Desktop** and wait for **"Engine running"** at the bottom left

**MAC**

1. Download from: docker.com/products/docker-desktop
2. Choose Mac with Apple Silicon or Mac with Intel Chip depending on your machine
3. Open the .dmg file and drag Docker to Applications
4. Open Docker Desktop from Applications and wait for "Engine running" at the bottom left


## Step 2 — Open Command Prompt

**(Windows)** -> Press **Windows key** → type **cmd** → press **Enter**.

Create the project folder:

```cmd
mkdir C:\himlt
cd C:\himlt
```

**(Mac)** -> **Cmd + Space** → type **Terminal** → press Enter.

Create the project folder:

```cmd
mkdir C:\himlt
cd C:\himlt
```

### Step 3 — Download Deployment Files

```cmd
curl -O https://raw.githubusercontent.com/MachineVisionTeam/HIMLT_V2/main/HIMLT_Docker/docker-compose.yml
curl -O https://raw.githubusercontent.com/MachineVisionTeam/HIMLT_V2/main/HIMLT_Docker/.env.example
curl -O https://raw.githubusercontent.com/MachineVisionTeam/HIMLT_V2/main/HIMLT_Docker/README.md
```
`docker-compose.yml` , `.env.example`, `README.md` will be downloaded and verify  the files using list command(check in the hidden files for .env)
 **rename** `.env.example` to `.env`  by the below

**Windows**

```cmd
move .env.example .env
```

**Mac**

```cmd
mv .env.example .env
```
!!! note
    - Replace both `<choose_a_strong_password>` values with strong passwords.
    - Generate `SECRET_KEY` with:

   ```cmd
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

   Save the file .

!!! If the URL is ever unreachable, or you just want to see what's inside before pulling images, both files are reproduced below so you can create them by hand instead.(you can follow Step4 ,Step5 )

## Step 4 — Create `docker-compose.yml` Manually (Only if files from Github was unable to download)

**Windows**

```cmd
notepad docker-compose.yml
```
**Mac**

```cmd
nano docker-compose.yml
```

Click **Yes** or **ENTER** to create a new file, then paste:

```yaml
version: '3.8'
services:
  db:
    image: deepcse/himlt:db
    container_name: himlt_db
    restart: "no"
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - himlt_mysql_data:/var/lib/mysql
    ports:
      - "3307:3306"
    networks:
      - himlt_net
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    image: redis:7-alpine
    container_name: himlt_redis
    restart: "no"
    ports:
      - "6380:6379"
    networks:
      - himlt_net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  web:
    image: deepcse/himlt:web
    container_name: himlt_web
    restart: "no"
    env_file: .env
    environment:
      DB_HOST: db
      REDIS_HOST: redis
    ports:
      - "8080:80"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - himlt_net
    volumes:
      - himlt_checkpoints:/app/checkpoints

  worker:
    image: deepcse/himlt:worker
    container_name: himlt_worker
    restart: "no"
    env_file: .env
    environment:
      DB_HOST: db
      REDIS_HOST: redis
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - himlt_net
    volumes:
      - himlt_checkpoints:/app/checkpoints
      - himlt_images:/data/GBM_shared
    healthcheck:
      test: ["CMD", "test", "-f", "/data/GBM_shared/TCGA-19-2620-01Z-00-DX1.b52311cf-5861-4653-9d87-bcc3389874ef.tif"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 10s

  iipimage:
    image: iipsrv/iipsrv:latest
    container_name: himlt_iipimage
    restart: "no"
    environment:
      - IIIF_VERSION=3
      - CORS=*
    volumes:
      - himlt_images:/images:ro
    depends_on:
      worker:
        condition: service_healthy
    networks:
      - himlt_net

volumes:
  himlt_mysql_data:
    driver: local
  himlt_checkpoints:
    driver: local
  himlt_images:
    driver: local

networks:
  himlt_net:
    driver: bridge
```

Save via **File → Save As**, set "Save as type" to **All Files**, filename -> In **Windows**
Save with **Ctrl+O → Enter → Ctrl+X**. -> In **Mac**

!!! note
    Newer Docker Compose versions no longer need the top `version: '3.8'`
    line and will print a harmless deprecation warning about it — safe to
    ignore, or delete that line and the blank line after it.

## Step 5 — Create `.env` File manually(Only if files from Github was unable to download)

**Windows**

```cmd
notepad .env
```
**Mac**

```cmd
nano .env
```
Paste:

```text
# MySQL
MYSQL_ROOT_PASSWORD=<choose_a_strong_password>
DB_HOST=db
DB_PORT=3306
DB_NAME=histomics_db
DB_USER=newhistomics
DB_PASSWORD=<choose_a_strong_password>

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=''

# Flask
FLASK_ENV=production
SECRET_KEY=<generate_with_command_below>
DEBUG=False

# Data paths (do not change)
DATA_DIR=/data/
DATASET_DIR=/data/GBM

# Gunicorn
WORKERS=4
WORKER_CLASS=sync
TIMEOUT=300
```

Fill in the placeholders:

- Replace both `<choose_a_strong_password>` values with strong passwords.
- Generate `SECRET_KEY` with:

```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Save via **File → Save As**, "Save as type" **All Files**, filename `.env`.

!!!  "Security"
    Make a secure note of your passwords. Never share your `.env` file with
    anyone 

## Step 6 — Pull All Images

```cmd
docker-compose pull
```

Downloads 5 images automatically:

| Image | Approx. Size |
|---|---|
| `deepcse/himlt:web` | ~3.4 GB |
| `deepcse/himlt:worker` | ~5.2 GB |
| `deepcse/himlt:db` | ~786 MB |
| `redis:7-alpine` | ~40 MB |
| `iipsrv/iipsrv:latest` | ~12 MB |

Total download: ~9.5 GB uncompressed — typically 10–30 minutes depending on
connection speed.

## Step 7 — Start the Application

```cmd
docker-compose up -d
```

Monitor the first start:

```cmd
docker-compose logs -f web
```

Wait until you see:

```text
Nuclei import complete!
Starting Nginx and Flask...
```

Press `Ctrl+C` to stop watching logs (this only stops the log stream, not
the containers).

!!! warning "First start takes longer"
    3–5 minutes longer due to automatic nuclei data import. Do not restart
    during this time.


## Step 8 — Verify All Containers Are Running

```cmd
docker-compose ps
```

All 5 containers must show `Up` or `healthy`:

```text
himlt_db        Up (healthy)
himlt_redis     Up (healthy)
himlt_web       Up
himlt_worker    Up (healthy)
himlt_iipimage  Up
```

## Step 9 — Open in Browser

Open **Chrome** or **Edge** and go to:

```text
http://localhost:8080/himlt/
```


