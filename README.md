# Infinite Outpaint Explorer (Docker + GPU)

This project runs a Gradio Web UI inside a Docker container, executing the Krea2 Outpaint model in an infinite loop. It automatically crops and saves frames, and allows you to download them as a ZIP directly from the UI.

## Prerequisites
- Docker installed
- NVIDIA GPU with Docker CUDA Toolkit installed (`nvidia-container-toolkit`)

## Setup Instructions

1. Build the Docker image:
   ```bash
   docker build -t krea2-infinite-outpaint .
   ```

2. Run the container:
   ```bash
   docker run --gpus all -p 7860:7860 -it krea2-infinite-outpaint
   ```

3. Open your browser:
   Go to `http://localhost:7860`

## Usage
1. Upload a starting 1024x1024 image.
2. Click **Start Journey** to begin generating infinite outpainting.
3. Click **Stop** whenever you're satisfied.
4. Click **Prepare ZIP Download** to grab all the frames generated during the session.
