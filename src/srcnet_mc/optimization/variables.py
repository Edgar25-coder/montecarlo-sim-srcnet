from pyscipopt import Model


class VariableFactory:

    def __init__(
        self,
        model: Model,
    ):

        self.model = model

    def create_placement_variables(
        self,
        scenario,
    ):

        x = {}

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            for node in (
                scenario.storage_nodes
            ):

                x[
                    dataset_id,
                    node,
                ] = self.model.addVar(
                    vtype="B",
                    name=(
                        f"x_"
                        f"{dataset_id}_"
                        f"{node}"
                    ),
                )

        return x

    def create_replica_variables(
        self,
        scenario,
    ):

        y = {}

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            for node in (
                scenario.storage_nodes
            ):

                y[
                    dataset_id,
                    node,
                ] = self.model.addVar(
                    vtype="B",
                    name=(
                        f"y_"
                        f"{dataset_id}_"
                        f"{node}"
                    ),
                )

        return y