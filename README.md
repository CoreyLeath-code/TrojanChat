# TrojanChat
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-Realtime-010101)
![Docker](https://img.shields.io/badge/Docker-Multi--Stage%20Non--Root-2496ED?logo=docker&logoColor=white)
![GHCR](https://img.shields.io/badge/GHCR-Container%20Publishing-24292F?logo=github&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-XML%20Artifacts-success)
![Ruff](https://img.shields.io/badge/Ruff-Correctness%20Gate-D7FF64)
![Black](https://img.shields.io/badge/Black-Formatting%20Advisory-000000)
![JUnit](https://img.shields.io/badge/JUnit-Test%20Artifacts-blue)
![CodeQL](https://img.shields.io/badge/CodeQL-Static%20Analysis-2F80ED?logo=github&logoColor=white)
![Gitleaks](https://img.shields.io/badge/Gitleaks-Secret%20Scanning-orange)
![Trivy](https://img.shields.io/badge/Trivy-Filesystem%20%2B%20Container%20Scanning-1904DA)
![SBOM](https://img.shields.io/badge/SBOM-CycloneDX-2D9CDB)
![Dependabot](https://img.shields.io/badge/Dependabot-Python%20%7C%20Actions%20%7C%20Docker-025E8C?logo=dependabot&logoColor=white)
![pip-audit](https://img.shields.io/badge/pip--audit-Dependency%20Audit-blueviolet)
![Release](https://img.shields.io/badge/Release-GitHub%20Artifacts-success)
![Semantic Versioning](https://img.shields.io/badge/SemVer-Tag%20Driven-orange)
![Security Policy](https://img.shields.io/badge/Security-Policy%20Added-success)
![Contributing](https://img.shields.io/badge/Contributing-Guidelines%20Added-blue)
![L6 Hygiene](https://img.shields.io/badge/L6%20Hygiene-9--Tier%20Deployment%20Model-gold)
![License](https://img.shields.io/github/license/CoreyLeath-code/TrojanChat)
![Last Commit](https://img.shields.io/github/last-commit/CoreyLeath-code/TrojanChat)
![Repo Size](https://img.shields.io/github/repo-size/CoreyLeath-code/TrojanChat)
![Issues](https://img.shields.io/github/issues/CoreyLeath-code/TrojanChat)
![Pull Requests](https://img.shields.io/github/issues-pr/CoreyLeath-code/TrojanChat)
![Stars](https://img.shields.io/github/stars/CoreyLeath-code/TrojanChat?style=social)

TrojanChat is a production-hardened, multi-client chat architecture optimized for high-concurrency environments. Moving away from standard blocking network sockets, this platform leverages asynchronous event loops to maintain thousands of concurrent connections efficiently while maintaining structural memory efficiency.

---

 Architectural Overview

 <img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/d9d6fa43-1152-4550-89b6-bcf2cebdf248" />


The platform splits operations across an event-driven system architecture to eliminate thread-starvation issues under scale.

* **Non-Blocking Core:** Built on top of Python's raw `asyncio` streams API, replacing slow multi-threaded overhead with a high-performance single-threaded asynchronous engine.
* **Structured Serialization Protocol:** Completely dropped plaintext string messaging in favor of structured JSON payloads, allowing for strict validation boundaries and predictable message framing.
* **Rootless Isolation Security:** Containers are structurally hardened using explicit multi-stage build patterns, forcing runtime scripts to execute via a dedicated unprivileged user group (`apprunner`).

---

## 🚀 Getting Started

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

├── chat_core/
│   ├── __init__.py
│   ├── config.py             # <-- Application security settings & validation rules
│   ├── crypto_broker.py      # <-- Challenge generation and key distribution logic
│   └── connection_manager.py # <-- Tier 5: High-concurrency socket tracking state loop
├── deployment/
│   ├── gateway.conf          # <-- Tier 2: Envoy or Nginx reverse-proxy ingress rules
│   ├── docker-compose.yml    # <-- Full local container environment mesh (Redis, App, Postgres)
│   └── Dockerfile            # <-- Minimal production runtime workspace blueprint
├── tests/
│   ├── unit/                 # <-- Job #3: Asynchronous socket validation benches
│   └── schemas/              # <-- Job #7: JSON framing contract tests
├── dailylog.md               # <-- Maintenance operations history ledger
└── requirements.txt          # <-- Managed dependencies


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
