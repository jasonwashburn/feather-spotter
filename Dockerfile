FROM python:3.11.4-slim-buster AS osbase

RUN apt-get update && \
    apt-get upgrade --yes && \
    apt-get install gcc libgl1 libglib2.0-0 --yes

RUN useradd --create-home fastapi
USER fastapi
WORKDIR /home/fastapi

FROM osbase AS pythonbase

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY --chown=fastapi:fastapi pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

FROM pythonbase AS builder

# Copy source code
COPY --chown=fastapi:fastapi README.md LICENSE.txt ./
COPY --chown=fastapi:fastapi src/ src/
COPY --chown=fastapi:fastapi tests/ tests/

# Install the package and run tests
RUN uv run python -m pip install . && \
    uv run python -m pytest tests/ && \
    uv run python -m ruff src/ && \
    uv run python -m black src/ --check && \
    uv run python -m bandit -r src/ --quiet && \
    uv build --wheel

FROM pythonbase AS app

# Copy the built wheel from builder
COPY --chown=fastapi:fastapi --from=builder /home/fastapi/dist/feather*.whl /home/fastapi/

# Install the wheel
RUN uv pip install --no-cache feather*.whl

CMD ["uv", "run", "uvicorn", "feather_spotter.app:app", "--host", "0.0.0.0", "--port", "8000"]
