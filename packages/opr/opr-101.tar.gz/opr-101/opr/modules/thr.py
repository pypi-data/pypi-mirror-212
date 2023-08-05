# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0116,E1101


import threading
import time


from ..objects import Object, update
from ..runtime import STARTTIME
from ..utility import elapsed


def thr(event):
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith('<_'):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, 'sleep', None):
            uptime = obj.sleep - int(time.time() - obj.state.latest)
        elif getattr(obj, 'starttime', None):
            uptime = int(time.time() - obj.starttime)
        else:
            uptime = int(time.time() - STARTTIME)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        lap = elapsed(uptime)
        res.append(f'{txt}/{lap}')
    if res:
        event.reply(' '.join(res))
    else:
        event.reply('no threads')
