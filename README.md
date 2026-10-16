# SRCNet Monte Carlo

Reproducible Python research framework for Monte Carlo experiments on the supplied SRCNet placement and replication model.

Current status: **B1 complete; deterministic reference optimiser not yet implemented.** The manuscript is unchanged. The selected route is an explicit daily NumPy/SciPy loop with PySCIPOpt/SCIP for the exact mixed-integer nonlinear model. A minimal binary/nonlinear compatibility probe passed on macOS Apple Silicon with CPython 3.12; it is not evidence that the complete SRCNet model has been implemented or validated.

## Scientific source and limits

The authoritative source is [docs/model/cas-dc-template.tex](docs/model/cas-dc-template.tex), SHA-256 `230b5df7bab09097089d44c26da6685586cafa5913a62d444e59dfb8c4da7898`. Read [docs/TRACEABILITY.md](docs/TRACEABILITY.md), [MODEL_REVIEW.md](MODEL_REVIEW.md), and [DECISIONS.md](DECISIONS.md) before changing scientific behavior.

Initial runnable inputs will be synthetic fixtures. They must never be described as calibrated SRCNet data or results.

## Setup and validated compatibility check

Native environment, tested on macOS arm64:

```shell
/opt/anaconda3/bin/python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/srcnet-mc probe-scip
```

The probe builds a binary activation variable, continuous flow, and exact congestion expression. Success means SCIP returned `optimal`, activation `1`, flow `2`, and congestion `0.25`.

Container route:

```shell
docker build -t srcnet-mc:local .
docker run --rm srcnet-mc:local probe-scip
```

The Docker base image is digest-pinned. `requirements.lock` is the tested dependency closure; update it only with a Python 3.12 re-test of the probe and suite.

## Accepted contracts

- Transfers complete in their decision day; there is no partial transfer, reservation, retry, or backlog.
- Infeasible batches are rejected atomically and are distinct from solver/backend errors.
- Offline decisions use a static non-clairvoyant template. Online S4 decisions apply only to new arrivals; existing copies are immutable.
- CAPEX is charged once on first activation in a replication.
- S1-S3 use fixed synthetic demand and reset storage daily; S4 adds dynamic occupancy, arrivals, retention, direct reception, and online re-optimisation.
- The Markov initial distribution is `X(0)`. Existing data age/expire before new arrivals; admitted arrivals begin at age zero.

See [docs/SCENARIO_CONTRACTS.md](docs/SCENARIO_CONTRACTS.md) for the feature, policy, daily-boundary, and RNG contracts.

## Repository guide

| File or directory | Purpose |
| --- | --- |
| [CODEX_PROMPT.md](CODEX_PROMPT.md) | Complete project requirements |
| [AGENTS.md](AGENTS.md) | Session, scientific, validation, and Git rules |
| [PLAN.md](PLAN.md) | Current milestones, evidence, blockers, and next action |
| [DECISIONS.md](DECISIONS.md) | Dated scientific and technical decisions |
| [MODEL_REVIEW.md](MODEL_REVIEW.md) | Manuscript ambiguities and missing inputs |
| [docs/TRACEABILITY.md](docs/TRACEABILITY.md) | Model-to-code map and validation responsibilities |
| [docs/SCENARIO_CONTRACTS.md](docs/SCENARIO_CONTRACTS.md) | Scenario, policy, and reproducibility contracts |
| `pyproject.toml`, `requirements.lock`, `Dockerfile` | Pinned native/container setup |
| `src/`, `tests/` | Python implementation and fast scientific checks |

## Not implemented yet

No SRCNet deterministic optimiser, stochastic trace generator, configuration schema, scenario run, restart mechanism, result writer, pilot, or full campaign exists yet. Commands for smoke campaigns, pilots, resume, and reporting will be added only after their implementation has been tested.

## Resource planning

The exact probe is not a benchmark. A full campaign can require at least 360,000 daily online solves before additional policies or re-solves. Runtime, memory, disk, worker count, and solver-thread limits remain pending measured representative pilots. The numerical model has no intrinsic GPU requirement.
