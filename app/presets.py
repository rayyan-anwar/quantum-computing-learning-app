"""Worked examples with the result a learner should expect (verified numerically in the tests).

Author: Rayyan Anwar
"""
from __future__ import annotations


def g(name, *qubits, theta=None):
    d = {"name": name, "qubits": list(qubits)}
    if theta is not None:
        d["theta"] = theta
    return d


PRESETS = [
    {"id": "superposition", "title": "Superposition", "n_qubits": 1, "gates": [g("h", 0)],
     "description": "One Hadamard puts the qubit in an equal mix of 0 and 1.", "expect": "Measuring gives 0 or 1 with probability 0.5 each."},
    {"id": "interference", "title": "Interference (H, Z, H)", "n_qubits": 1, "gates": [g("h", 0), g("z", 0), g("h", 0)],
     "description": "The Z in the middle changes only a phase, yet the second H turns that phase into a definite outcome.",
     "expect": "Always measures 1: the two paths to 0 cancel."},
    {"id": "bell", "title": "Bell pair", "n_qubits": 2, "gates": [g("h", 0), g("cnot", 0, 1)],
     "description": "Superposition on qubit 0, then CNOT copies the choice into qubit 1 without choosing it.",
     "expect": "Outcomes 00 and 11 with probability 0.5 each, never 01 or 10; each qubit alone is maximally mixed (entropy 1)."},
    {"id": "ghz3", "title": "GHZ state (3 qubits)", "n_qubits": 3, "gates": [g("h", 0), g("cnot", 0, 1), g("cnot", 1, 2)],
     "description": "Entanglement chained across three qubits.", "expect": "Only 000 and 111, 0.5 each."},
    {"id": "grover2", "title": "Grover search (2 qubits, marked state 11)", "n_qubits": 2,
     "gates": [g("h", 0), g("h", 1), g("cz", 0, 1), g("h", 0), g("h", 1), g("x", 0), g("x", 1), g("cz", 0, 1), g("x", 0), g("x", 1), g("h", 0), g("h", 1)],
     "description": "Oracle (CZ marks 11) then diffusion (reflect about the average). With 4 items one round is enough.",
     "expect": "Measures 11 with probability 1 after a single iteration."},
    {"id": "teleportation", "title": "Teleportation (deferred measurement)", "n_qubits": 3,
     "gates": [g("ry", 0, theta=1.1), g("rz", 0, theta=0.7), g("h", 1), g("cnot", 1, 2), g("cnot", 0, 1), g("h", 0), g("cnot", 1, 2), g("cz", 0, 2)],
     "description": "Qubit 0 holds an unknown state. A shared Bell pair (qubits 1, 2) plus classical-style corrections, written here as controlled gates (deferred measurement), moves the state to qubit 2.",
     "expect": "Qubit 2 ends with exactly the Bloch vector qubit 0 started with; qubits 0 and 1 end in uniform random-looking states."},
]
BY_ID = {p["id"]: p for p in PRESETS}
