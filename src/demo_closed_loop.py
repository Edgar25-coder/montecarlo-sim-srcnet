import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

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
    build_parameters,
    build_topology,
)


DAYS = 90

SEED = 1234

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_FILE = PROJECT_ROOT / "closed_loop_results.csv"
PLOT_FILE = PROJECT_ROOT / "closed_loop_occupancy.png"


def build_world():

    rng = np.random.default_rng(SEED)
    topology = build_topology()

    return SRCNetWorld(
        topology=topology,
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(
            rng,
            topology,
        ),
    )


def run_closed_loop():

    world = build_world()
    optimizer = SRCNetOptimizer()
    applier = DecisionApplier()
    daily_results = []

    for day in range(1, DAYS + 1):

        state = world.step()
        solution = optimizer.solve(state)

        if solution.is_feasible:

            applier.apply(
                world,
                solution,
            )

        daily_row = {
            "day": day,
            "active_datasets": len(world.datasets),
            "new_arrivals": state.new_arrivals,
            "expired_datasets": state.expired_datasets,
            "placements": len(solution.placements),
            "replicas": len(solution.replicas),
            "objective_value": solution.objective_value,
            "is_feasible": solution.is_feasible,
            "is_optimal": solution.is_optimal,
        }

        for node, occupancy in world.storage_occupancy.items():

            daily_row[f"storage_{node}_pb"] = occupancy

        daily_results.append(daily_row)

        print(
            f"Day {day:3d}/{DAYS}: "
            f"datasets={len(world.datasets):4d}, "
            f"arrivals={state.new_arrivals:2d}, "
            f"expired={state.expired_datasets:2d}, "
            f"feasible={solution.is_feasible}, "
            f"placements={len(solution.placements):4d}, "
            f"replicas={len(solution.replicas):4d}"
        )

    with RESULTS_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=list(daily_results[0]),
        )
        writer.writeheader()
        writer.writerows(daily_results)

    days = [row["day"] for row in daily_results]
    fig, axis = plt.subplots(figsize=(12, 6))

    for node in world.storage_occupancy:

        axis.plot(
            days,
            [row[f"storage_{node}_pb"] for row in daily_results],
            label=node,
        )

    axis.set_title("Closed-Loop Storage Occupancy")
    axis.set_xlabel("Day")
    axis.set_ylabel("Occupancy (PB)")
    axis.grid(True, alpha=0.3)
    axis.legend(title="Node")
    fig.tight_layout()
    fig.savefig(PLOT_FILE, dpi=200)
    plt.close(fig)

    feasible_days = sum(
        row["is_feasible"]
        for row in daily_results
    )

    print(f"\nFeasible optimization days: {feasible_days}/{DAYS}")
    print(f"Results written to: {RESULTS_FILE}")
    print(f"Occupancy plot written to: {PLOT_FILE}")

    return daily_results


def main():

    run_closed_loop()


if __name__ == "__main__":

    main()
