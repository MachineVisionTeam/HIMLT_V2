# HIMLT — Hybrid Interactive Machine Learning Tool
**For Histopathology Image Analysis**

HIMLT is a web-based active learning platform for nuclei classification in whole-slide histopathology images using Random Forest classification with iterative learning.

---

## Docker Hub Repository

Images are publicly available on Docker Hub — no login required:

| Image                      | Tag               |
|----------------------------|-------------------|
| Web (Flask + Nginx + React)| `deepcse/himlt:web` |
| ML Worker (Random Forest)  | `deepcse/himlt:worker` |
| Database (MySQL)           | `deepcse/himlt:db` |

---

## System Requirements

| Component    | Minimum | Recommended |
|--------------|---------|-------------|
| RAM          | 8GB     | 16GB+       |
| Disk Space   | 15GB free| 20GB+ free |
| OS           | Windows 10/11 | Windows 11 |
| CPU          | 4 cores | 8+ cores |

---

## Deployment Steps

### Step 1 — Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop
2. Run the installer — during installation check both:
   - Use WSL2 instead of Hyper-V
   - Add shortcut to desktop
3. Restart laptop when prompted
4. Open **Docker Desktop** and wait for **"Engine running"** at bottom left

---

### Step 2 — Open Command Prompt

Press **Windows key** → type **cmd** → press **Enter**

Create project folder:
```cmd
mkdir C:\himlt
cd C:\himlt
```

---

### Step 3 — Download Deployment Files

```cmd
curl -O https://raw.githubusercontent.com/MachineVisionTeam/HIMLT_V2/main/HIMLT_Docker/docker-compose.yml
curl -O https://raw.githubusercontent.com/MachineVisionTeam/HIMLT_V2/main/HIMLT_Docker/.env.example
curl -O https://raw.githubusercontent.com/MachineVisionTeam/HIMLT_V2/main/HIMLT_Docker/README.md
```

---

### Step 4 — Create `.env` File

```cmd
copy .env.example .env
vi .env
```

- Fill in strong passwords for `MYSQL_ROOT_PASSWORD` and `DB_PASSWORD`
- Generate a secret key and paste as `SECRET_KEY`:

```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

- Press **Ctrl+S** to save and close Notepad

> Make a note of your passwords.
> Never share your `.env` file with anyone.

---

### Step 5 — Pull All Images

```cmd
docker-compose pull
```

Downloads 5 images automatically:

| Image                    |
|--------------------------|
| `deepcse/himlt:web` |
| `deepcse/himlt:worker`|
| `deepcse/himlt:db`    | 
| `redis:7-alpine`           |
| `iipsrv/iipsrv:latest`      |


---

### Step 6 — Start the Application

```cmd
docker-compose up -d
```

Monitor the first start:
```cmd
docker-compose logs -f web
```

Wait until you see:
```
Nuclei import complete!
Starting Nginx and Flask...
```

Press **Ctrl+C** to stop watching logs.

> ⏱️ First start takes 3–5 minutes longer due to automatic nuclei data import. Do not restart during this time.

---

### Step 7 — Verify All Containers Are Running

```cmd
docker-compose ps
```

All 5 containers must show `Up` or `healthy`:
```
himlt_db        Up (healthy)
himlt_redis     Up (healthy)
himlt_web       Up
himlt_worker    Up (healthy)
himlt_iipimage  Up
```

---

### Step 8 — Open in Browser

Open **Chrome** or **Edge** and go to:
```
http://localhost:8080/himlt/
```

---

## Using the Application

```
1. Select Dataset  →  GBM
2. Select Slide    →  TCGA-19
3. Click Show Nuclei   →  nuclei boundaries load on image
4. Click Positive      →  click 4 nuclei on image
5. Click Negative      →  click 4 nuclei on image
6. Click Train Model   →  trains in under 1 second
7. View predictions    →  color-coded on all nuclei
8. Repeat steps 4-7    →  refine model (iterative learning)
```

### Color Legend

| Color                 |             Meaning               |
|-----------------------|-----------------------------------|
| Yellow dots           |         Unselected nucleus        |
| Orange + green border | Selected positive training sample |
| Orange + red border   | Selected negative training sample |
| Magenta               | Predicted positive nucleus        |
| Cyan                  | Predicted negative nucleus        |

---

## Daily Commands

```cmd
cd C:\himlt

:: Start application
docker-compose up -d

:: Stop application
docker-compose down

:: View live logs
docker-compose logs -f

:: Check container status
docker-compose ps
```

---

## Troubleshooting

| Problem                      |                Solution                 |
|------------------------------|-----------------------------------------|
| Docker Desktop not starting  | Restart laptop and reopen Docker Desktop |
| `docker-compose` not found   | Restart Command Prompt after Docker installation |
| Containers not starting      | Run `docker-compose logs` |
| Image not loading in browser | Run `docker-compose restart iipimage` |
| Nuclei not showing           | Run `docker-compose logs web` |
| Worker keeps restarting      | Run `docker-compose logs worker` |
| Port 8080 already in use     | Change `"8080:80"` to `"9090:80"` in `docker-compose.yml` |
| Need a fresh start           | Run `docker-compose down -v` then `docker-compose up -d` |

---

## Architecture

| Component   |           Technology            |
|-------------|---------------------------------|
| Frontend    | React + TypeScript + OpenSeadragon |
| Backend     | Flask + Gunicorn |
| Database    | MySQL  |
| Job Queue   | Redis |
| ML Engine   | Random Forest |
| Image Server| IIPImage v1.3 |
| Web Server  | Nginx |

---

## Support

For issues please open a GitHub issue:
https://github.com/MachineVisionTeam/HIMLT_V2/issues
