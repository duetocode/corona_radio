from types import SimpleNamespace

class PodcastStorage:

    def savePodcast(self, cursor, conn, subscriptionId, podcast):
        assert podcast.id is not None
        cursor.execute('INSERT INTO podcast (id, subscription_id, title, description, publish_date, url, length) values (?,?,?,?,?,?,?)', [
            podcast.id,
            subscriptionId,
            podcast.title,
            podcast.description,
            podcast.publishedAt.timestamp(),
            podcast.url,
            podcast.length])
        return podcast

    def saveBatch(self, cursor, conn, subscriptionId, podcasts):
        inputs = map(lambda podcast:[
                        podcast.id,
                        subscriptionId,
                        podcast.title,
                        podcast.description,
                        podcast.publishedAt.timestamp(),
                        podcast.url,
                        podcast.length], podcasts)
        cursor.executemany('''
            INSERT INTO podcast 
                (id, subscription_id, title, description, publish_date, url, length) 
            VALUES 
                (?,?,?,?,?,?,?)''', inputs)

    def findPodcast(self, cursor, conn, subscriptionId, podcastId):
        cursor.execute('SELECT id, title, description, publish_date, url, length FROM podcast WHERE id = ? and subscription_id = ?', [
            podcastId, 
            subscriptionId
        ])
        record = cursor.fetchone()
        if record is None:
            return None
        else:
            item = RSSItem()
            item.id, item.title, item.description, item.publishedAt, item.url, item.length = record
            return item


    def findAllPodcasts(self, cursor, conn):
        cursor.execute('SELECT `id`, `subscription_id`, `title`, `description`, `publish_date`, `url`, `length`, `downloaded` FROM podcast ORDER BY `publish_date` DESC')
        return [mapToPodcast(record) for record in cursor]

    def markDownloaded(self, cursor, conn, podcastId, subscriptionId):
        cursor.execute('''
            UPDATE podcast SET downloaded = 1
            WHERE id = ? and subscription_id = ?
            ''', [podcastId, subscriptionId])


def mapToPodcast(record):
    return SimpleNamespace(
        id = record[0],
        subscriptionId = record[1],
        title = record[2],
        description = record[3],
        publishDate = datetime.fromtimestamp(record[4]),
        url = record[5],
        length = record[6],
        downloaded = record[7])
