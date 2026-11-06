from pyscipopt import Model

from srcnet_mc.optimization.variables import (
    VariableFactory,
)

from srcnet_mc.optimization.constraints import (
    ConstraintBuilder,
)

from srcnet_mc.optimization.objective import (
    ObjectiveBuilder,
)

from srcnet_mc.optimization.solution import (
    PlacementDecision,
    ReplicaDecision,
    OptimizationSolution,
)

from srcnet_mc.optimization.scenario import (
    build_scenario,
)


class SRCNetOptimizer:

    def solve(
        self,
        world_state,
    ):

        scenario = build_scenario(
            world_state
        )

        model = Model(
            "SRCNet"
        )

        variables = VariableFactory(
            model
        )

        constraints = ConstraintBuilder(
            model
        )

        objective = ObjectiveBuilder(
            model
        )

        x = (
            variables
            .create_placement_variables(
                scenario
            )
        )

        y = (
            variables
            .create_replica_variables(
                scenario
            )
        )

        constraints.build(
            scenario,
            x,
            y,
        )

        objective.set_objective(
            scenario,
            x,
            y,
        )

        model.optimize()

        status = (
            model.getStatus()
        )

        is_feasible = status in {
            "optimal",
            "feasible",
        }

        is_optimal = (
            status == "optimal"
        )

        placements = []

        replicas = []

        if is_feasible:

            for dataset in (
                scenario.datasets
            ):

                dataset_id = (
                    dataset.dataset.identifier
                )

                for node in (
                    scenario.storage_nodes
                ):

                    if (
                        model.getVal(
                            x[
                                dataset_id,
                                node,
                            ]
                        )
                        > 0.5
                    ):

                        placements.append(
                            PlacementDecision(
                                dataset_id=dataset_id,
                                destination_node=node,
                            )
                        )

                    if (
                        model.getVal(
                            y[
                                dataset_id,
                                node,
                            ]
                        )
                        > 0.5
                    ):

                        replicas.append(
                            ReplicaDecision(
                                dataset_id=dataset_id,
                                node=node,
                            )
                        )

        objective_value = 0.0

        if is_feasible:

            objective_value = (
                model.getObjVal()
            )

        return OptimizationSolution(
            objective_value=objective_value,
            placements=placements,
            replicas=replicas,
            is_feasible=is_feasible,
            is_optimal=is_optimal,
        )