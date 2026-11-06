import numpy as np

from srcnet_mc.domain.distributions import (
    sample_weibull,
)


def test_weibull_mean():

    rng = np.random.default_rng(1234)

    mean_target = 365.0

    shape = 1.5

    samples = np.array(
        [
            sample_weibull(
                rng,
                mean_target,
                shape,
            )
            for _ in range(100_000)
        ]
    )

    empirical_mean = samples.mean()

    assert abs(
        empirical_mean - mean_target
    ) < 5.0