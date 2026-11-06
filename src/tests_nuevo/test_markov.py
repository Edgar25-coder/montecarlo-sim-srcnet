import numpy as np

from srcnet_mc.domain.markov import (
    LinkState,
    MarkovChain,
)


def test_transition_matrix_rows_sum_to_one():

    P = np.array([
        [0.90, 0.10, 0.00, 0.00],
        [0.10, 0.80, 0.10, 0.00],
        [0.00, 0.10, 0.80, 0.10],
        [0.20, 0.10, 0.00, 0.70],
    ])

    rng = np.random.default_rng(1234)

    MarkovChain(
        transition_matrix=P,
        initial_state=LinkState.NORMAL,
        rng=rng,
    )