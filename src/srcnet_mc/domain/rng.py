from numpy.random import Generator
from numpy.random import PCG64
from numpy.random import SeedSequence


class RNGManager:

    def __init__(self, seed: int):

        self._master = SeedSequence(seed)

    def replication_rng(
        self,
        replication_id: int,
    ) -> Generator:

        children = self._master.spawn(
            replication_id + 1
        )

        return Generator(
            PCG64(children[replication_id])
        )