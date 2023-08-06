import typing


class PyCsvXlsException(Exception):
    def __init__(
        self,
        msg: typing.Optional[str] = None,
        exc: typing.Optional[Exception] = None,
        **kwargs,
    ):
        self.msg = msg
        self.exc = exc
        self.__dict__.update(kwargs=kwargs)
