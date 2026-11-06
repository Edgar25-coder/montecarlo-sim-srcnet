from dataclasses import dataclass

from srcnet_mc.optimization.distances import (
    build_distance_matrix,
)

from srcnet_mc.domain.world_state import (
    WorldState,
)

from srcnet_mc.domain.markov import (
    LinkState,
)


@dataclass(frozen=True)
class OptimizationScenario:

    world_state: WorldState

    datasets: tuple

    storage_nodes: tuple

    current_occupancy: dict[str, float]

    capacities: dict[str, float]

    distances: dict

    failure_risk: dict[str, float]

    latency_costs: dict[str, float]

    capacity_costs: dict[str, float]

    failed_nodes: set[str]


def build_scenario(
    world_state: WorldState,
):

    print(
        world_state.storage_occupancy_pb
    )

    storage_nodes = tuple(
        world_state.storage_occupancy_pb.keys()
    )

    distances = build_distance_matrix(
        storage_nodes,
    )

    capacities = {}

    #
    # Para la primera implementación
    # utilizamos capacidad fija.
    #
    for node in storage_nodes:

        capacities[node] = 10000.0

    failure_risk = {}

    for node in storage_nodes:

        if node == "T0":

            failure_risk[node] = 0.50

        else:

            failure_risk[node] = 0.25

    latency_costs = {}
    capacity_costs = {}

    for node in storage_nodes:

        latency_costs[node] = 1000.0

        capacity_costs[node] = 1000.0

    failed_nodes = set()

    for (tail, head), arc_state in (
        world_state.arc_states.items()
    ):

        if arc_state.state == LinkState.FAILED:

            failed_nodes.add(head)

            continue

        latency_costs[head] = (
            arc_state.latency_ms
        )

        capacity_costs[head] = (
            arc_state.effective_capacity_pb_per_day
        )

    datasets = tuple(
        world_state.datasets.values()
    )
    current_occupancy = (
        world_state.storage_occupancy_pb
    )

    return OptimizationScenario(
        world_state=world_state,
        datasets=datasets,
        storage_nodes=storage_nodes,
        current_occupancy=current_occupancy,
        capacities=capacities,
        distances=distances,
        failure_risk=failure_risk,
        latency_costs=latency_costs,
        capacity_costs=capacity_costs,
        failed_nodes=failed_nodes,
    )
