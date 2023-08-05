# This file is placed in the Public Domain.
#
# pylint: disable=R,C0114,C0115,C0116


from .objects import Object


def __dir__():
    return (
            'Errors'
           )


class Errors(Object):

    errors = []

    @staticmethod
    def handle(ex) -> None:
        exc = ex.with_traceback(ex.__traceback__)
        Errors.errors.append(exc)
