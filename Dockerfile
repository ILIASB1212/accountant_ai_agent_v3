FROM python:3.11-slim

WORKDIR /app
# PYTHONPATH replaces the old `pip install -e .` (which ran before setup.py was copied into the image)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

RUN pip install --no-cache-dir uv

# CPU-only PyTorch. The default Linux wheel pulls ~3 GB of CUDA libraries Cloud Run cannot use.
# (the guardrails validators depend on torch)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .
#
# Download the guardrail models while building, so they are not fetched on every cold start.
# If this step fails the build still succeeds; the models are then downloaded at first start.
RUN python -c "import src.protection_rail.guard" || echo "guard warm-up skipped"

# Cloud Run sends traffic to $PORT (8080). One process per container: the API.
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn src.backend:app --host 0.0.0.0 --port ${PORT}"]