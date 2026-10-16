# Scenario, policy, and reproducibility contracts

## Feature matrix

| Feature | S1 | S2 | S3 | S4 |
| --- | --- | --- | --- | --- |
| Fixed synthetic workload | yes | yes | yes | no; Poisson arrivals |
| Storage reset each day | yes | yes | yes | no |
| Network state | deterministic | independent failure draws | per-link Markov trace | per-link Markov trace |
| Conditional capacity/latency sampling | fixed | fixed operational values | yes | yes |
| Retention and occupancy | no | no | no | yes |
| Direct reception | no | no | no | yes |
| Online re-optimisation | no | no | no | yes |

## Policy contract

`Policy.decide(observed_state, demands) -> DecisionResult` receives only the current day, current network/storage values, current demands and static configuration. It never receives a future trace or a mutable global RNG.

The offline policy is a static, non-clairvoyant placement-template rule. The online policy may optimise only each day's new demands. Existing persistent copies remain immutable; migration is outside scope.

## Daily S4 boundary

1. Transition each link from `X(t-1)` to `X(t)`; the configured initial distribution describes `X(0)`.
2. Sample operational capacities and latencies.
3. Age and expire existing stored datasets; release their exact persistent volume.
4. Generate new demands and sample their size and one shared retention lifetime.
5. Present free capacity to the policy/optimiser, validate a usable solution, then atomically commit complete replicas.
6. New datasets begin at age zero. An infeasible batch is rejected in full, without a queue or retry.

## RNG and run identity

Use NumPy `SeedSequence` with stable keys `(root_seed, replication_id, component_name)`. Separate streams are required for link states, capacities, latencies, arrivals, sizes, retention and policy randomness. The harness reuses immutable exogenous traces for paired policies. Worker count and execution order must not affect any scientific draw.

Each output campaign will retain the source hash, configuration hash, Git revision/dirty state, dependency/solver versions, root seed, stream scheme, OS/architecture, solver options, status counts and output schema version. Resume is permitted only when compatible hashes match.
