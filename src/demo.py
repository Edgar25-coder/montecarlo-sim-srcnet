import csv

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


# ==========================================================
# PARAMETERS
# ==========================================================

def build_parameters():
    normal = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.95,
            variance=0.001,
        ),
        latency=LogNormalMoments(
            mean=20,
            cv=0.10,
        ),
    )

    congested = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.70,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=50,
            cv=0.20,
        ),
    )

    degraded = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.40,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=120,
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


# ==========================================================
# TOPOLOGY
# ==========================================================

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
            Node(
                identifier="SRC2",
                role=NodeRole.NON_T0,
            ),
            Node(
                identifier="SRC3",
                role=NodeRole.NON_T0,
            ),
            Node(
                identifier="TRANS1",
                role=NodeRole.TRANSIT,
            ),
            Node(
                identifier="ST1",
                role=NodeRole.STORAGE,
                parent_se="SRC1",
            ),
            Node(
                identifier="ST2",
                role=NodeRole.STORAGE,
                parent_se="SRC3",
            ),
        ),
        arcs=(
            Arc(
                tail="T0",
                head="SRC1",
                capacity_pb_per_day=10.0,
            ),
            Arc(
                tail="T0",
                head="SRC2",
                capacity_pb_per_day=12.0,
            ),
            Arc(
                tail="T0",
                head="SRC3",
                capacity_pb_per_day=8.0,
            ),
            Arc(
                tail="SRC1",
                head="TRANS1",
                capacity_pb_per_day=6.0,
            ),
            Arc(
                tail="SRC2",
                head="TRANS1",
                capacity_pb_per_day=7.0,
            ),
            Arc(
                tail="SRC3",
                head="TRANS1",
                capacity_pb_per_day=5.0,
            ),
            Arc(
                tail="SRC1",
                head="ST1",
                capacity_pb_per_day=4.0,
            ),
            Arc(
                tail="SRC3",
                head="ST2",
                capacity_pb_per_day=4.0,
            ),
            Arc(
                tail="TRANS1",
                head="ST1",
                capacity_pb_per_day=3.0,
            ),
            Arc(
                tail="TRANS1",
                head="ST2",
                capacity_pb_per_day=3.0,
            ),
        ),
    )

    topology.validate()
    return topology


# ==========================================================
# MARKOV CHAINS
# ==========================================================

def build_chains(rng, topology):
    transition_matrix = np.array(
        [
            [0.90, 0.10, 0.00, 0.00],
            [0.10, 0.80, 0.10, 0.00],
            [0.00, 0.10, 0.80, 0.10],
            [0.20, 0.10, 0.00, 0.70],
        ]
    )

    chains = {}

    for arc in topology.arcs:
        chains[(arc.tail, arc.head)] = MarkovChain(
            transition_matrix=transition_matrix,
            initial_state=LinkState.NORMAL,
            rng=rng,
        )

    return chains


# ==========================================================
# MAIN
# ==========================================================

def main():
    seed = 1234
    days = 90
    results_file = "phaseA_10_links_daily_results.csv"

    topology = build_topology()
    rng = np.random.default_rng(seed)

    world = SRCNetWorld(
        topology=topology,
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(
            rng,
            topology,
        ),
    )

    occupancy = []
    datasets = []
    arrivals = []
    expirations = []
    daily_results = []

    state_counter = {
        "NORMAL": 0,
        "CONGESTED": 0,
        "DEGRADED": 0,
        "FAILED": 0,
    }

    print("\n===================================================")
    print("SRCNET PHASE A + LAYER 2 DEMO")
    print("===================================================")
    print(f"Seed = {seed}")
    print(f"Days = {days}")
    print(f"Nodes = {len(topology.nodes)}")
    print(f"Arcs = {len(topology.arcs)}")

    for day in range(days):
        state = world.step()

        active_datasets = len(state.datasets)

        occupancy.append(
            state.storage_occupancy_pb["T0"]
        )
        datasets.append(active_datasets)
        arrivals.append(state.new_arrivals)
        expirations.append(state.expired_datasets)

        daily_row = {
            "day": day + 1,
            "active_datasets": active_datasets,
            "new_arrivals": state.new_arrivals,
            "expired_datasets": state.expired_datasets,
        }

        for (tail, head), arc_state in state.arc_states.items():
            arc_column = f"arc_{tail}_{head}_state"
            daily_row[arc_column] = arc_state.state.name
            state_counter[arc_state.state.name] += 1

        for node_id, value in state.storage_occupancy_pb.items():
            daily_row[f"storage_{node_id}_pb"] = value

        daily_results.append(daily_row)

    if daily_results:
        with open(
            results_file,
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=list(daily_results[0].keys()),
            )
            writer.writeheader()
            writer.writerows(daily_results)

        print(f"\nResultados diarios guardados en {results_file}")

    print("\n----------------------")
    print("FINAL STATE")
    print("----------------------")
    print(f"Active datasets: {len(state.datasets)}")
    print(
        f"T0 occupancy: "
        f"{state.storage_occupancy_pb['T0']:.3f} PB"
    )
    print(f"Total arrivals: {sum(arrivals)}")
    print(f"Total expired: {sum(expirations)}")

    print("\nMarkov states observed")
    for state_name, count in state_counter.items():
        print(f"  {state_name:10s} : {count}")

    # ======================================================
    # PLOTS
    # ======================================================

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8),
    )

    axes[0, 0].plot(
        occupancy,
        linewidth=2,
    )
    axes[0, 0].set_title("T0 Storage Occupancy")
    axes[0, 0].set_xlabel("Day")
    axes[0, 0].set_ylabel("PB")

    axes[0, 1].plot(
        datasets,
        linewidth=2,
    )
    axes[0, 1].set_title("Active Datasets")
    axes[0, 1].set_xlabel("Day")
    axes[0, 1].set_ylabel("Datasets")

    axes[1, 0].plot(
        arrivals,
        label="Arrivals",
    )
    axes[1, 0].plot(
        expirations,
        label="Expired",
    )
    axes[1, 0].legend()
    axes[1, 0].set_title("Dataset Lifecycle")
    axes[1, 0].set_xlabel("Day")
    axes[1, 0].set_ylabel("Datasets")

    axes[1, 1].bar(
        list(state_counter.keys()),
        list(state_counter.values()),
    )
    axes[1, 1].set_title("Markov State Frequencies")
    axes[1, 1].set_xlabel("Link state")
    axes[1, 1].set_ylabel("Observations")

    fig.tight_layout()

    plt.savefig(
        "phaseA_10_links_summary.png",
        dpi=200,
    )

    print("\nFigure saved as phaseA_10_links_summary.png")
    plt.show()


if __name__ == "__main__":
    main()