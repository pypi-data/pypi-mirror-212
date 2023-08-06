"""
    Module for providing functions for wrapper value that can contain success value or an error.
"""

def ok(val):
    """Creates wrapped success value."""
    return ("ok", val)


def error(val):
    """Creates wrapped error."""
    return ("error", val)


def is_ok(err) -> bool:
    return err[0] == "ok"


def is_error(err) -> bool:
    return err[0] == "error"


def unwrap(err):
    """Unwraps value regardless if it's an error or not."""
    return err[1]


def attempt_unwrap(func_on_error, err):
    """Attempts to unwrap value. If wrapped value is an error than provided function is run."""
    if is_ok(err):
        return unwrap(err)
    else:
        return func_on_error()


def fmap(func, err):
    """Apply function to wrapped value if it's not an error. And returns wrapped value."""
    if is_ok(err):
        return ok(func(unwrap(err)))
    else:
        return err


def flat_map(func, err):
    """Flat map function over wrapped value if it's not an error. Expects given function to return also wrapped value."""
    if is_ok(err):
        return func(unwrap(err))
    else:
        return err


def try_err(func):
    """Decorator for catching exceptions and converting them to error."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return error(str(e))
    return wrapper
