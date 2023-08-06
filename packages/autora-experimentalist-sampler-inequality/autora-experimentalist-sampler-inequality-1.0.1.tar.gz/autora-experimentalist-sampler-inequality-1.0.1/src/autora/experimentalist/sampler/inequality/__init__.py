from typing import Iterable, Literal

import numpy as np
from sklearn.metrics import DistanceMetric

from autora.utils.deprecation import deprecated_alias

AllowedMetrics = Literal[
    "euclidean",
    "manhattan",
    "chebyshev",
    "minkowski",
    "wminkowski",
    "seuclidean",
    "mahalanobis",
    "haversine",
    "hamming",
    "canberra",
    "braycurtis",
    "matching",
    "jaccard",
    "dice",
    "kulsinski",
    "rogerstanimoto",
    "russellrao",
    "sokalmichener",
    "sokalsneath",
    "yule",
]


def summed_inequality_sample(
    condition_pool: np.ndarray,
    reference_conditions: np.ndarray,
    n: int = 1,
    equality_distance: float = 0,
    metric: str = "euclidean",
) -> np.ndarray:
    """
    This inequality sampler chooses from the pool of IV conditions according to their
    inequality with respect to a reference pool reference_conditions. Two IVs are considered equal if their
    distance is less then the equality_distance. The IVs chosen first are feed back into reference_conditions
    and are included in the summed equality calculation.

    Args:
        condition_pool: pool of IV conditions to evaluate inequality
        reference_conditions: reference pool of IV conditions
        n: number of samples to select
        equality_distance: the distance to decide if two data points are equal.
        metric: inequality measure. Options: 'euclidean', 'manhattan', 'chebyshev',
            'minkowski', 'wminkowski', 'seuclidean', 'mahalanobis', 'haversine',
            'hamming', 'canberra', 'braycurtis', 'matching', 'jaccard', 'dice',
            'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener',
            'sokalsneath', 'yule'. See `sklearn.metrics.DistanceMetric` for more details.

    Returns:
        Sampled pool

    Examples:
        The value 1 is not in the reference. Therefore it is choosen.
        >>> summed_inequality_sampler([1, 2, 3], [2, 3, 4])
        array([[1]])

        The equality distance is set to 0.4. 1 and 1.3 are considered equal, so are 3 and 3.1.
        Therefore 2 is choosen.
        >>> summed_inequality_sampler([1, 2, 3], [1.3, 2.7, 3.1], 1, .4)
        array([[2]])

        The value 3 appears least often in the reference.
        >>> summed_inequality_sampler([1, 2, 3], [1, 1, 1, 2, 2, 2, 3, 3])
        array([[3]])

        The samplers "fills up" the reference array so the values are contributed evenly
        >>> summed_inequality_sampler([1, 1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 2, 2, 2, 2, 3, 3, 3], 3)
        array([[1],
               [3],
               [1]])

        The sampler samples without replacemnt!
        >>> summed_inequality_sampler([1, 2, 3], [1, 1, 1], 3)
        array([[3],
               [2],
               [1]])

    """

    if isinstance(condition_pool, Iterable):
        condition_pool = np.array(list(condition_pool))

    if isinstance(reference_conditions, Iterable):
        reference_conditions = np.array(list(reference_conditions))

    if condition_pool.ndim == 1:
        condition_pool = condition_pool.reshape(-1, 1)

    if reference_conditions.ndim == 1:
        reference_conditions = reference_conditions.reshape(-1, 1)

    if condition_pool.shape[1] != reference_conditions.shape[1]:
        raise ValueError(
            f"condition_pool and reference_conditions must have the same number of columns.\n"
            f"condition_pool has {condition_pool.shape[1]} columns, while reference_conditions has {reference_conditions.shape[1]} columns."
        )

    if condition_pool.shape[0] < n:
        raise ValueError(
            f"condition_pool must have at least {n} rows matching the number of requested samples."
        )

    dist = DistanceMetric.get_metric(metric)

    # create a list to store the n condition_pool values with the highest inequality scores
    condition_pool_res = []
    # choose the canditate with the highest inequality score n-times
    for _ in range(n):
        summed_equalities = []
        # loop over all IV values
        for row in condition_pool:

            # calculate the distances between the current row in matrix1
            # and all other rows in matrix2
            summed_equality = 0
            for reference_conditions_row in reference_conditions:
                distance = dist.pairwise([row, reference_conditions_row])[0, 1]
                summed_equality += distance > equality_distance

            # store the summed distance for the current row
            summed_equalities.append(summed_equality)

        # sort the rows in matrix1 by their summed distances
        condition_pool = condition_pool[np.argsort(summed_equalities)[::-1]]
        # append the first value of the sorted list to the result
        condition_pool_res.append(condition_pool[0])
        # add the chosen value to reference_conditions
        reference_conditions = np.append(reference_conditions, [condition_pool[0]], axis=0)
        # remove the chosen value from condition_pool
        condition_pool = condition_pool[1:]

    return np.array(condition_pool_res[:n])

summed_inequality_sampler = deprecated_alias(summed_inequality_sample, "summed_inequality_sampler")
