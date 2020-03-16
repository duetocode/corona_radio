import logging
from corona_radio.subscription import SubscriptionManager
from corona_radio.storage import ManagedStorage, DatabaseConnectionFactory

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    connectionFactory = DatabaseConnectionFactory()
    storage = ManagedStorage(connectionFactory)
    manager = SubscriptionManager(storage=storage)
    subscription = manager.addSubscription('https://podcasts.files.bbci.co.uk/p02nq0gn.rss')

    print(f'Subscripted to {subscription.title}')