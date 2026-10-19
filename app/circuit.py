"""Circuit validation, step-by-step simulation and plain-language explanations for the learning app.

Ideal noise-free simulation. Qubit 0 is the leftmost bit of each basis label. Author: Rayyan Anwar
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np

from . import quantum as q

MAX_QUBITS, MAX_GATES, MAX_SHOTS = 6, 60, 100_000
ONE_Q = ("h", "x", "y", "z", "s", "sdg", "t", "tdg")
PARAM = ("rx", "ry", "rz")
TWO_Q = ("cnot", "cz", "swap")
CATALOG = [
    {"name": "h", "qubits": 1, "param": False, "title": "Hadamard", "text": "Turns |0> into an equal superposition of |0> and |1> (and back). The basic tool for creating superposition and interference."},
    {"name": "x", "qubits": 1, "param": False, "title": "Pauli-X (NOT)", "text": "Flips |0> and |1>: a quantum bit-flip."},
    {"name": "y", "qubits": 1, "param": False, "title": "Pauli-Y", "text": "Flips the bit and adds a phase: a half-turn around the Y axis of the Bloch sphere."},
    {"name": "z", "qubits": 1, "param": False, "title": "Pauli-Z", "text": "Leaves |0> alone and multiplies |1> by -1: a phase flip you cannot see by measuring directly."},
    {"name": "s", "qubits": 1, "param": False, "title": "S gate", "text": "A quarter-turn phase: |1> becomes i|1>. Rotates the Bloch vector 90 degrees about Z."},
    {"name": "sdg", "qubits": 1, "param": False, "title": "S-dagger", "text": "The inverse of S: |1> becomes -i|1>."},
    {"name": "t", "qubits": 1, "param": False, "title": "T gate", "text": "An eighth-turn phase (45 degrees about Z); with H and CNOT it makes universal quantum computing possible."},
    {"name": "tdg", "qubits": 1, "param": False, "title": "T-dagger", "text": "The inverse of T."},
    {"name": "rx", "qubits": 1, "param": True, "title": "Rotation X(theta)", "text": "Rotates the Bloch vector about the X axis by theta radians."},
    {"name": "ry", "qubits": 1, "param": True, "title": "Rotation Y(theta)", "text": "Rotates the Bloch vector about the Y axis by theta radians; RY(pi/2) on |0> gives an equal superposition with real amplitudes."},
    {"name": "rz", "qubits": 1, "param": True, "title": "Rotation Z(theta)", "text": "Rotates about the Z axis by theta radians: changes the relative phase only."},
    {"name": "cnot", "qubits": 2, "param": False, "title": "CNOT", "text": "Flips the target qubit when the control qubit is 1. Applied to a superposed control it creates entanglement."},
    {"name": "cz", "qubits": 2, "param": False, "title": "Controlled-Z", "text": "Multiplies the state by -1 only when both qubits are 1; symmetric in its two qubits."},
    {"name": "swap", "qubits": 2, "param": False, "title": "SWAP", "text": "Exchanges the states of two qubits."}]
INFO = {c["name"]: c for c in CATALOG}


class InputError(ValueError):
    """Invalid circuit or parameters."""


@dataclass(frozen=True)
class Op:
    name: str
    qubits: tuple
    theta: float | None = None


def validate(n_qubits, gates) -> list[Op]:
    if isinstance(n_qubits, bool) or not isinstance(n_qubits, int) or not 1 <= n_qubits <= MAX_QUBITS:
        raise InputError(f"n_qubits must be an integer in [1, {MAX_QUBITS}]")
    if not isinstance(gates, list) or len(gates) > MAX_GATES:
        raise InputError(f"gates must be a list of at most {MAX_GATES} items")
    ops = []
    for i, g in enumerate(gates):
        if not isinstance(g, dict) or set(g) - {"name", "qubits", "theta"}:
            raise InputError(f"gate {i}: expected an object with name, qubits and optional theta")
        name = g.get("name")
        if name not in INFO:
            raise InputError(f"gate {i}: unknown gate '{name}'")
        arity = INFO[name]["qubits"]
        qs = g.get("qubits")
        if not isinstance(qs, list) or len(qs) != arity or any(isinstance(x, bool) or not isinstance(x, int) for x in qs):
            raise InputError(f"gate {i} ({name}): qubits must be a list of {arity} integer(s)")
        if any(not 0 <= x < n_qubits for x in qs):
            raise InputError(f"gate {i} ({name}): qubit index out of range 0..{n_qubits - 1}")
        if len(set(qs)) != len(qs):
            raise InputError(f"gate {i} ({name}): qubits must be different")
        th = g.get("theta")
        if INFO[name]["param"]:
            if isinstance(th, bool) or not isinstance(th, (int, float)) or not np.isfinite(th) or abs(th) > 100:
                raise InputError(f"gate {i} ({name}): theta (radians, |theta| <= 100) is required")
            th = float(th)
        elif th is not None:
            raise InputError(f"gate {i} ({name}): this gate takes no theta")
        ops.append(Op(name, tuple(qs), th))
    return ops


def apply_op(state: np.ndarray, op: Op) -> np.ndarray:
    n = op.name
    if n in q.FIXED:
        return q.apply_1q(state, q.FIXED[n], op.qubits[0])
    if n in PARAM:
        return q.apply_1q(state, {"rx": q.rx, "ry": q.ry, "rz": q.rz}[n](op.theta), op.qubits[0])
    return {"cnot": q.apply_cnot, "cz": q.apply_cz, "swap": q.apply_swap}[n](state, *op.qubits)


def explain(op: Op | None, state_vec: np.ndarray) -> str:
    if op is None:
        return "Start: every qubit is |0>, so the whole register is the single basis state |" + "0" * state_vec.ndim + ">."
    info = INFO[op.name]
    if len(op.qubits) == 1:
        where = f"qubit {op.qubits[0]}"
    elif op.name == "cnot":
        where = f"control qubit {op.qubits[0]} and target qubit {op.qubits[1]}"
    else:
        where = f"qubits {op.qubits[0]} and {op.qubits[1]}"
    ang = f" by {op.theta:.3f} rad ({np.degrees(op.theta):.1f} degrees)" if op.theta is not None else ""
    p = (np.abs(state_vec) ** 2).ravel()
    n = state_vec.ndim
    top = [f"|{format(i, f'0{n}b')}> {p[i]:.1%}" for i in np.argsort(-p)[:3] if p[i] > 1e-9]
    return f"{info['title']} on {where}{ang}. {info['text']} Most likely outcomes now: {', '.join(top)}."


def snapshot(state: np.ndarray, op: Op | None) -> dict:
    v = state[0]
    n = v.ndim
    flat = v.reshape(-1)
    return {"gate": None if op is None else {"name": op.name, "qubits": list(op.qubits), "theta": op.theta},
            "explanation": explain(op, v),
            "amplitudes": [[round(float(a.real), 6), round(float(a.imag), 6)] for a in flat],
            "probabilities": [round(float(p), 6) for p in (np.abs(flat) ** 2)],
            "bloch": [[round(c, 6) for c in q.bloch_vector(v, k)] for k in range(n)],
            "entropy": [round(q.qubit_entropy(v, k), 6) for k in range(n)]}


def run_circuit(n_qubits, gates, shots: int = 1024, seed: int | None = None) -> dict:
    ops = validate(n_qubits, gates)
    if isinstance(shots, bool) or not isinstance(shots, int) or not 1 <= shots <= MAX_SHOTS:
        raise InputError(f"shots must be an integer in [1, {MAX_SHOTS}]")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed < 2 ** 32):
        raise InputError("seed must be an integer in [0, 2^32)")
    used_seed = seed if seed is not None else int.from_bytes(os.urandom(4), "big")
    state = q.zero_state(n_qubits)
    steps = [snapshot(state, None)]
    for op in ops:
        state = apply_op(state, op)
        steps.append(snapshot(state, op))
    probs = q.probabilities(state)[0]
    final = steps[-1]
    return {"n_qubits": n_qubits, "labels": q.basis_labels(n_qubits), "steps": steps,
            "counts": q.sample_counts(probs, shots, used_seed), "shots": shots, "seed": used_seed,
            "entangled_qubits": [k for k, e in enumerate(final["entropy"]) if e > 1e-6],
            "note": "Ideal noise-free simulation. Qubit 0 is the leftmost bit. Real devices add noise and limited connectivity."}
