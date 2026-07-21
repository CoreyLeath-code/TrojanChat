# TrojanChat
<p align="center">
  <a href="https://github.com/CoreyLeath-code/TrojanChat/actions/workflows/trojanchat-hygiene.yml">
    <img src="https://github.com/CoreyLeath-code/TrojanChat/actions/workflows/trojanchat-hygiene.yml/badge.svg?branch=main" alt="CI">
  </a>
  <a href="https://github.com/CoreyLeath-code/TrojanChat/actions/workflows/benchmarks.yml">
    <img src="https://github.com/CoreyLeath-code/TrojanChat/actions/workflows/benchmarks.yml/badge.svg?branch=main" alt="Benchmarks">
  </a>
  <a href="https://github.com/CoreyLeath-code/TrojanChat/actions/workflows/security-supply-chain.yml">
    <img src="https://github.com/CoreyLeath-code/TrojanChat/actions/workflows/security-supply-chain.yml/badge.svg?branch=main" alt="Security">
  </a>
  <a href="https://github.com/CoreyLeath-code/TrojanChat/security/code-scanning">
    <img src="https://img.shields.io/badge/CodeQL-enabled-2F80ED?logo=github&logoColor=white" alt="CodeQL">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-frontend-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Docker-non--root-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/SBOM-CycloneDX-2D9CDB" alt="CycloneDX SBOM">
</p>

<p align="center">
  <a href="https://github.com/CoreyLeath-code/TrojanChat/releases">
    <img src="https://img.shields.io/github/v/release/CoreyLeath-code/TrojanChat?include_prereleases&sort=semver" alt="Release">
  </a>
  <a href="https://github.com/CoreyLeath-code/TrojanChat/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/CoreyLeath-code/TrojanChat" alt="License">
  </a>
  <img src="https://img.shields.io/github/last-commit/CoreyLeath-code/TrojanChat/main" alt="Last commit">
  <img src="https://img.shields.io/github/repo-size/CoreyLeath-code/TrojanChat" alt="Repository size">
  <a href="https://github.com/CoreyLeath-code/TrojanChat/issues">
    <img src="https://img.shields.io/github/issues/CoreyLeath-code/TrojanChat" alt="Open issues">
  </a>
  <a href="https://github.com/CoreyLeath-code/TrojanChat/pulls">
    <img src="https://img.shields.io/github/issues-pr/CoreyLeath-code/TrojanChat" alt="Open pull requests">
  </a>
  <a href="https://github.com/CoreyLeath-code/TrojanChat/stargazers">
    <img src="https://img.shields.io/github/stars/CoreyLeath-code/TrojanChat?style=social" alt="GitHub stars">
  </a>
</p>

TrojanChat is a production-hardened, multi-client chat architecture optimized for high-concurrency environments. Moving away from standard blocking network sockets, this platform leverages asynchronous event loops to maintain thousands of concurrent connections efficiently while maintaining structural memory efficiency.

## Engineering evidence

| Evidence | Current result | Enforcement |
|---|---:|---|
| Unit + integration tests | 30 passing locally | Python 3.11/3.12 CI matrix |
| Critical-path coverage | 92.57% | CI fails below 90% |
| Median / P99 write latency | 1,239.880 / 1,303.501 ms per 50k-message run | Reproducible benchmark artifact |
| Throughput | 40,326.50 messages/s | Regression budget: no worse than -15% |
| Peak Python memory | 4.228 MiB | 80.06% below legacy baseline |
| Static analysis | Ruff + Bandit | Blocking; JSON report retained |
| Security | CodeQL, Gitleaks, pip-audit, Trivy | Blocking on secrets and actionable vulnerabilities |
| Supply chain | CycloneDX SBOM + Dependabot | Artifact per run; weekly updates |

The reference benchmark uses Windows 11, Python 3.12.13, 50,000 messages, seven iterations,
and a 10,000-message retention bound. Results describe this microbenchmarkâ€”not end-to-end network
latency or a production SLO. See the [benchmark methodology](benchmarks/benchmark_report.md),
[audit](docs/AUDIT.md), [architecture](ARCHITECTURE.md), [deployment guide](DEPLOYMENT.MD), and
[production checklist](docs/PRODUCTION_CHECKLIST.md).

## Research benchmark

**Question.** Can bounded, synchronized retention stop unbounded memory growth without exceeding a
15% write-throughput regression budget?

| Metric | Legacy list | Bounded, synchronized store | Relative change |
|---|---:|---:|---:|
| Mean latency / 50k writes | 1,141.831 ms | 1,237.607 ms | +8.4% |
| Median latency / 50k writes | 1,155.519 ms | 1,239.880 ms | +7.3% |
| P95 / P99 latency | 1,221.577 ms | 1,303.501 ms | +6.7% |
| Minimum / maximum latency | 1,063.323 / 1,221.577 ms | 1,180.249 / 1,303.501 ms | observed range |
| Throughput | 43,270.60 msg/s | 40,326.50 msg/s | **âˆ’6.8%** |
| Peak Python allocations | 21.205 MiB | 4.228 MiB | **âˆ’80.06%** |

**Method.** Seven independent iterations insert 50,000 structurally identical messages. Both
variants generate UUID4 identifiers and UTC timestamps; only storage and synchronization differ.
Latency uses `time.perf_counter`, memory uses `tracemalloc`, and throughput is derived from median
elapsed time. The raw, versioned result is [`benchmarks/latest.json`](benchmarks/latest.json).

**Interpretation.** The optimized store remains inside the pre-declared 15% throughput budget while
substantially reducing peak Python allocations. The experiment does not measure network transport,
JSON serialization, Redis, database persistence, multi-process contention, CPU utilization, or RSS.
CI reruns the benchmark on Ubuntu/Python 3.11 and uploads the raw result for per-commit comparison.

---

 Architectural Overview

 <img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/d9d6fa43-1152-4550-89b6-bcf2cebdf248" />


The platform splits operations across an event-driven system architecture to eliminate thread-starvation issues under scale.

* **Non-Blocking Core:** Built on top of Python's raw `asyncio` streams API, replacing slow multi-threaded overhead with a high-performance single-threaded asynchronous engine.
* **Structured Serialization Protocol:** Completely dropped plaintext string messaging in favor of structured JSON payloads, allowing for strict validation boundaries and predictable message framing.
* **Rootless Isolation Security:** Containers are structurally hardened using explicit multi-stage build patterns, forcing runtime scripts to execute via a dedicated unprivileged user group (`apprunner`).

---

## ðŸš€ Getting Started

### Prerequisites
* Python 3.11 or higher
* Docker (Optional, for containerized isolation)

### Standard Local Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Trojan3877/TrojanChat.git](https://github.com/Trojan3877/TrojanChat.git)
    cd TrojanChat
    ```

2.  **Initialize Environment & Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Spin Up the Core Infrastructure Engine:**
    ```bash
    python server.py
    ```

4.  **Connect Distributed Clients (In separate terminals):**
    ```bash
    python client.py "Corey"
    ```

â”œâ”€â”€ chat_core/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ config.py             # <-- Application security settings & validation rules
â”‚   â”œâ”€â”€ crypto_broker.py      # <-- Challenge generation and key distribution logic
â”‚   â””â”€â”€ connection_manager.py # <-- Tier 5: High-concurrency socket tracking state loop
â”œâ”€â”€ deployment/
â”‚   â”œâ”€â”€ gateway.conf          # <-- Tier 2: Envoy or Nginx reverse-proxy ingress rules
â”‚   â”œâ”€â”€ docker-compose.yml    # <-- Full local container environment mesh (Redis, App, Postgres)
â”‚   â””â”€â”€ Dockerfile            # <-- Minimal production runtime workspace blueprint
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ unit/                 # <-- Job #3: Asynchronous socket validation benches
â”‚   â””â”€â”€ schemas/              # <-- Job #7: JSON framing contract tests
â”œâ”€â”€ dailylog.md               # <-- Maintenance operations history ledger
â””â”€â”€ requirements.txt          # <-- Managed dependencies


 Engineering Roadmap
* [ ] **TLS/SSL Implementation:** Wrap connection initializations inside native `ssl.SSLContext` primitives to enforce data encryption in transit.
* [ ] **Horizontal Scale Broker:** Integrate a Redis Pub/Sub backplane layer to cleanly sync chat messages across multi-container instances.
* [ ] **Unit Test Suite:** Build comprehensive `pytest-asyncio` coverage to automatically validate connection handshakes and packet boundaries during CI/CD triggers.
    

Q1: Why use an Asynchronous Event Loop (asyncio) instead of traditional Multi-threading?
A: Multi-threaded architectures assign a dedicated operating system thread to every single connected client socket. When scaling up to thousands of concurrent users, this model hits a bottleneck due to extreme RAM consumption (each thread pre-allocates stack memory) and massive CPU overhead caused by continuous thread context-switching.

TrojanChat uses a single-threaded asynchronous event loop via asyncio. It utilizes multiplexed, non-blocking I/O system calls underneath the hood. When a socket is waiting for network data packets to arrive, it yields control back to the central event loop, enabling a single thread to smoothly manage thousands of active user data streams without breaking a sweat.

Q2: How does the application prevent data injection or cross-site script (XSS) delivery?
A: The platform implements defensive validation boundaries right at the ingestion layer:

Structural Enforcement: The backend drops raw plaintext and forces strict JSON layout checks. If a packet cannot be parsed into our target schema via json.loads(), it triggers a localized exception and drops the packet instantly.

Type Enforcement & Whitespace Trimming: The server extracts keys explicitly, forces type constraints, and trims down text fields via .strip().

Escaping Responsibilities: While basic script payloads are safely contained as text strings within the backend data stream, frontend interfaces reading from the stream treat the message string as immutable raw text rather than executable markup code, eliminating downstream script execution hazards.

Q3: What happens when a network connection suddenly drops or behaves erratically?
A: Traditional systems can suffer from socket resource leaks or frozen application states if a client drops offline abruptly. TrojanChat manages this through isolated, defensive write boundaries (_safe_write).

If a data write fails or throws an unhandled socket error, the server intercepts the exception immediately, bypasses global runtime crashes, purges that specific client's memory address pointer from the central tracking array (self.active_connections), and formally closes the socket file descriptor to prevent kernel-level file descriptor resource exhaustion.

Q4: How can this application scale horizontally to support millions of concurrent users across multiple regions?
A: Currently, the active connection mapping exists locally within the server's process memory space (self.active_connections). To scale horizontally across multiple cloud instances or Kubernetes clusters behind a global load balancer, the in-memory array can be supplemented with an external Redis Pub/Sub broker.

When Instance A receives a chat payload from an active socket, it publishes that JSON payload to a central Redis cluster topic. All other running application instances subscribing to that Redis topic pick up the message and broadcast it out concurrently to their own locally connected client pools.

### Building the Image
```bash
docker build -t trojanchat:latest .
