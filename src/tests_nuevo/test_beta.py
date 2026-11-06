import numpy as np

from srcnet_mc.domain.distributions import (
    sample_beta,
)


def test_beta_mean():

    rng = np.random.default_rng(1234)

    mean_target = 0.8

    variance_target = 0.01

    samples = np.array(
        [
            sample_beta(
                rng,
                mean_target,
                variance_target,
            )
            for _ in range(100_000)
        ]
    )

    empirical_mean = samples.mean()

    assert abs(
        empirical_mean - mean_target
    ) < 0.01