from enum import IntEnum

import numpy as np


class LinkState(IntEnum):

    NORMAL = 0

    CONGESTED = 1

    DEGRADED = 2

    FAILED = 3


class MarkovChain:

    def __init__(
        self,
        transition_matrix,
        initial_state,
        rng,
    ):

        self.transition_matrix = np.asarray(
            transition_matrix,
            dtype=float,
        )

        self.state = initial_state

        self.rng = rng

        self._validate()

    def _validate(self):

        for row in self.transition_matrix:

            if not np.isclose(
                np.sum(row),
                1.0,
            ):
                raise ValueError(
                    "Transition matrix row must sum to 1."
                )

    def step(self):

        probs = self.transition_matrix[self.state]

        self.state = LinkState(
            self.rng.choice(
                len(probs),
                p=probs,
            )
        )

        return self.state