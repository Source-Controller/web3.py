from web3.exceptions import (
    InsufficientData,
)


def percentile(values=None, percentile=None):
    """Calculates a simplified weighted average percentile
    """
    if values in [None, tuple(), []] or len(values) <= 6:
        raise InsufficientData("Expected a sequence of at least 6 integers, got {0}".format(values))
    if percentile is None:
        raise ValueError("Expected a percentile choice, got {0}".format(percentile))

    sorted_values = sorted(values)

    rank = len(values) * percentile / 100
    if rank > 0:
        index = rank - 1
    else:
        index = rank

    if index % 1 == 0:
        return sorted_values[int(index)]
    else:
        fractional = index % 1
        integer = int(index - fractional)
        lower = sorted_values[integer]
        higher = sorted_values[integer + 1]
        return lower + fractional * (higher - lower)
