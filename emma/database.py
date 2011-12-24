"""
DataBase interface

Using mongoDB

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

import pymongo
import logging

class DB:
    """
    Database class

    It is a singleton class, so any instantion of it will get the global
    database.
    """
    __ = {}
    def __init__(self):
        pass

    def connect(self, name):
        """
        Connect to a mongoDB database

        That method must be call before any use of the database
        @type name: string
        @param name: database name
        """
        logging.info("[core] connect to database")
        self.__['conn'] = pymongo.Connection()
        self.__['db'] = self.__['conn'][name]

    def collection(self, coll):
        """
        Get a database collection

        @type coll: string
        @param coll: coll name
        @returns: mongoDb collection
        """
        return self.__['db'][coll]

    def core(self):
        """
        Get the core collection

        The collection use by the core of emma
        @returns: mongoDb collection
        """
        return self.collection('core')
