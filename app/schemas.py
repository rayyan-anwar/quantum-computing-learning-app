"""Pydantic request models. Author: Rayyan Anwar"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GateName = Literal["h", "x", "y", "z", "s", "sdg", "t", "tdg", "rx", "ry", "rz", "cnot", "cz", "swap"]


class GateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: GateName
    qubits: list[int] = Field(min_length=1, max_length=2)
    theta: float | None = Field(None, ge=-100, le=100)


class SimulateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    n_qubits: int = Field(2, ge=1, le=6)
    gates: list[GateIn] = Field(default_factory=list, max_length=60)
    shots: int = Field(1024, ge=1, le=100_000)
    seed: int | None = Field(None, ge=0, lt=2 ** 32)
