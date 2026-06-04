# Docker Setup Guide

Complete guide for running the CV Interview Bot with Docker.

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v1.29+)
- 2GB+ available disk space

## Quick Start

```bash
# 1. Clone/navigate to the project
cd CV_Interview_Bot

# 2. Setup environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# 3. Build and run
docker-compose up --build
```

The application will be available at `http://localhost:8501`

## Using Make Commands

For convenience, use the included Makefile:

```bash
# Start the application
make up

# View logs
make logs

# Stop the application
make down

# Clean up everything
make clean

# Build the image
make build
```

## Docker Architecture

### Dockerfile

- **Base Image**: `python:3.11-slim` - Lightweight Python image
- **Work Directory**: `/app`
- **Dependencies**: Installed from `requirements.txt`
- **Port**: 8501
- **Health Check**: Built-in endpoint monitoring

### Docker Compose

Single service: `interview-bot`

**Ports**: Maps 8501 (host) → 8501 (container)

**Volumes**:
- `./data/resumes` - Persistent resume storage
- `./data/vector_db` - Persistent vector database
- `./outputs` - Generated outputs
- `./src` - Application code (hot reload for development)

**Environment**:
- Loads from `.env` file
- `PYTHONUNBUFFERED=1` - Unbuffered Python output

**Network**: `interview-network` (bridge)

**Restart Policy**: `unless-stopped`

## Managing Data

### Resume Storage
Uploaded resumes are stored in `data/resumes/`:
```bash
docker-compose exec interview-bot ls /app/data/resumes
```

### Vector Database
Embeddings are cached in `data/vector_db/`:
```bash
docker-compose exec interview-bot ls /app/data/vector_db
```

### Outputs
Generated results are saved to `outputs/`:
```bash
ls outputs/
```

## Common Tasks

### View Logs
```bash
# Follow logs in real-time
docker-compose logs -f interview-bot

# View last 100 lines
docker-compose logs --tail=100
```

### Execute Commands in Container
```bash
# Run a shell
docker-compose exec interview-bot bash

# Run Python commands
docker-compose exec interview-bot python -c "import flask; print(flask.__version__)"
```

### Restart Service
```bash
docker-compose restart interview-bot
```

### Rebuild After Code Changes
```bash
docker-compose up --build
```

## Troubleshooting

### Port 8501 Already in Use

**Option 1**: Change the port in `docker-compose.yml`
```yaml
ports:
  - "8502:8501"  # Use 8502 instead
```

**Option 2**: Stop the conflicting process
```bash
# macOS/Linux
lsof -i :8501
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Permission Denied
Run with `sudo`:
```bash
sudo docker-compose up
```

### Out of Memory
Increase Docker's memory allocation in Docker Desktop settings.

### Container Exits Immediately
Check logs:
```bash
docker-compose logs interview-bot
```

### API Key Issues
Verify `.env` file exists:
```bash
cat .env
```

Make sure `OPENAI_API_KEY` is set correctly.

## Development Workflow

### Live Code Reloading

The `./src` directory is volume-mounted, allowing live updates:

1. Edit files in `src/`
2. Flask reloads code when debug mode is enabled
3. Refresh the browser to apply changes

### Testing
```bash
docker-compose exec interview-bot python -m pytest tests/ -v
```

### Installing New Packages

1. Update `requirements.txt`
2. Rebuild the image:
   ```bash
   docker-compose up --build
   ```

## Deployment

### Production Considerations

1. **Environment Variables**: Use secrets management (AWS Secrets, etc.)
2. **Storage**: Use persistent volumes or cloud storage
3. **Scaling**: Use Kubernetes or container orchestration
4. **Monitoring**: Add logging and health check services

### Build Optimization

```bash
# Build with custom tag
docker build -t cv-interview-bot:v1.0 .

# Push to registry
docker push your-registry/cv-interview-bot:v1.0
```

## Cleanup

### Remove Containers and Images
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes data!)
docker-compose down -v

# Remove images
docker rmi cv-interview-bot
```

## Performance Tips

1. **Use .dockerignore** - Reduces build context
2. **Multi-stage builds** - Keep images lean
3. **Cache layers** - Order Dockerfile for efficiency
4. **Health checks** - Monitor container health

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
