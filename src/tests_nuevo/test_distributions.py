import numpy as np

from srcnet_mc.domain.distributions import (
    sample_lognormal,
)


def test_lognormal_mean():

    rng = np.random.default_rng(1234)

    mean_target = 100
    cv = 0.5

    samples = [
        sample_lognormal(
            rng,
            mean_target,
            cv,
        )
        for _ in range(100000)
    ]

    empirical_mean = np.mean(samples)

    assert abs(empirical_mean - mean_target) < 2