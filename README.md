# ⚛️ Quantum Computing Learning App

<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0B1026,40:312E81,75:6D28D9,100:06B6D4&height=240&section=header&text=Quantum%20Computing&fontSize=42&fontColor=FFFFFF&animation=fadeIn&fontAlignY=35&desc=Build%20Circuits.%20Explore%20States.%20Understand%20Quantum.&descSize=14&descAlignY=58" width="100%" alt="Animated Quantum Computing banner" />

  <h3>Learn Quantum Computing by Building Quantum Circuits</h3>

  **Created by Rayyan Anwar**

  *AI/ML Engineer · Researcher · Technology Manager · Software Developer*

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Quantum_Computing-6D28D9?style=for-the-badge" alt="Quantum Computing" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
  </p>

  <p>
    <img src="https://img.shields.io/badge/Tests-13%20Passed-success?style=flat-square" alt="13 passing tests reported" />
    <img src="https://img.shields.io/badge/Simulation-6%20Qubits-blueviolet?style=flat-square" alt="Up to six qubits" />
    <img src="https://img.shields.io/badge/Hardware-Ideal%20Simulation-blue?style=flat-square" alt="Ideal simulation" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License" />
  </p>

  <a href="https://github.com/rayyan-anwar">GitHub Profile</a> ·
  <a href="https://github.com/rayyan-anwar?tab=repositories">Explore Projects</a>

</div>

---

## 🌌 Explore the Quantum World

What happens when a qubit enters superposition? How does entanglement connect quantum systems? Why can quantum interference change measurement probabilities?

This interactive learning application lets you build a quantum circuit one gate at a time and inspect how the quantum state evolves after each operation.

Explore complex amplitudes, measurement probabilities, Bloch vectors, entanglement entropy, and sampled measurement results through a step-by-step visual learning experience.

> [!NOTE]
> This application simulates ideal, noise-free quantum circuits with a maximum of six qubits. It is an educational simulator, not a model of real quantum hardware.

## ✨ Key Features

<table>
  <tr>
    <td width="50%">
      <h3>⚛️ Interactive Circuit Builder</h3>
      Add quantum gates one by one and explore how each operation transforms the state vector.
    </td>
    <td width="50%">
      <h3>📊 State Amplitudes & Probabilities</h3>
      Inspect complex probability amplitudes and calculate the probabilities of computational-basis outcomes.
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🌐 Bloch Vector Visualization</h3>
      Examine the Bloch vector for each qubit to understand single-qubit state geometry.
    </td>
    <td width="50%">
      <h3>🔗 Entanglement Analysis</h3>
      Explore entanglement entropy and understand correlations in multi-qubit states.
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🎲 Quantum Measurements</h3>
      Sample measurement counts with configurable shots and a reproducible random seed.
    </td>
    <td width="50%">
      <h3>🧠 Step-by-Step Explanations</h3>
      Learn what each gate does and how it changes the quantum state, using plain-language explanations.
    </td>
  </tr>
</table>

## 🧩 Quantum Gates Supported

The simulator implements 14 quantum gates.

| Category | Gates | Purpose |
|---|---|---|
| Pauli gates | X, Y, Z | Bit flips, phase flips, and rotations of the state |
| Superposition | H | Creates equal superpositions from computational-basis states |
| Phase gates | S, S†, T, T† | Introduces relative phase shifts |
| Rotation gates | RX, RY, RZ | Rotates a qubit state around Bloch sphere axes |
| Controlled gates | CNOT, CZ | Applies conditional operations to multi-qubit states |
| Exchange gate | SWAP | Exchanges the states of two qubits |

## 🧪 Six Worked Quantum Experiments

<details>
<summary><strong>1. Superposition</strong></summary>

**Concept:** A Hadamard gate transforms the initial state \(|0\rangle\) into an equal superposition.

\[
H|0\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}
\]

Expected measurement probabilities:

- `0`: 50%
- `1`: 50%

</details>

<details>
<summary><strong>2. Quantum Interference</strong></summary>

**Concept:** Quantum amplitudes can reinforce or cancel one another.

Applying a Hadamard gate twice to \(|0\rangle\) returns the system to its original state:

\[
H H |0\rangle = |0\rangle
\]

Expected measurement: `0` with probability 100% in the ideal simulator.

</details>

<details>
<summary><strong>3. Bell Pair</strong></summary>

**Concept:** A Hadamard gate followed by a CNOT gate creates an entangled two-qubit state.

\[
|\Phi^+\rangle =
\frac{|00\rangle+|11\rangle}{\sqrt{2}}
\]

Expected measurement outcomes:

- `00`: 50%
- `11`: 50%

The two qubits exhibit correlated measurement results.

</details>

<details>
<summary><strong>4. GHZ State</strong></summary>

**Concept:** Extend entanglement across three qubits.

\[
|\mathrm{GHZ}\rangle =
\frac{|000\rangle+|111\rangle}{\sqrt{2}}
\]

Expected measurement outcomes:

- `000`: 50%
- `111`: 50%

This illustrates multi-qubit correlations in an ideal circuit.

</details>

<details>
<summary><strong>5. Grover Search</strong></summary>

**Concept:** Grover's algorithm uses an oracle and amplitude amplification to increase the probability of measuring a marked item.

The example demonstrates the algorithm's core idea on a small search space. Its expected result depends on the oracle, number of qubits, and number of Grover iterations.

</details>

<details>
<summary><strong>6. Quantum Teleportation</strong></summary>

**Concept:** Quantum teleportation transfers an unknown qubit state using shared entanglement, a joint measurement, classical communication, and conditional corrections.

It does not copy an unknown quantum state or transmit information faster than light.

The implementation's teleportation example was checked against 200 random input states.

</details>

## 🔬 Verification & Evaluation

Results from the committed evaluation report, `results/RESULTS.md`:

| Evaluation | Reported result |
|---|---:|
| Random circuits compared against an independent dense-matrix simulator | 300 |
| Maximum reported simulator disagreement | \(3 \times 10^{-16}\) |
| Norm drift after depth-200 circuits | Below \(2 \times 10^{-15}\) |
| Bell-state sampling calibration | Passed |
| Calibration false-rejection rate | 0.046 at a 5% significance level |
| Reported passing tests | 13 |

**What these results mean**

- Agreement with an independent implementation supports the correctness of the simulator for the tested circuits.
- Small norm drift indicates that state-vector normalization was preserved to high numerical precision in the reported tests.
- The Bell-state calibration result is specific to the test procedure and does not guarantee every measurement distribution will be accurate.
- These are software verification results, not evidence of quantum advantage or performance on real quantum computers.

See [Evaluation Documentation](docs/EVALUATION.md) for methodology and caveats.

## 🏗️ Technology Stack

| Technology | Role |
|---|---|
| Python | Core implementation |
| NumPy | Numerical linear algebra and state-vector calculations |
| FastAPI | HTTP API |
| HTML, CSS, JavaScript | Interactive browser interface |
| pytest / unittest | Automated verification |
| OpenAPI / Swagger UI | API exploration and documentation |

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or a compatible version supported by the project's dependencies.
- Git.
- A terminal or command prompt.

### 1. Clone the repository

```bash
git clone https://github.com/rayyan-anwar/quantum-computing-learning-app.git
cd quantum-computing-learning-app
```

*If your repository has a different name, replace the example repository URL and directory accordingly.*

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 4. Run the tests

```bash
python -m pytest -q
```

The committed report records 13 passing tests. Verify the current test output in your environment because API tests were not executed in the original authoring sandbox.

### 5. Launch the application

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8018
```

Open these addresses in your browser:

| Resource | URL |
|---|---|
| Learning application | http://127.0.0.1:8018 |
| Interactive API documentation | http://127.0.0.1:8018/docs |
| Health check | http://127.0.0.1:8018/health |
| Application information | http://127.0.0.1:8018/api/info |
| Available gates | http://127.0.0.1:8018/api/gates |
| Worked examples | http://127.0.0.1:8018/api/presets |

## 💻 Run Your First Quantum Circuit

The following request creates a Bell pair and samples 1,000 measurements.

```bash
curl -s http://127.0.0.1:8018/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "n_qubits": 2,
    "gates": [
      {"name": "h", "qubits": [0]},
      {"name": "cnot", "qubits": [0, 1]}
    ],
    "shots": 1000,
    "seed": 1
  }'
```

Expected behavior:

- The first qubit enters superposition.
- The CNOT operation entangles the two qubits.
- The ideal state has equal probabilities for `00` and `11`.
- The sampled counts should be approximately balanced, with small statistical variations.

The random seed makes the sampling reproducible for the same implementation and execution conditions.

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/info` | Simulator information |
| `GET` | `/api/gates` | Available quantum gates |
| `GET` | `/api/presets` | Worked circuit examples |
| `POST` | `/api/simulate` | Simulate a quantum circuit |
| `GET` | `/docs` | Interactive API documentation |

## 🧮 Core Quantum Concepts

The learning application introduces several foundational ideas.

**Qubit:** A quantum system represented by a state such as

\[
|\psi\rangle = \alpha|0\rangle+\beta|1\rangle
\]

where \(|\alpha|^2+|\beta|^2=1\).

**Superposition:** A quantum state can combine computational-basis states with complex amplitudes.

**Interference:** Amplitudes add together, allowing probabilities of some outcomes to increase and others to decrease.

**Entanglement:** A multi-qubit state can exhibit correlations that cannot be represented as a product of independent pure single-qubit states.

**Measurement:** Repeated measurements sample outcomes according to their quantum probabilities.

## ⚠️ Limitations

- Supports a maximum of six qubits.
- Uses ideal, noise-free state-vector simulation.
- Does not model decoherence, gate errors, or hardware noise.
- Does not implement mid-circuit measurement.
- Does not support custom gates or multi-controlled gates.
- Does not connect to real quantum hardware.
- Provides simplified educational explanations, not a complete quantum mechanics course.
- Has no authentication or rate limiting.
- Has not undergone formal usability testing.

## 🛣️ Future Roadmap

Potential future improvements, not currently implemented:

- [ ] Circuit drag-and-drop interface.
- [ ] Animated Bloch sphere visualization.
- [ ] Quantum noise and decoherence models.
- [ ] Step-by-step mathematical derivations.
- [ ] Circuit export to QASM.
- [ ] Integration with quantum SDKs and real-hardware backends.
- [ ] Expanded browser end-to-end tests.
- [ ] Mobile-friendly interactive circuit editor.
- [ ] Additional algorithms, including phase estimation and quantum Fourier transform.

## 📚 Documentation

| Document | Purpose |
|---|---|
| [Architecture](docs/ARCHITECTURE.md) | System design and components |
| [Evaluation](docs/EVALUATION.md) | Verification methodology and results |
| [Model Card](docs/MODEL_CARD.md) | Intended use and limitations |
| [Deployment](docs/DEPLOYMENT.md) | Deployment instructions |
| [Results](results/RESULTS.md) | Committed test and evaluation results |

## 👨‍💻 About the Author

<div align="center">

  <h3>Rayyan Anwar</h3>

  **AI/ML Engineer · Researcher · Technology Manager · Software Developer**

  Exploring the intersection of artificial intelligence, quantum computing, software engineering, and scientific research.

  <a href="https://github.com/rayyan-anwar">
    <img src="https://img.shields.io/badge/GitHub-rayyan--anwar-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile" />
  </a>

  <p>
    <a href="https://github.com/rayyan-anwar?tab=repositories">Explore My Repositories</a>
  </p>

</div>

## 📄 License

Released under the **MIT License**.

Copyright © Rayyan Anwar. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:06B6D4,50:312E81,100:0B1026&height=120&section=footer" width="100%" alt="Decorative quantum-themed footer" />

  **From the first qubit to quantum algorithms. Learn by experimenting.**

  <sub>Simulate carefully. Question deeply. Build scientifically.</sub>

</div>
