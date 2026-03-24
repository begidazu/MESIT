FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GDAL_DATA=/usr/local/lib/python3.11/site-packages/rasterio/gdal_data

WORKDIR /root

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

COPY requirements-docker.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt \
    && python -m pip install gunicorn

COPY . /root

EXPOSE 8050

ENTRYPOINT ["python", "run.py"]