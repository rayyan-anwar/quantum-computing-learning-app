# Evaluation

Author: Rayyan Anwar

This is a learning tool, so the evaluation is about **correctness** of the simulator and examples. `python scripts/evaluate.py` writes `results/RESULTS.md`.

| Check | Committed result |
|---|---|
| 300 random circuits (1-6 qubits, depth 30) vs an independent dense-matrix implementation | max amplitude difference 3e-16 |
| Unitarity of 48 gate matrices | max error 2e-16 |
| Norm after 50 circuits of depth 200 (5 qubits) | max drift 1.6e-15 |
| Sampling calibration: 1000 runs x 10,000 shots of a Bell state, chi-square test at 5% | false-rejection rate 0.046 (expected 0.05) |
| Six worked examples (superposition, interference, Bell, GHZ, Grover, teleportation of 200 random states) | match analytic results to the 6 decimals returned by the API |
| Time for a 50-gate circuit | about 2 ms at 6 qubits, 38 ms at 16 qubits; memory doubles per qubit |

## Caveats
- All checks are against ideal, noise-free quantum mechanics. Real devices have gate errors, decoherence, readout error and limited connectivity, none of which are modelled.
- The dense reference and the fast simulator were written by the same author; independence comes from different algorithms (axis operations vs Kronecker products and basis permutations), not from a third-party library.
- No usability study with real learners was conducted; the explanations are concise and may simplify (for example, the Bloch picture applies to single qubits only).
