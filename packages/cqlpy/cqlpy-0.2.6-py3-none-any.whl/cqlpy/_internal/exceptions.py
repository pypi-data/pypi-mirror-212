class CqlPyError(Exception):
    ...


class CqlParseError(CqlPyError, ValueError):
    ...


class ValueSetProviderError(CqlPyError):
    ...
