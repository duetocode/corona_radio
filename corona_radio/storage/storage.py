from .connection_factory import DatabaseConnectionFactory
from .database_injector import DatabaseInjector
from .subscription import SubscriptionStorage
from .podcast import PodcastStorage
from .download_task import DownloadTaskStorage

class StorageService:

    def __init__(self, databaseConnectionFactory=None):
        if databaseConnectionFactory is not None:
            self._databaseConnectionFactory = databaseConnectionFactory
        else:
            self._databaseConnectionFactory = DatabaseConnectionFactory('storage.db')

        self._subscriptionStorage = DatabaseInjector(SubscriptionStorage(), self._databaseConnectionFactory)
        self._podcastStorage = DatabaseInjector(PodcastStorage(), self._databaseConnectionFactory)
        self._downloadTaskStorage = DatabaseInjector(DownloadTaskStorage(), self._databaseConnectionFactory)
    
    @property
    def subscriptionStorage(self):
        return self._subscriptionStorage

    @property
    def podcastStorage(self):
        return self._podcastStorage
    
    @property
    def downloadTaskStorage(self):
        return self._downloadTaskStorage
