"""FastAPI application for the Quantum Computing Learning App. Author: Rayyan Anwar"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

from . import __author__, __version__
from .circuit import CATALOG, MAX_GATES, MAX_QUBITS, InputError, run_circuit
from .presets import PRESETS
from .schemas import SimulateRequest

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Quantum Computing Learning App", version=__version__,
              description="Build circuits and watch the quantum state change step by step (ideal simulator). Author: Rayyan Anwar.",
              contact={"name": __author__}, license_info={"name": "MIT"})


@app.exception_handler(InputError)
async def on_input_error(_: Request, exc: InputError):
    return JSONResponse(status_code=422, content={"error": {"code": "invalid_input", "message": str(exc)}})


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__, "author": __author__}


@app.get("/api/info")
def info():
    return {"name": "Quantum Computing Learning App", "author": __author__, "version": __version__,
            "limits": {"max_qubits": MAX_QUBITS, "max_gates": MAX_GATES}, "simulator": "ideal noise-free state vector"}


@app.get("/api/gates")
def gates():
    return {"gates": CATALOG}


@app.get("/api/presets")
def presets():
    return {"presets": PRESETS}


@app.post("/api/simulate")
def simulate(req: SimulateRequest):
    return run_circuit(req.n_qubits, [g.model_dump(exclude_none=True) for g in req.gates], req.shots, req.seed)


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(ROOT / "frontend" / "index.html")
