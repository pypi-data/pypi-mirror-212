import contextlib


@contextlib.contextmanager
def key_error_silence():
    """
    Context manager that silences key errors exceptions.
    """
    try:
        yield
    except KeyError:
        pass


def guard_against_none_or_empty_str(value: str, name: str):
    """
    Guard against None or empty string.

    Parameters:
    -----------
    value: str
        The value to check.
    name: str
        The name of the value.
    """

    if value is None or not isinstance(value, str) or value == "":
        raise ValueError(f"{name} cannot be None or empty")


def guard_against_none(value, name: str):
    """
    Guard against None.

    Parameters:
    -----------
    value: str
        The value to check.
    name: str
        The name of the value.
    """

    if value is None:
        raise ValueError(f"{name} cannot be None")
