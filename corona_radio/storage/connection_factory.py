import sqlite3
import os
import logging

class DatabaseConnectionFactory:

    def __init__(self, dbfile='storage.db'):
        self._logger = logging.getLogger('DatabaseConnectionFactory')
        shouldInitialize = not os.path.exists(dbfile)
        self._conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._logger.info('Connected to the database')

        if shouldInitialize:
            self._logger.info('Database file does not exists, will intialize it.')
            self._logger.info('Executing the database intialization script')
            with open('corona_radio/storage/initialization.sql', 'r') as fd:
                self._conn.executescript(fd.read()).close()
            self._logger.info('Database initialized.')

    def getConnection(self):
        return self._conn