import pyerr


def test_try_err():
    @pyerr.try_err
    def target(val_int):
        if val_int < 0:
            raise Exception("This is an exception.")
        else:
            return pyerr.ok(val_int)

    should_be_ok = target(1)
    assert pyerr.is_ok(should_be_ok) == True
    assert pyerr.unwrap(should_be_ok) == 1

    should_be_error = target(-1)
    assert pyerr.is_error(should_be_error) == True


def test_map_err():
    wrapped_result = pyerr.fmap(lambda x: x + 1, pyerr.ok(1))
    assert pyerr.unwrap(wrapped_result) == 2

    error = pyerr.fmap(lambda x: x + 1, pyerr.error("Error."))
    assert pyerr.is_error(error)

    flat_wrapped_result = pyerr.flat_map(lambda x: pyerr.ok(x+1), pyerr.ok(1))
    assert pyerr.unwrap(flat_wrapped_result) == 2

    flat_err = pyerr.flat_map(lambda x: pyerr.ok(x+1), pyerr.error("Error."))
    assert pyerr.is_error(flat_err)
