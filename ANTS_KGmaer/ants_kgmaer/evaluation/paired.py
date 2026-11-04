"""Paired dependency-block bootstrap; never treats millions of log rows as IID."""

import random

from .metrics import from_matrix


def sum_matrices(matrices):
    result = [[0.0] * 3 for _ in range(2)]
    for matrix in matrices:
        for row in range(2):
            for column in range(3):
                result[row][column] += matrix[row][column]
    return result


def quantile(values, fraction):
    values = sorted(values)
    index = (len(values) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] + (values[upper] - values[lower]) * (index - lower)


def paired_bootstrap(blocks, repetitions=2000, seed=20261026):
    """blocks maps group ID to two confusion matrices from the same target set."""
    if type(repetitions) is not int or repetitions < 1 or not blocks:
        raise ValueError("Nonempty paired blocks and positive repetitions required")
    ordered = [blocks[key] for key in sorted(blocks)]

    def difference(sample):
        left = from_matrix(sum_matrices(item[0] for item in sample))["BA_all"]
        right = from_matrix(sum_matrices(item[1] for item in sample))["BA_all"]
        return right - left if left is not None and right is not None else None

    randomizer = random.Random(seed)
    differences = []
    for _ in range(repetitions):
        delta = difference([randomizer.choice(ordered) for _ in ordered])
        if delta is not None:
            differences.append(delta)
    return {"delta_BA_all_right_minus_left": difference(ordered), "blocks": len(ordered),
            "repetitions": repetitions, "valid_repetitions": len(differences), "seed": seed,
            "percentile_95_interval": [quantile(differences, 0.025), quantile(differences, 0.975)] if differences else None,
            "limitations": "Few dependency blocks imply unstable intervals. Exact-overlap groups are minimum known dependencies."}
