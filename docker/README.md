# Docker instructions for serving models

This folder contains example Dockerfiles and a `docker-compose` fragment to run the FastAPI model server included in the repository.

Quick overview
- `Dockerfile.cpu` - lightweight CPU image using `python:3.12-slim`.
- `Dockerfile.gpu` - base image for systems with NVIDIA GPUs (uses a PyTorch CUDA runtime image).
- `docker-compose.model.yml` - example compose file that mounts a Docker volume named `ai-models` to `/root/.cache/huggingface` inside the container.

Recommended workflow

1) Download model to host cache (if you have enough disk and prefer offline):

```bash
# Run the project's model setup script on the host (this stores the model under ~/.cache/huggingface/hub)
bash setup-models.sh

# Create a docker volume and copy the HF cache into it (adjust paths if needed)
docker volume create ai-models
docker run --rm -v ai-models:/models -v $HOME/.cache/huggingface:/cache alpine sh -c "cp -r /cache /models || true"
```

2) Start the service (compose file lives under `docker/docker-compose.model.yml`):

```bash
# From repo/docker directory
docker compose -f docker-compose.model.yml up -d --build
```

3) Optional: If your model is stored inside the HF cache under a model-specific folder, set `MODEL_DIR` env to that folder.
   Example: `MODEL_DIR=/root/.cache/huggingface/hub/repo_name` or the exact model folder inside the volume.

Notes on `MODEL_DIR` and `HF_HOME`
- `HF_HOME` points to the Hugging Face cache root. The `main.py` loader prefers a `MODEL_DIR` that points directly
  at a model folder (the folder that contains `config.json`, `tokenizer.json`/`tokenizer_config.json`, and weights files).
- If you do not set `MODEL_DIR`, the app will attempt to download the model from Hugging Face using `MODEL_NAME`.

GPU support
- `Dockerfile.gpu` installs `accelerate` and `bitsandbytes` to support large-model optimizations; to run it, use a host with NVIDIA drivers
  and start the container with the appropriate runtime (Docker >= 20.10 can use `--gpus all`). Example compose changes are left as an exercise
  because CUDA image tags and host driver versions vary between systems.

Security & size considerations
- Model images and caches are large; keep model cache on a persistent volume and avoid baking very large model weights into image layers.
