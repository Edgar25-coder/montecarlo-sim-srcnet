from dataclasses import dataclass

from srcnet_mc.domain.model import Dataset


@dataclass
class DatasetInstance:

    dataset: Dataset

    age_days: int

    retention_days: float

    stored_at: set[str]

    direct_reception: bool = False

    def grow_old(self):

        self.age_days += 1

    @property
    def expired(self):

        return (
            self.age_days
            >= self.retention_days
        )