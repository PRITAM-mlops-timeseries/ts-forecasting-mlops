# CLAUDE.md — ts-forecasting-mlops

This file is read automatically by Claude Code at the start of every session. It captures all decisions made during planning, so implementation sessions stay aligned without re-explaining context each time.

---

## Project Identity

**Repo:** github.com/PRITAM-mlops-timeseries/ts-forecasting-mlops (public)
**Goal:** A production-grade time series forecasting project combining Marco Peixeiro's *Time Series Forecasting in Python* theory with a full open-source-first MLOps stack, built with professional-grade OOP — not notebooks.

**Domain:** Hierarchical retail demand forecasting using the **M5 dataset** (Walmart) — full complexity from day one, no toy subset. Chosen because multiple stores × departments × items, plus exogenous regressors (price, promotions, SNAP, calendar events), justifies genuine software design depth.

**Pacing:** No fixed timeline. Each phase finishes properly before the next starts. Depth over deadlines.

## Core Design Philosophy

- **Vertical slice early**: data → model → tracking → eval works end-to-end by the close of Phase 2. Every phase after that deepens modeling or engineering sophistication — nothing gets "productionized later."
- **Interface-driven architecture**: every model (statistical, ML, DL) implements the same `BaseForecaster` ABC contract.
- **Config-driven, no hardcoding**: Pydantic Settings for all paths, hyperparameters, service URIs.
- **Leak-proof by construction**: no future information leaks into training features, enforced by design, not just tested for.
- **SOLID made explicit**: every new class/module gets checked against Single Responsibility and Open/Closed as it's designed. Pattern choices get named against the SOLID principle they demonstrate:
  - `BaseForecaster` ABC → Liskov Substitution
  - Adding models without touching pipeline code → Open/Closed
  - `DataRepository` abstraction → Dependency Inversion
  - Strategy pattern for feature engineering → Single Responsibility
  - FastAPI dependency injection → Interface Segregation
- **DSA/algorithmic efficiency**: flagged inline only when genuinely relevant to the code being written (e.g. O(n²) rolling-window traps vs. deque-based O(n) approaches) — never a separate study track.
- **Gap-filling**: when the book assumes prior knowledge, either point to the specific chapter or generate a focused note (concept, intuition, math, code mapping) in the moment.

## Tool Stack (final, all open source except GitHub Actions)

| Layer | Tool | OSS? |
|---|---|---|
| Env/dependency management | uv | Yes |
| Structured & document data | PostgreSQL (relational + JSONB) | Yes |
| Caching / online feature store / task broker | Valkey (BSD, not Redis — license history) | Yes |
| Experiment tracking & model registry | MLflow | Yes |
| Data versioning | DVC | Yes |
| Data validation | Great Expectations | Yes |
| Hyperparameter tuning | Optuna | Yes |
| Orchestration | Airflow (CeleryExecutor + Valkey broker → KubernetesExecutor in Phase 9) | Yes |
| CI/CD | GitHub Actions | No — accepted pragmatic exception, free + industry standard |
| Containerization | Docker + docker-compose | Yes |
| Serving | FastAPI | Yes |
| Monitoring/drift | Evidently AI | Yes |
| Dashboard | Streamlit | Yes |
| Deployment (Phase 9 stretch) | Kubernetes | Yes |

## Engineering Patterns (must be used, not optional)

ABCs, Factory pattern, Strategy pattern, Repository pattern, Dependency Injection, Pydantic-based config, full type hints (`mypy`, `ruff`, pre-commit hooks), `pytest` unit tests for data pipelines and models.

## Phase Plan

0. Foundation — repo skeleton, `uv`, Pydantic config, `DataRepository` + `SQLRepository` (PostgreSQL), M5 dataset acquisition
1. EDA — decomposition, stationarity, ACF/PACF (Peixeiro ch. 1–3)
2. Baselines & model contract — `BaseForecaster`, naive/smoothing methods, MLflow (Peixeiro ch. 4–6) — **first full vertical slice closes here**
3. ARIMA family — AR/ARIMA/SARIMAX, Great Expectations, DVC (Peixeiro ch. 7–10)
4. Feature-based ML — LightGBM, Strategy-pattern feature pipeline, Optuna, Postgres feature store
5. Deep learning — LSTM/CNN via PyTorch (MPS backend on Apple Silicon), shared training-loop abstraction
6. Orchestration & CI — Airflow DAG (ingest→validate→feature→train→evaluate→register), CeleryExecutor+Valkey, GitHub Actions
7. Serving — FastAPI + DI, Valkey online feature cache, Postgres prediction logging, Docker/docker-compose
8. Monitoring & polish — Evidently AI (JSONB storage), Streamlit dashboard, docs
9. Kubernetes (stretch) — migrate CeleryExecutor→KubernetesExecutor, Docker→K8s

## Team Workflow — Three Environments

| Environment | Role | Identity |
|---|---|---|
| MacBook Air M4, 16GB RAM | **Contributor** — implements phases, opens PRs, writes tests, responds to review | Personal GitHub account (SSH key) |
| Windows (HP, dual-boot) | **Team Lead** — reviews PRs, approves/requests changes, merges to `main` | Personal GitHub account (SSH key) |
| Ubuntu (HP, dual-boot) | **Staging/deployment** — runs the live docker-compose stack persistently, home for Phase 9 K8s | **Deploy key** (repo-scoped, read-only — not a personal identity) |

Rules: no direct pushes to `main` — always feature branch → PR → review → merge. Branch protection requires 1 approval + passing CI. `CODEOWNERS` assigns Team Lead as required reviewer. Repo is **public** (required for free-tier branch protection; also a portfolio benefit) — never commit secrets (`.env`, gitignored) or the raw M5 dataset (Kaggle terms; DVC handles data, not git).

## Current Status (as of this handoff)

- ✅ GitHub Organization + public repo created
- ✅ Branch protection on `main` configured (1 approval + status checks required)
- ✅ MacBook (Contributor) environment set up: git, SSH key, uv, OrbStack, Claude Code installed & authenticated
- ✅ Windows (Team Lead) environment set up: Git for Windows, SSH key, Claude Code installed & authenticated
- ✅ Ubuntu (Staging) environment: Docker installed, deploy key generated and added to repo (read-only)
- ✅ `.gitattributes` and `.github/CODEOWNERS` merged to `main` via `chore/repo-hygiene` PR
- ⬜ Not yet started: actual Phase 0 implementation (repo skeleton, `pyproject.toml` via `uv init`, pre-commit hooks, `DataRepository`/`SQLRepository`, M5 data acquisition)

## What We Want Next

1. **Finish the open `chore/repo-hygiene` PR**: get it approved from the Team Lead (Windows) account and merged, then `git pull origin main` on both MacBook and Ubuntu to sync.
2. **Start Phase 0 for real**, on a new feature branch (e.g. `phase-0/foundation`):
   - `uv init` the project, set up `src/`-layout packaging
   - Pydantic Settings config module
   - Pre-commit hooks (`ruff`, `mypy`, `pytest`)
   - `DataRepository` ABC + `M5Repository` (flat files) + `SQLRepository` (PostgreSQL via SQLAlchemy) implementations
   - Docker-based local PostgreSQL for development
   - Acquire and understand the M5 dataset structure (calendar, sell prices, sales tables)
   - Open a PR when this is in a reviewable state — don't push directly to `main`
3. Continue applying the SOLID/DSA cross-cutting discussion as new classes get designed, and flag Peixeiro chapter references or generate theory notes whenever a gap shows up.

## Module Structure

```
ts-forecasting-mlops/
│
├── src/ts_forecasting/
│   ├── config/          ← Phase 0  Pydantic Settings (paths, DB URIs, service URIs)
│   ├── data/            ← Phase 0  DataRepository ABC + M5Repository + SQLRepository
│   ├── analysis/        ← Phase 1  EDA utilities (decomposition, stationarity, ACF/PACF)
│   ├── models/          ← Phase 2  BaseForecaster ABC, then one subpackage per family
│   │   ├── base.py
│   │   ├── baseline/    ← Phase 2  naive, mean, seasonal naive
│   │   ├── statistical/ ← Phase 3  ARIMA, SARIMAX
│   │   ├── ml/          ← Phase 4  LightGBM
│   │   └── dl/          ← Phase 5  LSTM, CNN (PyTorch/MPS)
│   ├── features/        ← Phase 4  Strategy-pattern feature pipeline
│   ├── training/        ← Phase 2  training loop, MLflow logging, Optuna wiring
│   ├── validation/      ← Phase 3  Great Expectations suites
│   ├── serving/         ← Phase 7  FastAPI app + DI + prediction endpoints
│   ├── monitoring/      ← Phase 8  Evidently AI drift detection
│   └── dashboard/       ← Phase 8  Streamlit app
│
├── dags/                ← Phase 6  Airflow DAGs (outside src — Airflow convention)
├── tests/               ← grows with each phase
├── data/                ← DVC-managed, never git
├── docker/              ← Phase 7  Dockerfiles per service
├── notebooks/           ← Phase 1 only, EDA scratch — never imported by src/
├── pyproject.toml
├── .pre-commit-config.yaml
└── docker-compose.yml   ← Phase 0 (Postgres dev DB), extended each phase
```

### Module–Phase Mapping

| Phase | Modules touched | What gets built |
|---|---|---|
| **0** | `config/`, `data/`, `docker-compose` | Pydantic Settings, `DataRepository` ABC, `M5Repository`, `SQLRepository`, local Postgres container |
| **1** | `analysis/`, `notebooks/` | EDA tools — stationarity tests, decomposition, ACF/PACF plots |
| **2** | `models/base.py`, `models/baseline/`, `training/` | `BaseForecaster`, naive models, MLflow experiment tracking — **first vertical slice** |
| **3** | `models/statistical/`, `validation/` | ARIMA/SARIMAX, Great Expectations suites, DVC pipeline |
| **4** | `models/ml/`, `features/`, `training/` | LightGBM, Strategy-pattern feature pipeline, Optuna tuning, Postgres feature store |
| **5** | `models/dl/`, `training/` | LSTM/CNN, shared training-loop abstraction (MPS backend) |
| **6** | `dags/`, CI config | Airflow DAG wiring all stages, CeleryExecutor + Valkey, GitHub Actions |
| **7** | `serving/`, `docker/` | FastAPI + DI, Valkey online feature cache, Postgres prediction logging, docker-compose extended |
| **8** | `monitoring/`, `dashboard/` | Evidently AI drift, Streamlit dashboard |
| **9** | infra only | K8s manifests, CeleryExecutor → KubernetesExecutor |

### Structural Rules

- `dags/` is outside `src/` — Airflow scans a flat `dags/` dir; DAG code stays thin (orchestration only), business logic lives in the installed `ts_forecasting` package.
- `notebooks/` is never imported by `src/` — EDA scratch only; anything reusable gets promoted into `analysis/`.
- `docker-compose.yml` grows incrementally — starts Phase 0 with Postgres only, gains Valkey, MLflow, Airflow services as phases demand.
- `training/` is shared across all model families — only the model object (conforming to `BaseForecaster`) changes.

## Reference Library (consult only when a specific gap needs it — not required reading)
*Architecture Patterns with Python* (Percival & Gregory) — Repository/DI questions · *Forecasting: Principles and Practice* (Hyndman & Athanasopoulos, free online) — deeper ARIMA/smoothing theory · *Designing Machine Learning Systems* (Huyen) — feature stores/monitoring · *Designing Data-Intensive Applications* (Kleppmann) — why Postgres/Valkey/Airflow behave as they do · *Kubernetes: Up & Running* — Phase 9 only · *Machine Learning Design Patterns* (Lakshmanan et al.) — feature pipeline patterns · *Fluent Python* (Ramalho) — idiomatic polish, any time.
