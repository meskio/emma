"""
modules are where the actual functionality of the bot happens

If you want to add functionality to emma you should hack here, creating a
module. Modules communicate through L{events} with 
L{interfaces<emma.interface>} for access to mailing lists, irc, ...

Module inheritate from L{complement} from where you can
L{log<emma.complement.Complement.log>}, L{use locks<emma.complement.use_lock>},
... Everything in a module happens in parallel on several threads, so for class
variables L{locks<emma.complement.use_lock>} should be use.

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@author: Ruben Pollan
@organization: hackmeeting U{http://sindominio.net/hackmeeting}
@contact: meskio@sindominio.net
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

from emma.complement import Complement


class Module(Complement):
    pass
