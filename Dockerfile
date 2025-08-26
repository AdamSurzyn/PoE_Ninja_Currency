FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONBUFFERED=1 \ 
    PYTHONPATH=/app:/app/src
RUN useradd -m appuser

WORKDIR /app

COPY requirements/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

CMD ["python", "standalone/extract_run.py"]