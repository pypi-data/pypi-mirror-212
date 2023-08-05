# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0116


from ..runtime import Cfg


def ver(event):
    event.reply(f"{Cfg.name.upper()} {Cfg.version}")
