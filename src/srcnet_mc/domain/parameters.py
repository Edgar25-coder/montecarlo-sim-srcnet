from dataclasses import dataclass

from srcnet_mc.domain.markov import LinkState


@dataclass(frozen=True)
class BetaMoments:
    mean: float
    variance: float


@dataclass(frozen=True)
class LogNormalMoments:
    mean: float
    cv: float


@dataclass(frozen=True)
class WeibullMoments:
    mean_lifetime_days: float
    shape: float


@dataclass(frozen=True)
class PoissonRate:
    rate: float


@dataclass(frozen=True)
class LinkStateParameters:
    utilization: BetaMoments
    latency: LogNormalMoments


@dataclass(frozen=True)
class LinkParameters:
    normal: LinkStateParameters
    congested: LinkStateParameters
    degraded: LinkStateParameters


@dataclass(frozen=True)
class DatasetParameters:
    arrivals: PoissonRate
    size_distribution: LogNormalMoments
    retention_distribution: WeibullMoments


@dataclass(frozen=True)
class SimulationParameters:
    link_parameters: LinkParameters
    dataset_parameters: DatasetParameters