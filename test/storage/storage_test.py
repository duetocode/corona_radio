from corona_radio.storage.storage import StorageService
import sqlite3

import pytest


class MemoryBasedConnectionFactory:

    def __init__(self):
        self._conn = sqlite3.connect(':memory:')
        with open('corona_radio/storage/initialization.sql', 'r') as fd:
            self._conn.executescript(fd.read()).close()

    def getConnection(self):
        return self._conn

@pytest.fixture()
def connectionFactory():
    return MemoryBasedConnectionFactory()

def test_add_subscript(connectionFactory):
    storageService = StorageService(databaseConnectionFactory=connectionFactory)

    assert storageService.subscriptionStorage is not None
    assert storageService.podcastStorage is not None
    assert storageService.downloadTaskStorage is not None

    '''
    subscription = SimpleNamespace(
        title = 'Title',
        link = 'https://example.org',
        createdAt = datetime.now(),
        updatedAt = datetime.now())

    actual = storage.saveSubscription(subscription)

    assert hasattr(actual, 'id')
    assert actual.id == 1

    cursor = connectionFactory.getConnection().execute('SELECT * FROM subscription WHERE id = ?', [actual.id])
    row = cursor.fetchone()
    assert row is not None
    '''