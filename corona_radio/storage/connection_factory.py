import sqlite3
import os
import logging
from pathlib import Path

class DatabaseConnectionFactory:

    def __init__(self, dbfile='storage.db'):
        self._logger = logging.getLogger('DatabaseConnectionFactory')
        dbfile = Path(dbfile)
        shouldInitialize = not dbfile.exists()
        self._conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._logger.info('Connected to the database')

        if shouldInitialize:
            self._logger.info('Database file does not exists, will intialize it.')
            self._logger.info('Executing the database intialization script')
            scriptPath = Path(Path(__file__).parent, 'initialization.sql')
            with open(scriptPath.absolute(), 'r') as fd:
                self._conn.executescript(fd.read()).close()
            self._logger.info('Database initialized.')

    def getConnection(self):
        return self._conn

    def shutdown(self):
        if self._conn is not None:
            self._conn.close()