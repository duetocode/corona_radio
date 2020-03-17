import pytest
from pytest_httpserver import HTTPServer
from corona_radio.subscription.subscription_manager import SubscriptionManager
from types import SimpleNamespace
from pubsub import pub
from datetime import datetime, timedelta

@pytest.fixture
def podcastURL(httpserver: HTTPServer):
    with open('test/bbc-world-news.xml', 'r') as fd:
        httpserver.expect_request('/bbc-world-news.rss') \
                    .respond_with_data(fd.read(), content_type='application/rss+xml')    
    httpserver.expect_request('/invalid') \
                    .respond_with_data(b'', status=404)
    return httpserver.url_for('/bbc-world-news.rss')


def test_add_new(podcastURL):
    # Setup Storage
    def save(entity):
        entity.id = 1234
        return entity

    storage = SimpleNamespace(subscriptionStorage=SimpleNamespace(save=save))

    # Listen to topic
    flags = [False]
    def newSubscription(subscription, rssEntity):
        subscription is not None
        assert subscription.id == 1234
        assert subscription.createdAt is not None
        assert subscription.updatedAt is not None
        assert rssEntity.title == 'Global News Podcast'
        flags[0] = True
    pub.subscribe(newSubscription, 'subscription.created')

    # Add
    manager = SubscriptionManager(storage)
    actual = manager.subscriptTo(podcastURL)
    
    # Verify
    assert actual.id == 1234
    assert flags[0] == True

def test_poll(podcastURL):
    # Setup Storage
    today = datetime.utcnow()
    yestoday = datetime.utcnow() - timedelta(days=1)
    weekBefore = datetime.utcnow() - timedelta(weeks=1)
    def findAll():
        result = [
            SimpleNamespace(id=0, title='a', link=podcastURL, createdAt=today, updatedAt=today),
            SimpleNamespace(id=1, title='b', link=podcastURL + 'invalid', createdAt=yestoday, updatedAt=yestoday),
            SimpleNamespace(id=2, title='c', link=podcastURL, createdAt=weekBefore, updatedAt=weekBefore)
        ]
        return result
    saved = []
    def save(entity):
        saved.append(entity)
        return entity

    storage = SimpleNamespace(
        subscriptionStorage = SimpleNamespace(
            save = save,
            findAll = findAll
        )
    )

    # Setup Listener
    events = []
    def subscriptionUpdated(subscription, rssEntity):
        events.append((subscription, rssEntity))
    pub.subscribe(subscriptionUpdated, 'subscription.updated')

    # Execute
    subscriptionManager = SubscriptionManager(storage)
    subscriptionManager.pollSubscriptions()

    # Verify
    assert len(events) == 2
    assert len(saved) == 2

