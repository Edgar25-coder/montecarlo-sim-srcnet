import numpy as np

from srcnet_mc.domain.model import (
    Arc,
    Node,
    NodeRole,
    Topology,
)

from srcnet_mc.domain.markov import (
    LinkState,
    MarkovChain,
)

from srcnet_mc.domain.parameters import (
    SimulationParameters,
    LinkParameters,
    LinkStateParameters,
    BetaMoments,
    LogNormalMoments,
    DatasetParameters,
    PoissonRate,
    WeibullMoments,
)

from srcnet_mc.domain.srcnet_world import (
    SRCNetWorld,
)


def build_parameters():

    normal = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.95,
            variance=0.001,
        ),
        latency=LogNormalMoments(
            mean=20.0,
            cv=0.10,
        ),
    )

    congested = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.70,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=50.0,
            cv=0.20,
        ),
    )

    degraded = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.40,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=120.0,
            cv=0.30,
        ),
    )

    return SimulationParameters(
        link_parameters=LinkParameters(
            normal=normal,
            congested=congested,
            degraded=degraded,
        ),
        dataset_parameters=DatasetParameters(
            arrivals=PoissonRate(
                rate=5.0
            ),
            size_distribution=LogNormalMoments(
                mean=1.0,
                cv=1.0,
            ),
            retention_distribution=WeibullMoments(
                mean_lifetime_days=365.0,
                shape=1.5,
            ),
        ),
    )


def build_topology():

    topology = Topology(
        nodes=(
            Node(
                identifier="T0",
                role=NodeRole.T0,
            ),
            Node(
                identifier="SRC1",
                role=NodeRole.NON_T0,
            ),
        ),
        arcs=(
            Arc(
                tail="T0",
                head="SRC1",
                capacity_pb_per_day=10.0,
            ),
        ),
    )

    topology.validate()

    return topology


def build_chains(rng):

    transition_matrix = np.array(
        [
            [0.90, 0.10, 0.00, 0.00],
            [0.10, 0.80, 0.10, 0.00],
            [0.00, 0.10, 0.80, 0.10],
            [0.20, 0.10, 0.00, 0.70],
        ]
    )

    return {
        ("T0", "SRC1"): MarkovChain(
            transition_matrix=transition_matrix,
            initial_state=LinkState.NORMAL,
            rng=rng,
        )
    }


def print_state(state):

    print("\n" + "=" * 60)
    print(f"DAY {state.day}")
    print("=" * 60)

    print("\nNETWORK")

    for arc_key, arc_state in state.arc_states.items():

        print(
            f"\nArc {arc_key}"
        )

        print(
            f"  State: {arc_state.state.name}"
        )

        print(
            f"  Capacity: "
            f"{arc_state.effective_capacity_pb_per_day:.4f} PB/day"
        )

        print(
            f"  Latency: "
            f"{arc_state.latency_ms:.4f} ms"
        )

    print("\nDATASETS")

    print(
        f"  New arrivals today: "
        f"{state.new_arrivals}"
    )

    print(
        f"  Expired today: "
        f"{state.expired_datasets}"
    )

    print(
        f"  Active datasets: "
        f"{len(state.datasets)}"
    )

    if state.datasets:

        total_volume = sum(
            ds.dataset.volume_pb
            for ds in state.datasets.values()
        )

        avg_age = (
            sum(
                ds.age_days
                for ds in state.datasets.values()
            )
            /
            len(state.datasets)
        )

        print(
            f"  Total dataset volume: "
            f"{total_volume:.4f} PB"
        )

        print(
            f"  Average age: "
            f"{avg_age:.2f} days"
        )

    print("\nSTORAGE")

    for node, occupancy in (
        state.storage_occupancy_pb.items()
    ):

        print(
            f"  {node}: "
            f"{occupancy:.4f} PB"
        )


def print_summary(states):

    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)

    final_state = states[-1]

    total_arrivals = sum(
        s.new_arrivals
        for s in states
    )

    total_expired = sum(
        s.expired_datasets
        for s in states
    )

    print(
        f"Days simulated: "
        f"{len(states)}"
    )

    print(
        f"Total arrivals: "
        f"{total_arrivals}"
    )

    print(
        f"Total expirations: "
        f"{total_expired}"
    )

    print(
        f"Active datasets at end: "
        f"{len(final_state.datasets)}"
    )

    for node, occupancy in (
        final_state.storage_occupancy_pb.items()
    ):

        print(
            f"Final occupancy {node}: "
            f"{occupancy:.4f} PB"
        )


def main():

    SEED = 1234

    DAYS = 10

    print(
        "\nSRCNet Phase A Demo"
    )

    print(
        f"Seed = {SEED}"
    )

    print(
        f"Days = {DAYS}"
    )

    rng = np.random.default_rng(SEED)

    world = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(rng),
    )

    states = []

    for _ in range(DAYS):

        state = world.step()

        states.append(state)

        print_state(state)

    print_summary(states)


if __name__ == "__main__":
    main()