# This file is placed in the Public Domain
#
# pylama: ignore=E402,W0611,W0401,C901


"""object programming runtime


OPR is runtime kit that uses object programming for it's implementation.
Object programming uses classes with the methods factored out into
functions, to get a clean namespace to load json into and not overwrite
any methods. A clean namespace way of programming, so to speak.

OPR provides object persistence, an event handler and some basic code to
load modules that can provide additional commands.

OPR has some functionality, mostly feeding RSS feeds into a irc
channel. It can do some logging of txt and take note of things todo.

OPR is placed in the Public Domain

"""


from .clients import Client
from .default import Default
from .objects import *
from .objfunc import *
from .command import Commands
from .logging import Logging
from .persist import *
from .runtime import *


def __dir__():
    return (
            'Cfg',
            'Default',
            'Object',
            'Persist',
            'copy',
            'dump',
            'dumprec',
            'edit',
            'ident',
            'items',
            'keys',
            'kind',
            'launch',
            'last',
            'load',
            'parse_cli',
            'prt',
            'read',
            'readrec',
            'search',
            'threaded',
            'update',
            'values',
            'waiter',
            'write',
            'writerec'
           )
