from pubsub import pub
from types import SimpleNamespace
import logging

class PodcastManager:

    def __init__(self, storage):
        self._storage = storage
        self._logger = logging.getLogger('PodcastManager')
        pub.subscribe(self. subscriptionUpdated, 'subscription.updated')
        pub.subscribe(self. subscriptionUpdated, 'subscription.created')

    def subscriptionUpdated(self, subscription, rssEntity):
        self._logger.info('We have a subscription [%d-%s] to scan.', subscription.id, subscription.title)
        # Find new rssEntities
        discoveries = []
        for podcast in rssEntity.items:
            item = self._storage.podcastStorage.findPodcast(subscription.id, podcast.id)
            if item is not None:
                # the podcast already exists
                continue
            else:
                # Save it to database
                discoveries.append(podcast)
                self._logger.info('Found new podcast: %s', podcast.title)
        
        if len(discoveries) == 0:
            self._logger.info('There is no new podcast.')
            return
        
        self._logger.info('We have found %d new podcasts.', len(discoveries))

        # Save them to database
        self._storage.podcastStorage.saveBatch(subscription.id, discoveries)

        # Broadcast new findings
        pub.sendMessage('podcast.dicovery', discoveries=discoveries)