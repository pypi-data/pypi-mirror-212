"""Numerical utilities."""


def is_power_of_two(number: int) -> bool:
    """Check if a number is a power of two.

    Args:
        number: The candidate

    Returns:
        Whether or not it is a power of two
    """
    if not isinstance(number, int):
        return False
    return (number & (number - 1) == 0) and number != 0
