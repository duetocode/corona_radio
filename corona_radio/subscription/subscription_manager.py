import requests
from corona_radio.entity import RSSEndpoint
from types import SimpleNamespace
from datetime import datetime
import logging
from pubsub import pub

class SubscriptionManager:

    def __init__(self, storage):
        self._storage = storage
        self._logger = logging.getLogger('SubscriptionManager')
    
    def subscriptTo(self, url):
        ''' Subscript to a new Podcast '''
        subscription, rssEntity = self._update(url)

        # send new subscription message
        pub.sendMessage('subscription.created', subscription=subscription, rssEntity=rssEntity)

        return subscription

    def pollSubscriptions(self):
        ''' Poll all subscriptions '''
        discovery = []
        self._logger.info('Begin poll subscriptions for new podcasts.')
        subscriptionList = self._storage.subscriptionStorage.findAll()

        self._logger.info('We have %d subscriptions to poll', len(subscriptionList))
        for subscription in subscriptionList:
            self._logger.info('Poll %s', subscription.title)
            try:
                subscription, rssEntity = self._update(subscription.url)
            except Exception as err:
                self._logger.error('Failed to poll subscrition %d:%s due to error %s', subscription.id, subscription.title, err)
                continue
            # Send subscription updated message
            pub.sendMessage('subscription.updated', subscription=subscription, rssEntity=rssEntity)
    
    def _update(self, url):
        # Fetch its information from url
        self._logger.info('Requesting rss from %s', url)
        response = requests.get(url)
        response.raise_for_status()
        self._logger.info('Got response from %s', url)

        # Parse RSS
        self._logger.info('Try to parse the response text as RSS documentation')
        entity = RSSEndpoint.fromString(response.text)
        self._logger.info('Parsed the RSS successfully.')

        entity.link = url
        # Save it to storage
        currentDateTime = datetime.utcnow()
        subscription = self._storage.subscriptionStorage.save(SimpleNamespace(
                    title = entity.title,
                    link = entity.link,
                    createdAt = currentDateTime,
                    updatedAt = currentDateTime))
        self._logger.info('Subscription with title %s was saved to the storage.', subscription.title)
        return subscription, entity
    
        '''
            # Process Items
            for podcast in entity.items:
                item = self._storage.findPodcast(subscription.id, podcast.id)
                if item is not None:
                    # the podcast already exists
                    continue
                else:
                    # Save it to database
                    newPodcast = self._storage.savePodcast(subscription.id, podcast)
                    discovery.append(newPodcast)
        return discovery
        '''