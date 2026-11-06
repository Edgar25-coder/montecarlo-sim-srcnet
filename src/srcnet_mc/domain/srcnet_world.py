from srcnet_mc.domain.model import Dataset

from srcnet_mc.domain.dataset_instance import (
    DatasetInstance,
)

from srcnet_mc.domain.world_state import (
    ArcState,
    WorldState,
)

from srcnet_mc.domain.markov import (
    LinkState,
)

from srcnet_mc.domain.distributions import (
    sample_beta,
    sample_lognormal,
    sample_poisson,
    sample_weibull,
)


class SRCNetWorld:

    def __init__(
        self,
        topology,
        parameters,
        rng,
        chains,
    ):

        self.topology = topology

        self.parameters = parameters

        self.rng = rng

        self.chains = chains

        self.current_day = 0

        self.next_dataset_id = 1

        self.datasets = {}

        self.storage_occupancy = {
            node.identifier: 0.0
            for node in topology.nodes
        }

    def _state_parameters(self, state):

        lp = self.parameters.link_parameters

        match state:

            case LinkState.NORMAL:
                return lp.normal

            case LinkState.CONGESTED:
                return lp.congested

            case LinkState.DEGRADED:
                return lp.degraded

            case LinkState.FAILED:
                return None

        raise ValueError(
            f"Unsupported state {state}"
        )

    def _age_datasets(self):

        for dataset in self.datasets.values():

            dataset.grow_old()

    def _remove_expired(self):

        expired_ids = []

        released_volume = 0.0

        for dataset_id, dataset in self.datasets.items():

            if dataset.expired:

                expired_ids.append(dataset_id)

                released_volume += (
                    dataset.dataset.volume_pb
                )

        for dataset_id in expired_ids:

            del self.datasets[dataset_id]

        self.storage_occupancy["T0"] = max(
            0.0,
            self.storage_occupancy["T0"]
            - released_volume,
        )

        return len(expired_ids)

    def _generate_new_datasets(self):

        params = (
            self.parameters.dataset_parameters
        )

        arrivals = sample_poisson(
            self.rng,
            params.arrivals.rate,
        )

        total_volume = 0.0

        for _ in range(arrivals):

            volume = sample_lognormal(
                self.rng,
                params.size_distribution.mean,
                params.size_distribution.cv,
            )

            retention = sample_weibull(
                self.rng,
                params.retention_distribution.mean_lifetime_days,
                params.retention_distribution.shape,
            )

            dataset = Dataset(
                identifier=f"D{self.next_dataset_id}",
                source_sdp="SDP1",
                volume_pb=volume,
                compatible_receivers=frozenset(
                    {
                        "T0",
                        "SRC1",
                        "SRC2",
                        "SRC3",
                    }
                ),
            )

            instance = DatasetInstance(
                dataset=dataset,
                age_days=0,
                retention_days=retention,
                stored_at={"T0"},
            )

            self.datasets[
                dataset.identifier
            ] = instance

            self.next_dataset_id += 1

            total_volume += volume

        self.storage_occupancy["T0"] += (
            total_volume
        )

        return arrivals

    def _update_network(self):

        arc_states = {}

        for arc in self.topology.arcs:

            key = (arc.tail, arc.head)

            chain = self.chains[key]

            state = chain.step()

            if state == LinkState.FAILED:

                arc_states[key] = ArcState(
                    state=state,
                    effective_capacity_pb_per_day=0.0,
                    latency_ms=float("inf"),
                )

                continue

            params = self._state_parameters(state)

            utilisation = sample_beta(
                self.rng,
                params.utilization.mean,
                params.utilization.variance,
            )

            effective_capacity = (
                arc.capacity_pb_per_day
                * utilisation
            )

            latency = sample_lognormal(
                self.rng,
                params.latency.mean,
                params.latency.cv,
            )

            arc_states[key] = ArcState(
                state=state,
                effective_capacity_pb_per_day=effective_capacity,
                latency_ms=latency,
            )

        return arc_states

    def step(self):

        self.current_day += 1

        self._age_datasets()

        expired = self._remove_expired()

        arrivals = self._generate_new_datasets()

        arc_states = self._update_network()

        return WorldState(
            day=self.current_day,
            arc_states=arc_states,
            storage_occupancy_pb=self.storage_occupancy.copy(),
            datasets=self.datasets.copy(),
            new_arrivals=arrivals,
            expired_datasets=expired,
        )