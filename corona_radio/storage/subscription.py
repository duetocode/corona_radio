from types import SimpleNamespace

class SubscriptionStorage:

    def findAll(self, cursor, conn):
        cursor.execute('SELECT `id`, `title`, `link`, `latest_content`, `created_at`, `updated_at` FROM subscription')
        return [mapToSubscription(record) for record in cursor.fetchall()]

    def save(self, cursor, conn, subscription):
        if hasattr(subscription, 'id') and subscription.id is not None:
            # Update
            cursor.execute('UPDATE subscriptions SET `title`=?, `link`=?, `latest_content`=?,`updated_at`=? WHERE `id`=?', [
                subscription.title,
                subscription.url,
                subscription.latestContent,
                subscription.lastUpdated,
                subscription.id])
        else:
            # Insert new
            cursor.execute('INSERT INTO subscription (`title`, `link`, `latest_content`, `created_at`, `updated_at`) values (?, ?, ?, ?, ?)', [
                subscription.title,
                subscription.link,
                subscription.latestContent,
                subscription.createdAt,
                subscription.updatedAt])
            subscription.id = cursor.lastrowid
        return subscription

        

def mapToSubscription(record):
    return SimpleNamespace(
        id = record[0],
        title = record[1],
        link = record[2],
        latestContent = record[3],
        createdAt = record[4],
        updatedAt = record[5])

