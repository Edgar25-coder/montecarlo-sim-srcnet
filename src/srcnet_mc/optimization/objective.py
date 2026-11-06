from dataclasses import dataclass

from pyscipopt import quicksum


@dataclass(frozen=True)
class OptimizationWeights:

    storage: float = 1.0

    replication: float = 0.5

    exposure: float = 5.0

    latency: float = 2.0

    capacity: float = 3.0


class ObjectiveBuilder:

    def __init__(
        self,
        model,
        weights=None,
    ):

        self.model = model

        self.weights = (
            weights
            if weights is not None
            else OptimizationWeights()
        )

    def set_objective(
        self,
        scenario,
        x,
        y,
    ):

        #
        # STORAGE COST
        #
        storage_cost = quicksum(

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

            for node
            in scenario.storage_nodes
        )

        #
        # REPLICATION COST
        #
        replica_cost = quicksum(

            y[
                dataset.dataset.identifier,
                node,
            ]

            for dataset
            in scenario.datasets

            for node
            in scenario.storage_nodes
        )

        #
        # FAILURE EXPOSURE COST
        #
        exposure_cost = quicksum(

            scenario.failure_risk[node]

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

            for node
            in scenario.storage_nodes
        )

        #
        # LATENCY COST
        #
        #
        latency_cost = quicksum(

            scenario.latency_costs[node]

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

            for node
            in scenario.storage_nodes
        )

        capacity_cost = quicksum(

            scenario.capacity_costs[node]

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

            for node
            in scenario.storage_nodes
        )

        dataset_count = len(scenario.datasets)
        node_count = len(scenario.storage_nodes)

        storage_scale = sum(
            dataset.dataset.volume_pb
            * (1 + node_count)
            for dataset in scenario.datasets
        )
        replication_scale = dataset_count * node_count

        exposure_risks = tuple(
            scenario.failure_risk[node]
            for node in scenario.storage_nodes
        )
        exposure_scale = dataset_count * (
            max(exposure_risks, default=0.0)
            + sum(exposure_risks)
        )

        latency_costs = tuple(
            scenario.latency_costs[node]
            for node in scenario.storage_nodes
        )
        latency_scale = dataset_count * (
            max(latency_costs, default=0.0)
            + sum(latency_costs)
        )

        capacity_costs = tuple(
            scenario.capacity_costs[node]
            for node in scenario.storage_nodes
        )
        capacity_scale = dataset_count * (
            max(capacity_costs, default=0.0)
            + sum(capacity_costs)
        )

        normalized_storage_cost = storage_cost / (
            storage_scale or 1.0
        )
        normalized_replica_cost = replica_cost / (
            replication_scale or 1.0
        )
        normalized_exposure_cost = exposure_cost / (
            exposure_scale or 1.0
        )
        normalized_latency_cost = latency_cost / (
            latency_scale or 1.0
        )
        normalized_capacity_cost = capacity_cost / (
            capacity_scale or 1.0
        )

        objective = (

            self.weights.storage
            *
            normalized_storage_cost

            +

            self.weights.replication
            *
            normalized_replica_cost

            +

            self.weights.exposure
            *
            normalized_exposure_cost

            +

            self.weights.latency
            *
            normalized_latency_cost

            +

            self.weights.capacity
            *
            normalized_capacity_cost
        )

        self.model.setObjective(
            objective,
            sense="minimize",
        )