# This file is placed in the Public Domain
# pylama: ignore=E402

"""there are no paths


NOPATHS is a python3 bot, it connects to irc and provides a select sets of
commands. It doesn't use os.popen, does no external imports, can be run in
client or daemon mode and has batteries included.

MOPATHS is intended to be programmable, it provides object persistence, an
event handler and some basic code to load modules that can provide
additional functionality.

NOPATHS uses object programming, programming where the methods are
seperated out into functions that use the object as the first argument of
that funcion. This gives base class definitions a clean namespace to
inherit from and to load json data into the object's __dict__. A clean
namespace prevents a json loaded attribute to overwrite any methods.

NOPATHS stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON
dumps and paths carry the type in the path name what makes reconstruction
from filename easier then reading type from the object.

NOPATHS has some functionality builtin, it can take notes, add todo,
maintain a shopping list and display rss feeds.


NOPATHS has its roots in "no other options available" e.g. no choices left.

"""
