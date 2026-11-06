import numpy as np

from srcnet_mc.domain.distributions import (
    sample_poisson,
)


def test_poisson_mean():

    rng = np.random.default_rng(1234)

    rate = 5.0

    samples = np.array(
        [
            sample_poisson(
                rng,
                rate,
            )
            for _ in range(100_000)
        ]
    )

    empirical_mean = samples.mean()

    assert abs(
        empirical_mean - rate
    ) < 0.1