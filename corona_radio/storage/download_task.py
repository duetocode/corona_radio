from types import SimpleNamespace

class DownloadTaskStorage:

    def saveDownloadTask(self, cursor, conn, downloadTask):
        cursor.execute('INSERT INTO download_queue (`podcast_id`, `subscription_id`, `priority`) values (?, ?, ?)', [
            downloadTask.podcastId,
            downloadTask.subscriptionId,
            downloadTask.priority])

    def findDownloadTask(self, cursor, conn, podcastId, subscriptionId):
        cursor.execute('SELECT `podcast_id`, `subscription_id`, `priority` FROM download_queue WHERE `podcast_id` = ? and `subscription_id` = ?', [
            podcastId, 
            subscriptionId])
            
        record = cursor.fetchone()
        if record is None:
            return None
        else:
            return mapToDownloadTask(cursor.fetchone())

    def findNextDownloadTask(self, cursor, conn):
        cursor.execute('''
            SELECT 
                t.`podcast_id`, t.`subscription_id`, t.`priority`,
                p.`url`
            FROM download_queue t INNER JOIN podcast p ON t.podcast_id = p.id
            ORDER BY t.priority DESC, p.publish_date DESC
            LIMIT 1
            ''')
        record = cursor.fetchone()
        if record is None:
            return None
        else:
            return mapToDownloadTask(record)
    
    def removeTask(self, cursor, conn, podcastId, subscriptionId):
        cursor.execute('''
            DELETE FROM download_queue 
            WHERE podcast_id = ? and subscription_id = ?
            ''', [podcastId, subscriptionId])


def mapToDownloadTask(record):
    return SimpleNamespace(
        podcastId = record[0],
        subscriptionId = record[1],
        priority = record[2],
        url = record[3]
    )