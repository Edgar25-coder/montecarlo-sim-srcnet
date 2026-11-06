import numpy as np

from srcnet_mc.domain.distributions import (
    sample_poisson,
)


def test_dataset_arrivals_mean():

    rng = np.random.default_rng(1234)

    rate = 5.0

    arrivals = np.array(
        [
            sample_poisson(
                rng,
                rate,
            )
            for _ in range(100_000)
        ]
    )

    assert abs(arrivals.mean() - rate) < 0.1