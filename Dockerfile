# Resolved from python:3.12-slim on 2026-10-16.
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1

WORKDIR /app
COPY requirements.lock ./requirements.lock
RUN python -m pip install --no-cache-dir -r requirements.lock
COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-deps .

ENTRYPOINT ["srcnet-mc"]
CMD ["probe-scip"]
