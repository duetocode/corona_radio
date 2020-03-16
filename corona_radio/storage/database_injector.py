

class DatabaseInjector:

    def __init__(self, storageService, databaseConnectionFactory):
        self._service = storageService
        self._databaseConnectionFactory = databaseConnectionFactory

    def __getattr__(self, attr):
        target = getattr(self._service, attr)
        if not callable(target):
            return target
        else:
            return self._wrap(target)

    def _wrap(self, targetMethod):
        def execute(*args, **kwargs):
            conn = None
            cursor = None

            try:
                conn = self._databaseConnectionFactory.getConnection()
                cursor = conn.cursor()
                return targetMethod(cursor, conn, *args, **kwargs)

            except Exception as e:
                if conn is not None:
                    conn.rollback()
                raise e

            finally:
                if cursor is not None:
                    cursor.close()

        return execute