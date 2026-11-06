def build_distance_matrix(
    storage_nodes,
):

    distances = {}

    for node_i in storage_nodes:

        for node_j in storage_nodes:

            if node_i == node_j:

                distances[
                    node_i,
                    node_j,
                ] = 0.0

            else:

                distances[
                    node_i,
                    node_j,
                ] = 100.0

    return distances