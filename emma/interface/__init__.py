"""
interfaces are where the comunication to the internet happends

Interfaces communicate with L{modules<module>} through L{events}. modules 
will do the functionallity of the bot, using interfaces for communicate with
mailing lists, irc, ...

Interface inheritate from L{complement} from where you can
L{log<emma.complement.Complement.log>}, L{use locks<emma.complement.use_lock>},
... Everything in an interface happens in parallel on several threads, so for
class variables L{locks<emma.complement.use_lock>} should be use.

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

from emma.complement import Complement

class Interface(Complement):
    pass
