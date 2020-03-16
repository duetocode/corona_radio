from corona_radio.storage.connection_factory import DatabaseConnectionFactory
import os


def test_database_initialization(tmpdir):
    targetFile = os.path.join(tmpdir, 'database.db')
    factory = DatabaseConnectionFactory(dbfile=targetFile)

    assert os.path.exists(targetFile)