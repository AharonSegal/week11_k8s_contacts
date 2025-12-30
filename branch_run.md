# This branch goal is Local FastAPI + MongoDB in Docker container (no port conflict)

### Run MongoDB container on a different host port
```bash
# Expose container port 27017 as host port 27018
docker run -d --name mongodb_container -p 27018:27017 mongo:latest
````
### Environment variables for FastAPI

# Connect FastAPI to the container on port 27018
MONGO_URI="mongodb://localhost:27018"
DB_NAME="fastapi_db_container"
cat .env


### Run FastAPI locally

```bash
uvicorn app.main:app --reload
```

### Stop and remove MongoDB container when done

```bash
docker stop mongodb_container
docker rm mongodb_container
```
View and inspect MongoDB container
# Check running containers
docker ps

# View container logs
docker logs mongodb_container

# Open Mongo shell inside the container
docker exec -it mongodb_container mongosh

# Show databases in the container
show dbs

# Switch to your FastAPI database
use fastapi_db_container

# Show collections in that database
show collections
db.items.find().pretty()





