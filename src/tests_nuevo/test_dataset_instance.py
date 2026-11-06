from srcnet_mc.domain.model import Dataset
from srcnet_mc.domain.dataset_instance import DatasetInstance


def test_dataset_grows_older():

    dataset = Dataset(
        identifier="D1",
        source_sdp="SDP1",
        volume_pb=1.0,
        compatible_receivers=frozenset({"SRC1"}),
    )

    instance = DatasetInstance(
        dataset=dataset,
        age_days=0,
        retention_days=10,
        stored_at=set(),
    )

    instance.grow_old()

    assert instance.age_days == 1


def test_dataset_not_expired():

    dataset = Dataset(
        identifier="D1",
        source_sdp="SDP1",
        volume_pb=1.0,
        compatible_receivers=frozenset({"SRC1"}),
    )

    instance = DatasetInstance(
        dataset=dataset,
        age_days=5,
        retention_days=10,
        stored_at=set(),
    )

    assert instance.expired is False


def test_dataset_expired():

    dataset = Dataset(
        identifier="D1",
        source_sdp="SDP1",
        volume_pb=1.0,
        compatible_receivers=frozenset({"SRC1"}),
    )

    instance = DatasetInstance(
        dataset=dataset,
        age_days=10,
        retention_days=10,
        stored_at=set(),
    )

    assert instance.expired is True