from dataclasses import dataclass


@dataclass(frozen=True)
class PlacementDecision:

    dataset_id: str

    destination_node: str


@dataclass(frozen=True)
class ReplicaDecision:

    dataset_id: str

    node: str


@dataclass(frozen=True)
class OptimizationSolution:

    objective_value: float

    placements: list[PlacementDecision]

    replicas: list[ReplicaDecision]

    is_feasible: bool

    is_optimal: bool