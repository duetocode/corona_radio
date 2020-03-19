import logging
from corona_radio.subscription import SubscriptionManager
from corona_radio.storage import StorageService

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    storageService = StorageService()
    subscriptionManager = SubscriptionManager(storageService)
    subscription = subscriptionManager.subscriptTo('https://podcasts.files.bbci.co.uk/p02nq0gn.rss')

    print(f'Subscripted to {subscription.title}')