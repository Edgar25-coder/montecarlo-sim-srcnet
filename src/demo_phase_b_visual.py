import numpy as np
import matplotlib.pyplot as plt

from srcnet_mc.domain.srcnet_world import (
    SRCNetWorld,
)

from srcnet_mc.optimization.optimizer import (
    SRCNetOptimizer,
)

from srcnet_mc.optimization.decision_applier import (
    DecisionApplier,
)

from demo import (
    build_chains,
    build_topology,
)

#
# Reutilizamos los parámetros validados
# en la Fase A.
#
from tests_opt.conftest import (
    simulation_parameters,
)


def build_world():

    rng = np.random.default_rng(1234)

    tp = build_topology()

    params = simulation_parameters.__wrapped__()

    mk_chains = build_chains(
        rng,
        tp,
    )

    return SRCNetWorld(
        topology=tp,
        parameters=params,
        rng=rng,
        chains=mk_chains,
    )


def print_solution(solution):

    print("\n")
    print("=" * 60)
    print("OPTIMIZATION SOLUTION")
    print("=" * 60)

    print(
        f"Feasible : {solution.is_feasible}"
    )

    print(
        f"Optimal  : {solution.is_optimal}"
    )

    print(
        f"Objective: "
        f"{solution.objective_value:.3f}"
    )

    print("\nPLACEMENTS")

    for placement in solution.placements[:20]:

        print(
            f"  "
            f"{placement.dataset_id}"
            f" -> "
            f"{placement.destination_node}"
        )

    if len(solution.placements) > 20:

        print("  ...")

    print("\nREPLICAS")

    for replica in solution.replicas[:20]:

        print(
            f"  "
            f"{replica.dataset_id}"
            f" -> "
            f"{replica.node}"
        )

    if len(solution.replicas) > 20:

        print("  ...")


def main():

    print("\n")
    print("=" * 70)
    print("SRCNET PHASE B VISUAL DEMO")
    print("=" * 70)

    world = build_world()

    #
    # Generar un estado razonable.
    #
    for _ in range(5):

        state = world.step()

    print("\nSTATE BEFORE OPTIMIZATION")

    print(
        f"Datasets: "
        f"{len(state.datasets)}"
    )

    print("\nDATASET AGES BEFORE OPTIMIZATION")
    print("-" * 40)

    for dataset_instance in state.datasets.values():

        print(
            f"{dataset_instance.dataset.identifier:>4s}"
            f" | age={dataset_instance.age_days:3d}"
            f" | retention={dataset_instance.retention_days:8.2f}"
            f" | size={dataset_instance.dataset.volume_pb:6.3f} PB"
        )

    occupancy_before = (
        state.storage_occupancy_pb.copy()
    )

    for node, value in occupancy_before.items():

        print(
            f"{node}: "
            f"{value:.3f} PB"
        )

    #
    # Optimización.
    #
    optimizer = SRCNetOptimizer()

    solution = optimizer.solve(
        state
    )

    print_solution(solution)

    print()
    print("REPLICATED DATASETS")

    replicated_ids = {
        replica.dataset_id
        for replica in solution.replicas
    }

    print(sorted(replicated_ids))

    print()
    print("NEW DATASETS")

    new_ids = []

    for dataset_instance in state.datasets.values():

        if dataset_instance.age_days == 0:

            new_ids.append(
                dataset_instance.dataset.identifier
            )

    print(sorted(new_ids))

    #
    # Aplicar decisiones.
    #
    applier = DecisionApplier()

    applier.apply(
        world,
        solution,
    )

    occupancy_after = (
        world.storage_occupancy.copy()
    )

    #
    # Estadísticas.
    #
    placements_per_node = {}

    replicas_per_node = {}

    for placement in solution.placements:

        node = placement.destination_node

        placements_per_node[node] = (
            placements_per_node.get(node, 0)
            + 1
        )

    for replica in solution.replicas:

        node = replica.node

        replicas_per_node[node] = (
            replicas_per_node.get(node, 0)
            + 1
        )

    nodes = sorted(
        occupancy_after.keys()
    )

    before_values = [
        occupancy_before.get(
            node,
            0.0,
        )
        for node in nodes
    ]

    after_values = [
        occupancy_after.get(
            node,
            0.0,
        )
        for node in nodes
    ]

    placement_counts = [
        placements_per_node.get(
            node,
            0,
        )
        for node in nodes
    ]

    replica_counts = [
        replicas_per_node.get(
            node,
            0,
        )
        for node in nodes
    ]

    #
    # GRÁFICOS
    #
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14, 10),
    )

    #
    # Occupancy before/after.
    #
    x = np.arange(len(nodes))

    width = 0.35

    axes[0, 0].bar(
        x - width / 2,
        before_values,
        width,
        label="Before",
    )

    axes[0, 0].bar(
        x + width / 2,
        after_values,
        width,
        label="After",
    )

    axes[0, 0].set_title(
        "Storage Occupancy"
    )

    axes[0, 0].set_xticks(x)

    axes[0, 0].set_xticklabels(nodes)

    axes[0, 0].set_ylabel(
        "PB"
    )

    axes[0, 0].legend()

    #
    # Placements.
    #
    axes[0, 1].bar(
        nodes,
        placement_counts,
    )

    axes[0, 1].set_title(
        "Placements per Node"
    )

    axes[0, 1].set_ylabel(
        "Placements"
    )

    #
    # Replicas.
    #
    axes[1, 0].bar(
        nodes,
        replica_counts,
    )

    axes[1, 0].set_title(
        "Replicas per Node"
    )

    axes[1, 0].set_ylabel(
        "Replicas"
    )

    #
    # Solution summary.
    #
    total_datasets = len(
        state.datasets
    )

    total_replicas = len(
        solution.replicas
    )

    axes[1, 1].bar(
        [
            "Datasets",
            "Replicas",
        ],
        [
            total_datasets,
            total_replicas,
        ],
    )

    axes[1, 1].set_title(
        "Solution Summary"
    )

    fig.suptitle(
        "SRCNet Phase B Demonstration",
        fontsize=14,
    )

    fig.tight_layout()

    plt.savefig(
        "phase_b_visual_demo.png",
        dpi=200,
    )

    print("\n")
    print("=" * 60)
    print("WORLD AFTER APPLY")
    print("=" * 60)

    for node, value in (
        occupancy_after.items()
    ):

        print(
            f"{node}: "
            f"{value:.3f} PB"
        )

    print(
        "\nFigure saved as:"
    )

    print(
        "phase_b_visual_demo.png"
    )

    plt.show()


if __name__ == "__main__":

    main()