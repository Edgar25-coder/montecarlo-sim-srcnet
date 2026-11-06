from dataclasses import dataclass

from srcnet_mc.domain.dataset_instance import (
    DatasetInstance,
)

from srcnet_mc.domain.markov import (
    LinkState,
)


@dataclass
class ArcState:

    state: LinkState

    effective_capacity_pb_per_day: float

    latency_ms: float


@dataclass
class WorldState:

    day: int

    arc_states: dict[tuple[str, str], ArcState]

    storage_occupancy_pb: dict[str, float]

    datasets: dict[str, DatasetInstance]

    new_arrivals: int

    expired_datasets: int