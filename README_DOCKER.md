# Docker Setup Guide for Simple-Bot

This guide explains how to run Simple-Bot using Docker and Docker Compose.

## Architecture

- **Backend**: FastAPI service running on port 8000
- **Frontend**: Streamlit service running on port 8501
- **Network**: Both services communicate via Docker internal network

## Prerequisites

- Docker installed (https://docs.docker.com/get-docker/)
- Docker Compose installed (usually comes with Docker Desktop)
- API keys set in `.env` file

## Quick Start

1. **Ensure API keys are configured** in your `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

2. **Build and run the containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - **Frontend UI**: http://localhost:8501
   - **Backend API**: http://localhost:8000
   - **Health Check**: http://localhost:8000/health

4. **Stop the containers**:
   ```bash
   docker-compose down
   ```

## Development Mode

To enable live code reloading during development:

1. Uncomment the volume mount for frontend in `docker-compose.yml` if needed
2. Run with development flags:
   ```bash
   docker-compose up --build
   ```

## Services

### Backend Service (simplebot-backend)
- **Port**: 8000
- **API Endpoint**: `/chat`
- **Health Check**: `/health`
- **Environment**: Uses all variables from `.env` file

### Frontend Service (simplebot-frontend)
- **Port**: 8501
- **URL**: http://localhost:8501
- **Dependencies**: Requires backend service to be healthy before starting
- **Backend URL**: Automatically configured to use Docker networking

## Environment Variables

Required environment variables (must be in `.env` file):

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM model | Yes |
| `TAVILY_API_KEY` | Tavily API key for web search | Yes |
| `NVIDIA_API_KEY` | NVIDIA API key (optional) | No |
| `OPEN_ROUTER_API_KEY` | OpenRouter API key (optional) | No |

## Troubleshooting

### Frontend can't connect to backend
- Ensure both services are running: `docker-compose ps`
- Check backend health: `curl http://localhost:8000/health`
- Check logs: `docker-compose logs backend`

### API key errors
- Verify `.env` file exists in project root
- Check that required keys are set correctly
- Restart containers after changing `.env`: `docker-compose down && docker-compose up --build`

### Port conflicts
- Ensure ports 8000 and 8501 are not in use by other applications
- Modify `docker-compose.yml` ports mapping if needed

## Production Considerations

For production deployment:

1. **Remove secrets from images**: Mount `.env` file instead of building it into images
2. **Use Docker secrets**: Consider using Docker secrets for sensitive data
3. **Database persistence**: Add volume mounts for data persistence
4. **Reverse proxy**: Place nginx in front of services
5. **SSL certificates**: Add certificates for HTTPS
6. **Resource limits**: Set CPU and memory limits per container

## Commands Reference

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart

# Stop and remove containers
docker-compose down

# Stop but keep volumes
docker-compose down --volumes

# Rebuild from scratch
docker-compose build --no-cache
```

## Docker Image Sizes

- Backend image: ~200MB (multi-stage build optimized)
- Frontend image: ~200MB (multi-stage build optimized)

Total: ~400MB for both services
