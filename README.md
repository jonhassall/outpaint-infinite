# Infinite Outpaint Explorer (Docker Compose + GPU)

This project runs a Gradio Web UI inside a Docker Compose service, executing the Krea2 Outpaint model in an infinite loop. It automatically crops and saves frames, and allows you to download them as a ZIP directly from the UI.

## Prerequisites
- Docker installed
- NVIDIA GPU with Docker CUDA Toolkit installed (`nvidia-container-toolkit`)

## Setup Instructions

1. Create your local environment file:
   ```bash
   cp .env.example .env
   ```

2. (Optional) Edit ports in `.env`:
   - `PUBLIC_PORT`: Port exposed on your machine
   - `APP_PORT`: Port used by Gradio inside the container

3. Build and start with Docker Compose:
   ```bash
   docker compose up --build
   ```

4. To run in detached mode:
   ```bash
   docker compose up --build -d
   ```

5. Open your browser:
   Go to `http://localhost:${PUBLIC_PORT}` (default: `http://localhost:7860`)

6. Stop the service:
   ```bash
   docker compose down
   ```

## Usage
1. Upload a starting 1024x1024 image.
2. Click **Start Journey** to begin generating infinite outpainting.
3. Click **Stop** whenever you're satisfied.
4. Click **Prepare ZIP Download** to grab all the frames generated during the session.
