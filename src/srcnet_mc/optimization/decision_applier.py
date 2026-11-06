from srcnet_mc.optimization.solution import (
    OptimizationSolution,
)


class DecisionApplier:
    """
    Aplica una OptimizationSolution
    sobre un SRCNetWorld existente.
    """

    def apply(
        self,
        world,
        solution: OptimizationSolution,
    ):
        """
        Actualiza:

        - dataset.stored_at
        - storage_occupancy

        a partir de placements y réplicas.
        """

        if not solution.is_feasible:

            return

        self._apply_placements(
            world,
            solution,
        )

        self._apply_replicas(
            world,
            solution,
        )

    def _apply_placements(
        self,
        world,
        solution,
    ):
        """
        Placement principal.
        """

        for placement in solution.placements:

            dataset_id = (
                placement.dataset_id
            )

            destination = (
                placement.destination_node
            )

            if (
                dataset_id
                not in world.datasets
            ):
                continue

            instance = (
                world.datasets[
                    dataset_id
                ]
            )

            volume = (
                instance.dataset.volume_pb
            )

            #
            # Eliminamos ocupación anterior.
            #

            for node in list(
                instance.stored_at
            ):

                if (
                    node
                    in
                    world.storage_occupancy
                ):

                    world.storage_occupancy[
                        node
                    ] = max(
                        0.0,
                        world.storage_occupancy[
                            node
                        ]
                        - volume,
                    )

            #
            # Nuevo placement.
            #

            instance.stored_at = {
                destination
            }

            world.storage_occupancy[
                destination
            ] += volume

    def _apply_replicas(
        self,
        world,
        solution,
    ):
        """
        Réplicas adicionales.
        """

        for replica in solution.replicas:

            dataset_id = (
                replica.dataset_id
            )

            node = (
                replica.node
            )

            if (
                dataset_id
                not in world.datasets
            ):
                continue

            instance = (
                world.datasets[
                    dataset_id
                ]
            )

            if node in instance.stored_at:

                continue

            volume = (
                instance.dataset.volume_pb
            )

            instance.stored_at.add(
                node
            )

            world.storage_occupancy[
                node
            ] += volume