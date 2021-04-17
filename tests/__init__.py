import unittest.mock as mock


def decorated_mocks(func):
    """Collapse decorated mocks into a single dict"""

    def _m(*args, **kwargs):
        new_args = []
        mocks = {}
        for arg in args:
            if isinstance(arg, mock.Mock):
                mocks[arg._mock_name] = arg
            else:
                new_args.append(arg)
        new_args.append(mocks)
        return func(*new_args, **kwargs)

    return _m
