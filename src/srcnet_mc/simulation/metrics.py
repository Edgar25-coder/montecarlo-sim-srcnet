from srcnet_mc.optimization.solution import (
    OptimizationSolution,
)


def compute_economic_cost(
    world,
    solution,
):

    return (
        sum(
            world.storage_occupancy.values()
        )
        +
        len(solution.replicas)
    )


def compute_exposure_cost(
    scenario,
    solution,
):

    return len(
        solution.replicas
    )


def compute_throughput(
    state,
):

    return sum(
        arc.effective_capacity_pb_per_day
        for arc
        in state.arc_states.values()
    )


def compute_congestion_cost(
    state,
):

    congested = 0

    for arc in (
        state.arc_states.values()
    ):

        if (
            arc.state.name
            == "CONGESTED"
        ):
            congested += 1

    return congested


def compute_resilience(
    solution,
):

    return len(
        solution.replicas
    )


def compute_efficiency(
    state,
):

    if len(state.datasets) == 0:

        return 0.0

    return (
        len(state.datasets)
        /
        (
            1.0
            +
            sum(
                state.storage_occupancy_pb.values()
            )
        )
    )