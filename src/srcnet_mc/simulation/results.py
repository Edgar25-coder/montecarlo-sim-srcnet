from dataclasses import dataclass


@dataclass(frozen=True)
class ReplicationResult:

    replication_id: int

    economic_cost: float

    exposure_cost: float

    throughput: float

    congestion_cost: float

    resilience_cost: float

    efficiency: float

    active_datasets: int

    total_occupancy_pb: float

    objective_value: float