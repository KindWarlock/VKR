import sqlite3


class SqliteDB:
    def __init__(self, game):
        self.conn = sqlite3.connect('scores.db')
        self.cursor = self.conn.cursor()
        self._createTable(game)

    def insertScore(self, game, name, score):
        query = f'INSERT OR REPLACE INTO {game} VALUES ({name}, {score})'
        self.cursor.execute(query)
        self.conn.commit()

    def retrieveScore(self, game, limit=5):
        query = f'SELECT * FROM {game} ORDER BY score DESC LIMIT {limit}'
        res = self.cursor.execute(query)
        return res.fetchall()

    def _createTable(self, game):
        query = f'CREATE TABLE IF NOT EXISTS {
            game} (name TEXT, score INTEGER)'
        self.cursor.execute(query)
        self.conn.commit()
