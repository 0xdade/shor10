FROM python:3.12-slim-bookworm

# It's best practice to pin uv versions but YOLO
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV SHOR10_URLS=/data/shor10_urls.json
COPY pyproject.toml uv.lock app.py ./
COPY templates ./templates/
RUN uv sync --frozen

EXPOSE 8000
VOLUME /data
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:8000", "app:app"]
