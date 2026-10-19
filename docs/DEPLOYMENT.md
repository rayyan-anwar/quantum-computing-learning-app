# Deployment

Author: Rayyan Anwar

## Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
python scripts/evaluate.py
uvicorn app.main:app --port 8018     # http://127.0.0.1:8018
```
## Docker
`docker compose up --build` (port 8018, health `/health`). Written but **not built or run** in the authoring sandbox; CI has a `docker build` job.
## Cloud
Any container host: build and push (your account), expose 8018 behind HTTPS, probe `/health`. Stateless, no secrets, no database. Request cost is bounded (6 qubits, 60 gates), but the API is unauthenticated: add rate limiting or platform access control if public. Not deployed by the author.
## Screenshots
Load the Bell example, move the step slider and measure; capture into `docs/screenshots/` (none bundled).
