from srcnet_mc.domain.model import Dataset

from srcnet_mc.domain.dataset_instance import (
    DatasetInstance,
)


def test_dataset_expires_after_retention():

    dataset = Dataset(
        identifier="D1",
        source_sdp="SDP1",
        volume_pb=1.0,
        compatible_receivers=frozenset({"T0"}),
    )

    instance = DatasetInstance(
        dataset=dataset,
        age_days=9,
        retention_days=10,
        stored_at={"T0"},
    )

    instance.grow_old()

    assert instance.expired