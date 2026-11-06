from srcnet_mc.domain.rng import RNGManager


def test_seed_reproducibility():

    manager1 = RNGManager(1234)
    manager2 = RNGManager(1234)

    rng1 = manager1.replication_rng(0)
    rng2 = manager2.replication_rng(0)

    values1 = rng1.integers(0, 100, 10)
    values2 = rng2.integers(0, 100, 10)

    assert all(values1 == values2)