FROM python:3.11-slim

WORKDIR /app


RUN pip install uv

COPY requirements.txt .
RUN uv pip install --system -e .

RUN uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["bash", "-c", "uvicorn src.backend:app --host 0.0.0.0 --port 8000 & python -mstreamlit run src/main.py --server.port 8501 --server.address 0.0.0.0"]