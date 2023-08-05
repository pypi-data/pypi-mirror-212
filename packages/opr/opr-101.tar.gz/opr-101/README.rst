NAME


::

    opr - object programming runtime


SYNOPSIS


::

    opr [cmd] [key=value] [key==value]
    opr [-a|-c|-d|-t|-v]


INSTALL


::

    pip3 install opr --upgrade --force-reinstall


DESCRIPTION


::

    OPR is runtime kit that uses object programming for it's implementation.
    Object programming uses classes with the methods factored out into
    functions, to get a clean namespace to load json into and not overwrite
    any methods. A clean namespace way of programming, so to speak.

    OPR provides object persistence, an event handler and some basic code to
    load modules that can provide additional commands.

    OPR has some functionality, mostly feeding RSS feeds into a irc
    channel. It can do some logging of txt and take note of things todo.


COMMANDS


::

    here is a short description of the commands:

    cmd - shows all commands
    cfg - shows/edit the irc configuration
    dlt - removes a user from bot
    dpl - sets display items for a rss feed
    ftc - runs a rss feed fetching batch
    flt - list of bot registered to the bus
    log - log some text
    met - add  users with their irc userhost
    mre - displays cached output per channel
    nck - changes nick on irc
    nme - set the name of a feed
    pwd - nickserv name/password to sasl pwd
    rem - removes a rss feed
    rss - add a feed to fetch
    thr - show the running threads
    tdo - add a todo item


USAGE


::

    as a default opr does not react

    $ opr
    $

    list of commands 

    $ opr cmd
    cmd,err,flt,mod,sts,thr,upt,ver

    list of modules

    $ opr mod
    cmd,err,flt,fnd,irc,log,mod,rss,sts,tdo,thr,upt,ver

    start a shell

    $ opr -c
    >

    run shell with irc and rss modules loaded

    $ opr -c mod=irc,rss
    >

    (*) default is #opr on localhost

    put into dameon mode

    $ opr mod=irc,rss -d
    $

    options are

    -a loads all modules
    -c start console
    -d start as daemon
    -v enables verbose
    -t enables threading


CONFIGURATION


::

    configuration is done by calling the cfg command of the bot.

    irc

    opr cfg server=<server>
    opr cfg channel=<channel>
    opr cfg nick=<nick>
    opr cfg port=<portnr>

    (*) default is #opr on localhost

    sasl

    opr pwd <nsnick> <nspass>
    opr cfg password=<outputfrompwd>

    users

    opr cfg users=True
    opr met <userhost>

    rss

    opr rss <url>
    opr rem <url>
    opr dpl title,summary,link
    opr nme <url> <name>
    opr ftc

    log

    opr log <txt>
    opr log

    todo

    opr tdo <txt>
    opr dne <txt>


AUTHOR


::

    Bart Thate - <bthate@dds.nl>

COPYRIGHT


::

    OPR is placed in the Public Domain.
