# SRCNet model-to-code traceability

Source: `docs/model/cas-dc-template.tex`  
SHA-256: `230b5df7bab09097089d44c26da6685586cafa5913a62d444e59dfb8c4da7898`  
Status: Phase A baseline; implementation references are planned unless stated otherwise.

| Manuscript anchor | Scientific element | Planned representation | Independent validation |
| --- | --- | --- | --- |
| Sets and Indices, lines 404-459 | Directed topology, SDP/SE/T0/storage/SRC/parent sets and two arc stages | Immutable typed domain records and NetworkX structural checks | Node-role, parent and stage membership checks |
| Parameters, lines 461-554 | Volumes, costs, capacities, compatibility, availability, resilience limits and weights | Validated versioned configuration with units/provenance | Schema and unit/range tests |
| Decision variables, lines 555-586 | Activations, reception, replica placement/origin and continuous flows | PySCIPOpt variable builder | Tiny exhaustive reference comparison |
| Objectives, lines 587-754 | Economic cost, energy, temporal proxy, congestion, exposure and maximum utilisation | Objective registry; exact SCIP congestion term | Original objective recalculation from a returned solution |
| Constraints, lines 755-1032 | Reception, replica, flow, resource, availability, diversity, distance and exposure families | `optimization/deterministic.py` plus `optimization/validation.py` | Positive and negative synthetic-fixture checks; wider configurations remain future work |
| Monte Carlo, lines 1684-1933 | Daily horizon, Markov states, conditional sampling, arrivals, occupancy and retention | Stochastic trace and daily-state modules | Moment, transition, age/expiry and mass-balance tests |
| Procedure/policies, lines 1934-1961 | Daily ordering and offline/online behaviour | Explicit state transition and restricted policy interface | No-future-access and state-isolation tests |
| Indicators/scenarios, lines 1962-2012 | Six objectives, success/availability/compliance/direct metrics, S1-S4 | Scenario registry and replication summaries | Scenario-isolation and denominator tests |

## Preserved distinctions

- Dataset replicas are indivisible complete copies; continuous flows do not add an unrequested unsplittable-path constraint.
- `C_RR` is the manuscript's failure-distance exposure proxy, not a count or cost of rerouting.
- `T` remains a flow-weighted objective term and is not presented as a measured dataset completion latency.
- Failed links have zero flow and no congestion expression is evaluated for their zero capacity.

