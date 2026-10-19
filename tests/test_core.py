"""Tests: validation, worked examples with analytic expectations, teleportation fidelity, dense-reference agreement, API.

Author: Rayyan Anwar
"""
import unittest

import numpy as np

from app import dense_reference as D
from app import quantum as q
from app.circuit import CATALOG, INFO, MAX_GATES, InputError, run_circuit, validate
from app.presets import BY_ID, PRESETS, g


def final_probs(preset_id):
    p = BY_ID[preset_id]
    r = run_circuit(p["n_qubits"], p["gates"], 100, 0)
    return dict(zip(r["labels"], r["steps"][-1]["probabilities"])), r


class TestValidation(unittest.TestCase):
    def test_bad_circuits_rejected(self):
        bad = [(0, []), (7, []), (True, []), ("2", []), (2, "h"), (2, [{}]), (2, [{"name": "foo", "qubits": [0]}]),
               (2, [{"name": "h", "qubits": [2]}]), (2, [{"name": "h", "qubits": [0, 1]}]), (2, [{"name": "cnot", "qubits": [0]}]),
               (2, [{"name": "cnot", "qubits": [1, 1]}]), (2, [{"name": "h", "qubits": [True]}]), (2, [{"name": "rx", "qubits": [0]}]),
               (2, [{"name": "rx", "qubits": [0], "theta": float("nan")}]), (2, [{"name": "rx", "qubits": [0], "theta": 1000}]),
               (2, [{"name": "h", "qubits": [0], "theta": 1.0}]), (2, [{"name": "h", "qubits": [0], "extra": 1}]),
               (2, [g("h", 0)] * (MAX_GATES + 1)), (2, [{"name": "h", "qubits": [-1]}])]
        for n, gates in bad:
            with self.assertRaises(InputError, msg=str(gates)[:60]):
                validate(n, gates)

    def test_bad_shots_and_seed(self):
        for kw in ({"shots": 0}, {"shots": 100_001}, {"shots": 1.5}, {"shots": True}, {"seed": -1}, {"seed": 2 ** 32}, {"seed": "x"}):
            with self.assertRaises(InputError, msg=str(kw)):
                run_circuit(1, [g("h", 0)], **kw)

    def test_empty_circuit_is_all_zero_state(self):
        r = run_circuit(3, [], 10, 0)
        self.assertEqual(len(r["steps"]), 1)
        self.assertEqual(r["counts"], {"000": 10})

    def test_catalog_is_complete_and_runnable(self):
        self.assertEqual({c["name"] for c in CATALOG}, set(INFO))
        for c in CATALOG:
            gate = {"name": c["name"], "qubits": [0] if c["qubits"] == 1 else [0, 1]}
            if c["param"]:
                gate["theta"] = 0.5
            r = run_circuit(2, [gate], 10, 0)
            self.assertAlmostEqual(sum(r["steps"][-1]["probabilities"]), 1.0, places=5)
            self.assertIn(c["title"].split()[0], r["steps"][-1]["explanation"])


class TestWorkedExamples(unittest.TestCase):
    def test_superposition_and_interference(self):
        p, _ = final_probs("superposition")
        self.assertAlmostEqual(p["0"], 0.5, places=6)
        p, _ = final_probs("interference")
        self.assertAlmostEqual(p["1"], 1.0, places=6)

    def test_bell_and_ghz(self):
        p, r = final_probs("bell")
        self.assertAlmostEqual(p["00"], 0.5, places=6)
        self.assertAlmostEqual(p["11"], 0.5, places=6)
        self.assertEqual(r["entangled_qubits"], [0, 1])
        self.assertTrue(np.allclose(r["steps"][-1]["entropy"], [1, 1], atol=1e-5))
        self.assertEqual(set(r["counts"]), {"00", "11"})
        p, r = final_probs("ghz3")
        self.assertAlmostEqual(p["000"] + p["111"], 1.0, places=6)
        self.assertEqual(r["entangled_qubits"], [0, 1, 2])

    def test_grover_finds_marked_state_with_certainty(self):
        p, r = final_probs("grover2")
        self.assertAlmostEqual(p["11"], 1.0, places=6)
        self.assertEqual(r["counts"], {"11": 100})

    def test_teleportation_moves_arbitrary_states(self):
        rng = np.random.default_rng(0)
        for _ in range(50):
            th, ph = float(rng.uniform(0, np.pi)), float(rng.uniform(0, 2 * np.pi))
            gates = [g("ry", 0, theta=th), g("rz", 0, theta=ph), g("h", 1), g("cnot", 1, 2), g("cnot", 0, 1), g("h", 0),
                     g("cnot", 1, 2), g("cz", 0, 2)]
            r = run_circuit(3, gates, 10, 0)
            sent, got = r["steps"][2]["bloch"][0], r["steps"][-1]["bloch"][2]
            np.testing.assert_allclose(got, sent, atol=1e-5)
            self.assertAlmostEqual(float(np.dot(got, sent)), 1.0, places=4)  # fidelity (1 + r.r')/2 = 1

    def test_every_preset_has_text_and_validates(self):
        for p in PRESETS:
            validate(p["n_qubits"], p["gates"])
            self.assertTrue(p["description"] and p["expect"] and p["title"])
        self.assertEqual(len({p["id"] for p in PRESETS}), len(PRESETS))


class TestSnapshotsAndSampling(unittest.TestCase):
    def test_each_step_is_normalised_and_bloch_bounded(self):
        rng = np.random.default_rng(1)
        gates = []
        for _ in range(40):
            a, b = [int(x) for x in rng.choice(4, 2, replace=False)]
            gates += [g(["h", "t", "s"][int(rng.integers(0, 3))], a), g("cnot", a, b), g("ry", b, theta=float(rng.uniform(0, 6)))]
        r = run_circuit(4, gates[:MAX_GATES], 10, 0)
        for s in r["steps"]:
            self.assertAlmostEqual(sum(s["probabilities"]), 1.0, places=4)
            for v in s["bloch"]:
                self.assertLessEqual(float(np.linalg.norm(v)), 1 + 1e-5)
            for e in s["entropy"]:
                self.assertTrue(-1e-9 <= e <= 1 + 1e-6)

    def test_seeded_sampling_is_reproducible_and_sums_to_shots(self):
        a, b = run_circuit(2, BY_ID["bell"]["gates"], 5000, 7), run_circuit(2, BY_ID["bell"]["gates"], 5000, 7)
        self.assertEqual(a["counts"], b["counts"])
        self.assertEqual(sum(a["counts"].values()), 5000)
        self.assertEqual(a["seed"], 7)
        self.assertNotEqual(a["counts"], run_circuit(2, BY_ID["bell"]["gates"], 5000, 8)["counts"])
        free = run_circuit(2, BY_ID["bell"]["gates"], 100)
        self.assertIsInstance(free["seed"], int)

    def test_sampling_matches_probabilities(self):
        r = run_circuit(1, [g("ry", 0, theta=1.0)], 40000, 3)
        p1 = np.sin(0.5) ** 2
        self.assertAlmostEqual(r["counts"].get("1", 0) / 40000, p1, delta=4 * np.sqrt(p1 * (1 - p1) / 40000))


class TestDenseAgreementThroughPublicApi(unittest.TestCase):
    def test_random_circuits_match_independent_dense_simulation(self):
        rng = np.random.default_rng(5)
        for _ in range(40):
            n = int(rng.integers(1, 6))
            gates, ops = [], []
            for _ in range(20):
                name = ["h", "x", "y", "z", "s", "t", "rx", "ry", "rz", "cnot", "cz", "swap"][int(rng.integers(0, 12))]
                if name in ("cnot", "cz", "swap"):
                    if n < 2:
                        continue
                    a, b = [int(x) for x in rng.choice(n, 2, replace=False)]
                    gates.append(g(name, a, b))
                    ops.append({"cnot": D.op_cnot, "cz": D.op_cz, "swap": D.op_swap}[name](n, a, b))
                else:
                    a = int(rng.integers(0, n))
                    th = float(rng.uniform(0, 6)) if name.startswith("r") else None
                    gates.append(g(name, a, theta=th))
                    mat = q.FIXED[name] if th is None else {"rx": q.rx, "ry": q.ry, "rz": q.rz}[name](th)
                    ops.append(D.op_1q(n, mat, a))
            r = run_circuit(n, gates, 10, 0)
            amp = np.array([complex(re, im) for re, im in r["steps"][-1]["amplitudes"]])
            np.testing.assert_allclose(amp, D.run(n, ops), atol=2e-6)


try:
    import fastapi  # noqa: F401
    import httpx  # noqa: F401
    HAVE_API = True
except ImportError:
    HAVE_API = False


@unittest.skipUnless(HAVE_API, "fastapi/httpx not installed - API tests are skipped, not passed")
class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient
        from app.main import app
        cls.c = TestClient(app)

    def test_basics_and_catalog(self):
        self.assertEqual(self.c.get("/health").json()["author"], "Rayyan Anwar")
        self.assertIn("Rayyan Anwar", self.c.get("/").text)
        self.assertEqual(len(self.c.get("/api/gates").json()["gates"]), len(CATALOG))
        self.assertEqual(len(self.c.get("/api/presets").json()["presets"]), len(PRESETS))

    def test_simulate_bell_and_errors(self):
        r = self.c.post("/api/simulate", json={"n_qubits": 2, "gates": BY_ID["bell"]["gates"], "shots": 100, "seed": 1})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(set(r.json()["counts"]), {"00", "11"})
        for bad in ({"n_qubits": 9}, {"gates": [{"name": "foo", "qubits": [0]}]}, {"shots": 0},
                    {"gates": [{"name": "rx", "qubits": [0]}]}, {"gates": [{"name": "h", "qubits": [5]}], "n_qubits": 2}):
            self.assertEqual(self.c.post("/api/simulate", json=bad).status_code, 422, msg=str(bad)[:50])


if __name__ == "__main__":
    unittest.main()
