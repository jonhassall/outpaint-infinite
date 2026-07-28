# Use official PyTorch image with CUDA support
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# System dependencies for OpenCV/Image processing
RUN apt-get update && apt-get install -y wget git libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Install Python stack
RUN pip install diffusers transformers accelerate safetensors huggingface_hub pillow gradio gradio_client

# Download the required proprietary scripts from the Krea2 HF repository
RUN wget https://huggingface.co/yijunwang2/krea2-outpaint/resolve/main/pipeline.py && \
    wget https://huggingface.co/yijunwang2/krea2-outpaint/resolve/main/outpaint.py && \
    wget https://huggingface.co/yijunwang2/krea2-outpaint/resolve/main/example.py

COPY app.py /app/app.py

ENV APP_PORT=7860

EXPOSE ${APP_PORT}

CMD ["python", "app.py"]
