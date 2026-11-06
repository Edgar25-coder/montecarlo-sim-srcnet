import numpy as np
import matplotlib.pyplot as plt

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


# =====================================================
# Fixtures (idénticas a las utilizadas en los tests)
# =====================================================

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
                rate=5.0,
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


# =====================================================
# Demo
# =====================================================

def main():

    SEED = 1234

    DAYS = 10

    rng = np.random.default_rng(SEED)

    world = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(rng),
    )

    occupancy_history = []
    datasets_history = []
    arrivals_history = []
    expirations_history = []
    markov_history = []
    capacity_history = []
    latency_history = []

    states = []

    for _ in range(DAYS):

        state = world.step()

        states.append(state)

        occupancy_history.append(
            state.storage_occupancy_pb["T0"]
        )

        datasets_history.append(
            len(state.datasets)
        )

        arrivals_history.append(
            state.new_arrivals
        )

        expirations_history.append(
            state.expired_datasets
        )

        arc_state = state.arc_states[
            ("T0", "SRC1")
        ]

        markov_history.append(
            arc_state.state.value
        )

        capacity_history.append(
            arc_state.effective_capacity_pb_per_day
        )

        latency_history.append(
            arc_state.latency_ms
        )

    # ========================================
    # Resumen
    # ========================================

    print("\n===================================")
    print("SRCNET WORLD SUMMARY")
    print("===================================\n")

    print(f"Seed: {SEED}")
    print(f"Days simulated: {DAYS}")

    print(
        f"Total arrivals: "
        f"{sum(arrivals_history)}"
    )

    print(
        f"Total expirations: "
        f"{sum(expirations_history)}"
    )

    print(
        f"Active datasets: "
        f"{len(states[-1].datasets)}"
    )

    print(
        f"Final occupancy T0: "
        f"{occupancy_history[-1]:.3f} PB"
    )

    # ========================================
    # Gráficos
    # ========================================

    fig, axes = plt.subplots(
        3,
        2,
        figsize=(14, 12),
    )

    ax = axes[0, 0]

    ax.plot(
        occupancy_history,
        linewidth=2,
    )

    ax.set_title(
        "Storage Occupancy"
    )

    ax.set_xlabel("Day")

    ax.set_ylabel("PB")

    # --------------------------------

    ax = axes[0, 1]

    ax.plot(
        datasets_history,
        linewidth=2,
    )

    ax.set_title(
        "Active Datasets"
    )

    ax.set_xlabel("Day")

    ax.set_ylabel("Datasets")

    # --------------------------------

    ax = axes[1, 0]

    ax.plot(
        arrivals_history,
        label="Arrivals",
    )

    ax.plot(
        expirations_history,
        label="Expired",
    )

    ax.legend()

    ax.set_title(
        "Dataset Lifecycle"
    )

    ax.set_xlabel("Day")

    # --------------------------------

    ax = axes[1, 1]

    ax.step(
        range(DAYS),
        markov_history,
        where="post",
    )

    ax.set_yticks(
        [0, 1, 2, 3]
    )

    ax.set_yticklabels(
        [
            "NORMAL",
            "CONGESTED",
            "DEGRADED",
            "FAILED",
        ]
    )

    ax.set_title(
        "Markov Link State"
    )

    ax.set_xlabel("Day")

    # --------------------------------

    ax = axes[2, 0]

    ax.plot(
        capacity_history,
        linewidth=2,
    )

    ax.set_title(
        "Effective Capacity"
    )

    ax.set_xlabel("Day")

    ax.set_ylabel("PB/day")

    # --------------------------------

    ax = axes[2, 1]

    ax.plot(
        latency_history,
        linewidth=2,
    )

    ax.set_title(
        "Latency"
    )

    ax.set_xlabel("Day")

    ax.set_ylabel("ms")

    # --------------------------------

    fig.tight_layout()

    plt.savefig(
        "phaseA_summary.png",
        dpi=200,
    )

    plt.show()


if __name__ == "__main__":
    main()