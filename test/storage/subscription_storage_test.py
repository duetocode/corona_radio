import pytest
from types import SimpleNamespace
from corona_radio.storage.connection_factory import DatabaseConnectionFactory
from corona_radio.storage.subscription import SubscriptionStorage
from datetime import datetime

@pytest.fixture
def databaseConnection():
    factory = None 
    try:
        factory = DatabaseConnectionFactory(dbfile=':memory:')
        yield factory.getConnection()
    finally:
        if factory is not None:
            factory.shutdown()

@pytest.fixture
def cursor(databaseConnection):
    cursor = None
    try:
        cursor = databaseConnection.cursor()
        yield cursor
    finally:
        if cursor is not None:
            cursor.close()

def test_finalAll(databaseConnection, cursor):
    storage = SubscriptionStorage()

    timestamp = datetime.utcnow()
    cursor.execute('''INSERT INTO subscription
                        (`title`, `link`, `latest_content`, `created_at`, `updated_at`)
                        values (?, ?, ?, ?, ?)''', ['eltit', 'knil', None, timestamp, timestamp])
    databaseConnection.commit()

    actual = storage.findAll(cursor, databaseConnection)
    assert actual is not None
    assert len(actual) == 1
    
    subscription = actual[0]
    assert subscription.title == 'eltit'
    assert subscription.link == 'knil'
    assert subscription.latestContent is None
    assert subscription.createdAt == timestamp
    assert subscription.updatedAt == timestamp

def test_insert(databaseConnection, cursor):
    storage = SubscriptionStorage()

    timestamp = datetime.utcnow()
    entity = SimpleNamespace(
        title = 'Title',
        link = 'Link',
        latestContent = 'ABCDEFG',
        createdAt = timestamp,
        updatedAt = timestamp)

    actual = storage.save(cursor, databaseConnection, entity)

    assert hasattr(actual, 'id') and actual.id is not None
    assert actual.title == 'Title'
    assert actual.link == 'Link'
    assert actual.latestContent == 'ABCDEFG'
    assert actual.createdAt is not None and type(actual.createdAt) is datetime
    assert timestamp == actual.createdAt
    assert actual.updatedAt is not None

    cursor = databaseConnection.execute('select id, title, latest_content, created_at, updated_at '
                                            'from subscription '
                                            'where id = ? '
                                                'and title = ? '
                                                'and link = ?',[actual.id, 'Title', 'Link'])

    record = cursor.fetchone()
    assert record is not None
    assert record[2] == 'ABCDEFG'
    assert type(record[3]) == datetime and type(record[3]) == datetime
    assert record[3] == timestamp
    assert record[3] == record[4]
