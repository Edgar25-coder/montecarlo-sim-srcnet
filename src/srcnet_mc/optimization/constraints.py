from pyscipopt import quicksum


class ConstraintBuilder:

    def __init__(
        self,
        model,
    ):

        self.model = model

    def add_single_placement_constraint(
        self,
        scenario,
        x,
    ):

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            self.model.addCons(

                quicksum(
                    x[
                        dataset_id,
                        node,
                    ]

                    for node
                    in scenario.storage_nodes
                )

                == 1,

                name=f"assign_{dataset_id}",
            )

    def add_storage_capacity_constraint(
        self,
        scenario,
        x,
        y,
    ):

        for node in scenario.storage_nodes:

            occupancy = (
                scenario.current_occupancy[node]
            )

            capacity = (
                scenario.capacities[node]
            )

            additional_volume = quicksum(

                dataset.dataset.volume_pb

                *

                (
                    x[
                        dataset.dataset.identifier,
                        node,
                    ]
                    +
                    y[
                        dataset.dataset.identifier,
                        node,
                    ]
                )

                for dataset
                in scenario.datasets

            )

            self.model.addCons(

                occupancy
                +
                additional_volume

                <=

                capacity,

                name=f"capacity_{node}",
            )

    def add_receiver_compatibility_constraint(
        self,
        scenario,
        x,
        y,
    ):

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            compatible = (
                dataset.dataset
                .compatible_receivers
            )

            for node in (
                scenario.storage_nodes
            ):

                if node not in compatible:

                    self.model.addCons(
                        x[
                            dataset_id,
                            node,
                        ]
                        == 0
                    )

                    self.model.addCons(
                        y[
                            dataset_id,
                            node,
                        ]
                        == 0
                    )

    def add_replication_constraint(
        self,
        scenario,
        x,
        y,
    ):
        """
        Al menos una réplica.

        Σ y[k,s] >= 1
        """

        for dataset in scenario.datasets:

            if dataset.age_days < 1:

                continue

            dataset_id = (
                dataset.dataset.identifier
            )

            self.model.addCons(

                quicksum(
                    y[
                        dataset_id,
                        node,
                    ]

                    for node
                    in scenario.storage_nodes
                )

                >= 1,

                name=(
                    f"replica_"
                    f"{dataset_id}"
                ),
            )

    def add_replication_delay_constraint(
        self,
        scenario,
        y,
    ):
        """
        Un dataset recién llegado
        no puede replicarse.

        age_days == 0
            => y[k,s] = 0
        """

        for dataset_instance in scenario.datasets:

            dataset_id = (
                dataset_instance.dataset.identifier
            )

            if dataset_instance.age_days < 1:

                for node in scenario.storage_nodes:

                    self.model.addCons(
                        y[
                            dataset_id,
                            node,
                        ]
                        == 0,
                        name=(
                            f"rep_delay_"
                            f"{dataset_id}_"
                            f"{node}"
                        ),
                    )

    def add_replica_separation_constraint(
        self,
        scenario,
        x,
        y,
    ):

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            for node in scenario.storage_nodes:

                self.model.addCons(
                    x[
                        dataset_id,
                        node,
                    ]
                    +
                    y[
                        dataset_id,
                        node,
                    ]
                    <= 1,
                    name=(
                        f"distinct_replica_"
                        f"{dataset_id}_"
                        f"{node}"
                    ),
                )

    def add_minimum_replica_distance_constraint(
        self,
        scenario,
        x,
        y,
    ):

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            minimum_distance = (
                dataset.dataset
                .minimum_replica_distance
            )

            nodes = list(
                scenario.storage_nodes
            )

            for i, node_a in enumerate(nodes):

                for node_b in nodes[i + 1:]:

                    distance = (
                        scenario.distances[
                            node_a,
                            node_b,
                        ]
                    )

                    if distance < minimum_distance:

                        self.model.addCons(
                            x[
                                dataset_id,
                                node_a,
                            ]
                            +
                            y[
                                dataset_id,
                                node_a,
                            ]
                            +
                            x[
                                dataset_id,
                                node_b,
                            ]
                            +
                            y[
                                dataset_id,
                                node_b,
                            ]
                            <= 1,
                            name=(
                                f"distance_"
                                f"{dataset_id}_"
                                f"{node_a}_"
                                f"{node_b}"
                            ),
                        )

    def add_failure_exposure_constraint(
        self,
        scenario,
        x,
        y,
    ):
        """
        Exposure(k)
        <=
        FailureBudget(k)
        """

        for dataset in scenario.datasets:

            dataset_id = (
                dataset.dataset.identifier
            )

            budget = (
                dataset.dataset
                .failure_exposure_budget
            )

            exposure = quicksum(

                scenario.failure_risk[node]

                *

                (
                    x[
                        dataset_id,
                        node,
                    ]
                    +
                    y[
                        dataset_id,
                        node,
                    ]
                )

                for node
                in scenario.storage_nodes
            )

            self.model.addCons(

                exposure
                <=
                budget,

                name=(
                    f"failure_budget_"
                    f"{dataset_id}"
                ),
            )

    def add_failed_link_constraint(
        self,
        scenario,
        x,
        y,
    ):
        """
        Nodos inaccesibles en el día actual.
        """

        for node in scenario.failed_nodes:

            for dataset in scenario.datasets:

                dataset_id = (
                    dataset.dataset.identifier
                )

                self.model.addCons(
                    x[
                        dataset_id,
                        node,
                    ]
                    == 0,
                    name=(
                        f"failed_x_"
                        f"{dataset_id}_"
                        f"{node}"
                    ),
                )

                self.model.addCons(
                    y[
                        dataset_id,
                        node,
                    ]
                    == 0,
                    name=(
                        f"failed_y_"
                        f"{dataset_id}_"
                        f"{node}"
                    ),
                )

    def build(
        self,
        scenario,
        x,
        y,
    ):

        self.add_single_placement_constraint(
            scenario,
            x,
        )

        self.add_storage_capacity_constraint(
            scenario,
            x,
            y,
        )

        self.add_receiver_compatibility_constraint(
            scenario,
            x,
            y,
        )

        self.add_replication_constraint(
            scenario,
            x,
            y,
        )

        self.add_replication_delay_constraint(
            scenario,
            y,
        )

        self.add_replica_separation_constraint(
            scenario,
            x,
            y,
        )

        self.add_minimum_replica_distance_constraint(
            scenario,
            x,
            y,
        )

        self.add_failure_exposure_constraint(
            scenario,
            x,
            y,
        )

        self.add_failed_link_constraint(
            scenario,
            x,
            y,
        )