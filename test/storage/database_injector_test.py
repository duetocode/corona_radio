from corona_radio.storage.database_injector import DatabaseInjector
from .storage_test import MemoryBasedConnectionFactory
import pytest


@pytest.fixture()
def connectionFactory():
    return MemoryBasedConnectionFactory()

def test_inject(connectionFactory):

    class MockStorageService:
        def __init__(self):
            self._invoked = False
            self._verified = False

        def databaseOperation(self, cursor, conn, arg):
            self._invoked = True

            assert cursor is not None
            assert conn is not None

            self._verified = True

            return self._verified

    actualService =  MockStorageService()
    proxy = DatabaseInjector(actualService, connectionFactory)

    actual = proxy.databaseOperation(9876)

    assert actual == True
    assert actualService._invoked == True
    assert actualService._verified == True