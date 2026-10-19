# Quantum Computing Learning App

**Author: Rayyan Anwar** — AI/ML Engineer | Researcher | Technology Manager | Software Developer

Build a quantum circuit gate by gate and watch what happens: amplitudes and probabilities, a Bloch sphere per qubit, entanglement entropy, plain-language explanations of each step, and sampled measurement counts. Six worked examples (superposition, interference, Bell pair, GHZ, Grover search, teleportation) come with the result you should expect.

> Ideal, noise-free simulation of at most 6 qubits. It teaches the concepts; it does not model real quantum hardware.

## Implemented vs optional
| Feature | Status |
|---|---|
| 14 gates (H, X, Y, Z, S, S†, T, T†, RX, RY, RZ, CNOT, CZ, SWAP) with explanations | Implemented, tested |
| Step-through states, Bloch vectors, entanglement entropy, seeded measurement sampling | Implemented, tested |
| Six worked examples with analytic expectations (teleportation checked on 200 random states) | Implemented, tested |
| Simulator verified against an independent dense-matrix implementation | Implemented, tested |
| FastAPI service + interactive browser UI | Implemented; API tests written but **not executed in the authoring sandbox**; UI JavaScript only syntax-checked |
| Noise models, mid-circuit measurement, custom or multi-controlled gates, more than 6 qubits, real-hardware backends | Not implemented |

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
uvicorn app.main:app --port 8018       # open http://127.0.0.1:8018
```
`curl -s localhost:8018/api/simulate -H 'content-type: application/json' -d '{"n_qubits":2,"gates":[{"name":"h","qubits":[0]},{"name":"cnot","qubits":[0,1]}],"shots":1000,"seed":1}'`

Endpoints: `GET /health`, `/api/info`, `/api/gates`, `/api/presets`; `POST /api/simulate`; docs at `/docs`.

## Verification (committed run, `results/RESULTS.md`)
Agreement with an independent dense-matrix simulator on 300 random circuits to 3e-16; norm drift under 2e-15 after depth-200 circuits; Bell-state sampling passes a calibration check (false-rejection rate 0.046 at a 5% level). Details and caveats: [docs/EVALUATION.md](docs/EVALUATION.md).

## Documentation
[Architecture](docs/ARCHITECTURE.md) · [Evaluation](docs/EVALUATION.md) · [System card](docs/MODEL_CARD.md) · [Deployment](docs/DEPLOYMENT.md)

## Testing status
13 tests executed and passing (`python -m unittest`); 2 API tests skipped in the authoring sandbox (FastAPI/httpx unavailable). Docker not built; Ruff not run.

## Known limitations
Ideal qubits only; 6-qubit cap; simplified explanations; no usability testing; no authentication or rate limiting.

## GitHub repository metadata
- **Description:** Interactive step-by-step quantum circuit simulator for learning: gates, superposition, entanglement, Bloch spheres, Grover and teleportation examples.
- **Topics:** `quantum-computing`, `quantum-simulator`, `education`, `bloch-sphere`, `state-vector`, `numpy`, `fastapi`, `python`

## License
MIT © Rayyan Anwar. See [LICENSE](LICENSE).
