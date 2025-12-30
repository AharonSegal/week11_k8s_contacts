<!-- 
███████ ███████ ████████ ██    ██ ██████  
██      ██         ██    ██    ██ ██   ██ 
███████ █████      ██    ██    ██ ██████  
     ██ ██         ██    ██    ██ ██      
███████ ███████    ██     ██████  ██      
                                           -->
                                           
```bash

git init
python -m venv venv
source venv/Scripts/activate
source ../venv/Scripts/activate
python.exe -m pip install --upgrade pip

pip install fastapi uvicorn pydantic
pip install requests
pip install --upgrade mysql-connector-python
pip install python-dotenv

python -c "import fastapi; print(fastapi.__version__)"
python -c "import uvicorn; print(uvicorn.__version__)"
python -c "import requests; print(requests.__version__)"
python -c "import mysql.connector; print(mysql.connector.__version__)"
python -c "import importlib.metadata as m; print(m.version('python-dotenv'))"

pip freeze > requirements.txt
git add .  
git commit -m "initial commit"
git push -u origin main

uvicorn main:app --reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8090

http://127.0.0.1:8000/docs#/
```

<!-- 
██████   ██████   ██████ ██   ██ ███████ ██████              
██   ██ ██    ██ ██      ██  ██  ██      ██   ██             
██   ██ ██    ██ ██      █████   █████   ██████              
██   ██ ██    ██ ██      ██  ██  ██      ██   ██             
██████   ██████   ██████ ██   ██ ███████ ██   ██             
                                                             
                                                             
 ██████  ██████  ███    ███ ██████   ██████  ███████ ███████ 
██      ██    ██ ████  ████ ██   ██ ██    ██ ██      ██      
██      ██    ██ ██ ████ ██ ██████  ██    ██ ███████ █████   
██      ██    ██ ██  ██  ██ ██      ██    ██      ██ ██      
 ██████  ██████  ██      ██ ██       ██████  ███████ ███████ 
                                                             
                                           -->

# 🐳 Docker Command Lifecycle (Short)

build → image  
up / run → container  
start → existing container  
stop → container only  
down → remove container  
down -v → remove container + volumes  

## How Long Things Live in Docker
image     → reusable
container → temporary
volume    → persistent
### Start & Build


<!-- 
███████ ██    ██ ███    ██ ████████  █████  ██   ██ 
██       ██  ██  ████   ██    ██    ██   ██  ██ ██  
███████   ████   ██ ██  ██    ██    ███████   ███   
     ██    ██    ██  ██ ██    ██    ██   ██  ██ ██  
███████    ██    ██   ████    ██    ██   ██ ██   ██  -->
                                                    
                                                    

# 🐳 Docker Compose File Syntax Cheat Sheet
version: "3.9"  # Compose file version

# ===================================================
# Volumes: persistent data storage for databases
# ===================================================
volumes:
  mysql_data:   # Named volume for MySQL data
    driver: local

# ===================================================
# Networks: define isolated network for services
# ===================================================
networks:
  app-network:
    driver: bridge

# ===================================================
# Services: define containers
# ===================================================
services:

  # -------------------- MySQL Database --------------------
  database:
    image: mysql:8                      # Use official MySQL 8 image
    container_name: mysql_db
    restart: unless-stopped             # Restart automatically unless stopped manually

    # -------------------- Environment variables --------------------
    environment:
      MYSQL_ROOT_PASSWORD: ${ROOT_PASS}  # Root password
      MYSQL_DATABASE: ${DB_NAME}         # Initial database
      MYSQL_USER: ${DB_USER}             # Optional: additional user
      MYSQL_PASSWORD: ${DB_PASSWORD}     # Optional: additional user password
    env_file:                             # Alternative: load from .env file
      - .env

    # -------------------- Port mapping --------------------
    ports:
      - "3307:3306"   # HOST:CONTAINER mapping; 3307 on host, 3306 inside container

    # -------------------- Volumes --------------------
    volumes:
      - mysql_data:/var/lib/mysql       # Persistent DB storage
      - ./app/sql/init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # Initialize DB

    # -------------------- Healthcheck --------------------
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

    networks:
      - app-network

  # -------------------- FastAPI Backend --------------------
  backend:
    build:
      context: ./app                      # Dockerfile context
      dockerfile: Dockerfile
    container_name: backend_api
    restart: unless-stopped
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    # -------------------- Environment --------------------
    environment:
      DB_HOST: database                     # Link to MySQL service
      DB_PORT: 3306                         # Internal MySQL port
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
    env_file:
      - .env

    # -------------------- Port mapping --------------------
    ports:
      - "8000:8000"   # HOST:CONTAINER; FastAPI accessible on localhost:8000

    # -------------------- Dependencies --------------------
    depends_on:
      database:
        condition: service_healthy       # Wait for DB to be healthy before starting

    # -------------------- Volumes --------------------
    volumes:
      - ./app:/app                         # Mount app source code for live reload

    networks:
      - app-network

  # -------------------- Optional: Adminer (DB GUI) --------------------
  adminer:
    image: adminer
    container_name: adminer_gui
    restart: unless-stopped
    ports:
      - "8080:8080"   # Access Adminer on localhost:8080
    depends_on:
      - database
    networks:
      - app-network

# ===================================================
# Notes:
# 1. Use environment variables via .env for sensitive info
# 2. Volumes ensure database persists even if container is removed
# 3. Healthchecks help orchestrate service dependencies
# 4. Mounting ./app allows live reload during development
# 5. `depends_on` ensures proper startup order
# 6. Adminer is optional, helpful for GUI DB management
# 7. Use `docker-compose up --build` to rebuild images after changes
# ===================================================

---

## 📄 Version Declaration

```yaml
version: '3.8'   # Compose file version (2.x, 3.x)
````
## 🧩 Top-Level Keys

 Key        | Description                                   |
 ---------- | --------------------------------------------- |
 `services` | Defines containers to run (mandatory).        |
 `volumes`  | Defines named volumes for persistent storage. |
 `networks` | Defines custom networks.                      |
 `configs`  | Defines configs (v3.3+).                      |
 `secrets`  | Defines secrets for secure data (v3.1+).      |

---

## 🏷 Services Syntax

```yaml
services:
  web:
    image: nginx:alpine          # Docker image to use
    build: ./path                # Build context (can also include Dockerfile)
    container_name: my_container # Optional custom name
    ports:                       # Map host:container ports
      - "8080:80"
    environment:                 # Environment variables
      - DEBUG=true
    volumes:                     # Mount host or named volumes
      - ./index.html:/usr/share/nginx/html/index.html:ro
    networks:                    # Assign to networks
      - frontend
    depends_on:                  # Control start order
      - db
    command: ["npm", "start"]    # Override default container command
    entrypoint: /bin/sh           # Override default entrypoint
    restart: always              # Restart policy: no, always, on-failure, unless-stopped
    healthcheck:                 # Optional container health check
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      retries: 3
      timeout: 10s

~ IN DETAIL ~
healthcheck:                 # Optional container health check to determine if the container is "healthy"
  test: ["CMD", "curl", "-f", "http://localhost"]  
  # 'test' defines the command Docker runs to check health.
  # Here it uses `curl -f http://localhost` inside the container.
  # The "CMD" form runs a command inside the container (as opposed to "CMD-SHELL").

  interval: 30s  
  # How often to run the health check. In this example, every 30 seconds.

  timeout: 10s  
  # Maximum time allowed for the health check command to complete.
  # If it takes longer than this, Docker considers it a failure.

  retries: 3  
  # Number of consecutive failures required before marking the container as unhealthy.

```

---

## 💾 Volumes Syntax

```yaml
volumes:
  my_data:        # Named volume
    driver: local # Optional driver
    driver_opts:
      type: none
      device: /path/on/host
      o: bind
```

---

## 🌐 Networks Syntax

```yaml
networks:
  frontend:
    driver: bridge   # Options: bridge, overlay, macvlan
  backend:
    driver: overlay
```

---

## 🔑 Environment & Secrets

```yaml
environment:
  - VAR_NAME=value
  - OTHER_VAR=123

secrets:
  my_secret:
    file: ./secret.txt
```

---

## 🔄 Deployment (v3+ for Swarm)

```yaml
deploy:
  replicas: 3
  restart_policy:
    condition: on-failure
  resources:
    limits:
      cpus: "0.5"
      memory: 512M
```

---

## 🛠 Other Useful Keys

| Key                  | Description                                 |
| -------------------- | ------------------------------------------- |
| `build.context`      | Path to Dockerfile context.                 |
| `build.dockerfile`   | Specify Dockerfile name.                    |
| `labels`             | Add metadata labels.                        |
| `extra_hosts`        | Add host-to-IP mappings.                    |
| `working_dir`        | Set working directory inside container.     |
| `user`               | Set container user.                         |
| `stdin_open` / `tty` | Keep container interactive (for debugging). |
| `logging`            | Configure logging driver and options.       |
| `tmpfs`              | Mount temporary filesystem.                 |

---

### 🔍 Notes

* Keys like `depends_on`, `volumes`, `networks`, `environment`, `ports`, `restart`, and `healthcheck` are **the most commonly used**.
* Indentation matters! YAML is **space-sensitive**, use 2 spaces per level.
* You can combine multiple `docker-compose.yml` files using `-f` flag for production overrides.

<!-- ---

 ██████  ██████  ███    ███ ███    ███  █████  ███    ██ ██████  ███████ 
██      ██    ██ ████  ████ ████  ████ ██   ██ ████   ██ ██   ██ ██      
██      ██    ██ ██ ████ ██ ██ ████ ██ ███████ ██ ██  ██ ██   ██ ███████ 
██      ██    ██ ██  ██  ██ ██  ██  ██ ██   ██ ██  ██ ██ ██   ██      ██ 
 ██████  ██████  ██      ██ ██      ██ ██   ██ ██   ████ ██████  ███████ 
                                                                         
                                                                          -->

# 🐳 Docker Compose Commands Cheat Sheet

## ⚡ Basic Commands

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start services defined in `docker-compose.yml`. Creates containers if needed. |
| `docker-compose up -d` | Start services in **detached/background** mode. |
| `docker-compose down` | Stop and remove containers, networks, and default volumes created by `up`. |
| `docker-compose down -v` | Stop and remove containers **and volumes**. |
| `docker-compose restart` | Restart services. |

---

## 🔧 Building & Updating

| Command | Description |
|---------|-------------|
| `docker-compose build` | Build or rebuild services. |
| `docker-compose up --build` | Build services before starting containers. |
| `docker-compose pull` | Pull updated images from Docker Hub. |
| `docker-compose push` | Push built images to a registry. |

---

## 📋 Inspect & Logs

| Command | Description |
|---------|-------------|
| `docker-compose ps` | List all containers managed by Compose. |
| `docker-compose logs` | View logs for all services. |
| `docker-compose logs -f` | Follow logs in real-time. |
| `docker-compose config` | Validate and view the full config. |
| `docker-compose top` | Display running processes inside containers. |

---

## 🧹 Cleanup & Maintenance

| Command | Description |
|---------|-------------|
| `docker-compose rm` | Remove stopped containers. |
| `docker-compose down` | Stop and remove containers, networks, and default volumes. |
| `docker-compose down -v` | Stop and remove containers **and volumes**. |
| `docker volume ls` | List all volumes. |
| `docker volume prune` | Remove unused volumes. |
| `docker network ls` | List Docker networks. |
| `docker network prune` | Remove unused networks. |

---

## 🔀 Service Control

| Command | Description |
|---------|-------------|
| `docker-compose stop <service>` | Stop a specific service container. |
| `docker-compose start <service>` | Start a stopped service container. |
| `docker-compose restart <service>` | Restart a specific service container. |
| `docker-compose up --force-recreate` | Recreate containers even if their configuration didn’t change. |
| `docker-compose scale <service>=<n>` | Set number of container replicas (v2 syntax; in v3 use `replicas` in `deploy`). |

---

## 🌐 Misc / Advanced

| Command | Description |
|---------|-------------|
| `docker-compose exec <service> <command>` | Run a command inside a running container. |
| `docker-compose run <service> <command>` | Run a **one-off** command in a new container. |
| `docker-compose pause <service>` | Pause a running service. |
| `docker-compose unpause <service>` | Unpause a paused service. |
| `docker-compose config --services` | List all service names defined in the file. |
| `docker-compose config --volumes` | List all volumes defined in the file. |

<!-- __ _               
                          
 ██████ ██    ██  ██████ ██      ███████ 
██       ██  ██  ██      ██      ██      
██        ████   ██      ██      █████   
██         ██    ██      ██      ██      
 ██████    ██     ██████ ███████ ███████ 
                                         
                                         
                       -->

## Final Docker Compose Cheat Sheet

```bash
# Lifecycle Commands
# builds images if needed + creates and runs containers + sets up networks/volumes. 
# ✅ This is what you use most of the time.
docker-compose up              # Start services
docker-compose up -d           # Start in background
docker-compose down            # Stop and remove containers
docker-compose down -v         # Also remove volumes
docker-compose restart         # Restart all services
docker-compose pause           # Pause services
docker-compose unpause         # Unpause services

# builds images only, no containers.
# Use build manually only for pre-building, debugging, or forcing rebuilds.
docker-compose build           # Build all images
docker-compose build --no-cache # Build without cache
docker-compose pull            # Pull all images

# Inspection
docker-compose ps              # List containers
docker-compose top             # Display running processes
docker-compose logs            # View logs
docker-compose logs -f         # Follow logs
docker-compose config          # Validate and view config

# Execution
docker-compose exec <service> <command>  # Run command
docker-compose run <service> <command>   # Run one-off command

# Scaling
docker-compose up -d --scale api=3      # Run 3 instances of api
```

<!-- __ _               
                          
███████ ██       ██████  ██     ██ 
██      ██      ██    ██ ██     ██ 
█████   ██      ██    ██ ██  █  ██ 
██      ██      ██    ██ ██ ███ ██ 
██      ███████  ██████   ███ ███  
                                   
                       -->
                      



<!-- 
██████  ███████ ████████  █████  ██ ██      
██   ██ ██         ██    ██   ██ ██ ██      
██   ██ █████      ██    ███████ ██ ██      
██   ██ ██         ██    ██   ██ ██ ██      
██████  ███████    ██    ██   ██ ██ ███████ 
                            -->
                           
## 📦 Initial State (Before Anything)

**Docker has:**
- ❌ No running containers
- ❌ No stopped containers
- ❌ No volumes (unless created earlier)
- ❌ No images (unless built earlier)

---

# 🛠️ Development Mode (Local)

📂 Uses:
- `docker-compose.yml`
- `docker-compose.override.yml` (applied automatically)

💾 Storage:
- **Bind mount** → local filesystem (live DB on your PC)

---

## ▶️ Start & Build (Dev)

```bash
docker-compose up --build
````

### What Docker does

* Builds a **Docker image** from `Dockerfile`
* Creates **1 container** from that image
* Mounts local DB folder into container
* Starts the container in foreground

### What you have now

* ✅ **Running container** (dev)
* ✅ **Built image**
* ❌ No Docker volumes
* ✅ DB lives on **local filesystem**
* 🔄 Only the DB is updating live
* 🧱 Code changes require a rebuild

---

## ▶️ Start in Background (Dev)

```bash
docker-compose up -d
```

### What Docker does

* Reuses the **existing image**
* Starts container in detached mode

### What you have now

* ✅ **Running container (background)**
* ✅ **Image still exists**
* ❌ No volumes
* ✅ Local DB still mounted

---

## ⏹️ Stop Dev Containers (Keep Image)

```bash
docker-compose down
```

### What Docker does

* Stops the container
* Removes the container
* Removes the network

### What Docker does NOT do

* ❌ Does NOT delete the image
* ❌ Does NOT touch your local DB

### What you have now

* ❌ No running containers
* ❌ No stopped containers
* ✅ **Image still exists**
* ❌ No volumes
* ✅ Local DB still on disk

---

## 📄 View Logs (When Running)

```bash
docker-compose logs -f
```
* Container must be running

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# 🚀 Production Mode (Final)

Used for deployment or final testing.

📂 Uses:

* `docker-compose.yml`
* `docker-compose.prod.yml`

💾 Storage:

* **Named Docker volume**
* Isolated from local filesystem

---

## ▶️ Start & Build (Prod)

```bash
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  up -d --build
```

### What Docker does

* Reuses or rebuilds the **same image**
* Creates a **new container (prod)**
* Creates a **named Docker volume**
* Mounts volume into `/app/db`
* Exposes port 80

### What you have now

* ✅ **Running prod container**
* ✅ **Image exists**
* ✅ **Named volume exists**
* ❌ No local DB involvement
* 🔒 Data stored inside Docker volume

---

## ⏹️ Stop Prod Containers (Keep Data)

```bash
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  down
```

### What Docker does

* Stops prod container
* Removes container & network

### What Docker does NOT do

* ❌ Does NOT remove image
* ❌ Does NOT remove volume

### What you have now

* ❌ No running containers
* ❌ No stopped containers
* ✅ **Image exists**
* ✅ **Volume exists with data**

---

## 📦 Check Volumes

```bash
docker volume ls
```

### What you see

* `prod_db` (or similar)

This volume contains your **production database**.

---

## 💣 Reset Production (Wipe Data)

```bash
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  down -v
```

### What Docker does

* Stops container
* Removes container
* Removes network
* ❌ **Deletes the volume**

### What you have now

* ❌ No containers
* ✅ Image still exists
* ❌ Volume deleted
* ❌ All prod data lost

---

# 🔍 Maintenance & Inspection

## See Running Containers

```bash
docker ps
```

---

## Inspect Database Inside Container

```bash
docker exec -it <container_name> sh
```

```bash
ls /app/db
cat /app/db/database.json
```

---

# 🧠 Key Rules to Remember

* `docker-compose down`
  ➜ removes containers, **keeps images & volumes**

* `docker-compose down -v`
  ➜ removes containers **and volumes**

* Images persist until:

  ```bash
  docker rmi <image>
  ```
  ```

* Dev uses **bind mounts**

* Prod uses **named volumes**

* Same image, different storage


<!-- 
 ██████ ██      ███████  █████  ██████  
██      ██      ██      ██   ██ ██   ██ 
██      ██      █████   ███████ ██████  
██      ██      ██      ██   ██ ██   ██ 
 ██████ ███████ ███████ ██   ██ ██   ██ 
                                         -->

## Cleanup

When you're done with the exercise:

```bash
# Stop and remove everything
docker-compose down -v

# Remove orphaned images
docker image prune

# Remove all unused resources
docker system prune -a
       
### **1️⃣ Bash Script: `docker-clean.sh`**

#!/bin/bash

#!/bin/bash

echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || true

echo "Removing all containers..."
docker rm $(docker ps -a -q) 2>/dev/null || true

echo "Removing all images..."
docker rmi -f $(docker images -q) 2>/dev/null || true

echo "Removing all volumes..."
# Remove volumes only if they exist
volumes=$(docker volume ls -q)
if [ ! -z "$volumes" ]; then
  docker volume rm $volumes 2>/dev/null || true
fi

echo "Removing all custom networks..."
# Keep default networks (bridge, host, none)
networks=$(docker network ls -q | grep -v -E "bridge|host|none")
if [ ! -z "$networks" ]; then
  docker network rm $networks 2>/dev/null || true
fi

echo "Full Docker cleanup complete!"
docker system prune -af --volumes
