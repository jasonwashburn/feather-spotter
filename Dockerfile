FROM python:3.11.4-slim-buster as osbase

RUN apt-get update && \
    apt-get upgrade --yes && \
    apt-get install gcc libgl1 libglib2.0-0 --yes

RUN useradd --create-home fastapi
USER fastapi
WORKDIR /home/fastapi

FROM osbase as pythonbase

ENV VIRTUALENV=/home/fastapi/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=fastapi:fastapi requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

FROM pythonbase as builder

COPY --chown=fastapi:fastapi requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY --chown=fastapi:fastapi pyproject.toml README.md LICENSE.txt ./
COPY --chown=fastapi:fastapi src/ src/
COPY --chown=fastapi:fastapi tests/ tests/

RUN python -m pip install . && \
    python -m pytest tests/ && \
    python -m ruff src/ && \
    python -m black src/ --check && \
    python -m bandit -r src/ --quiet && \
    python -m pip wheel --wheel-dir dist/ . -r requirements.txt

FROM pythonbase as app

COPY --chown=fastapi:fastapi --from=builder /home/fastapi/dist/feather*.whl /home/fastapi/

RUN pip install --no-cache-dir feather*.whl

CMD ["uvicorn", "feather_spotter.app:app", "--host", "0.0.0.0", "--port", "8000"]
