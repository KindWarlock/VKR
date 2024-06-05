import sqlite3


class SqliteDB:
    def __init__(self, game):
        self.conn = sqlite3.connect('scores.db')
        self.cursor = self.conn.cursor()
        self.game = game
        self._createTable()

    def insertScore(self, name, score):
        name = name.strip()
        query = f'''SELECT name, score FROM {
            self.game} WHERE name=? LIMIT 1'''
        res = self.cursor.execute(query, (name, )).fetchone()
        if res != None and res[1] >= score:
            return
        query = f'''INSERT OR REPLACE INTO {
            self.game} (name, score) VALUES (?, ?)'''
        self.cursor.execute(query, (name, score))
        self.conn.commit()

    def retrieveScore(self, player, limit=5):
        query = f'''SELECT name, score FROM {
            self.game} ORDER BY score DESC'''

        resAll = self.cursor.execute(query).fetchall()

        # Для каждого игрока указываем позицию в рейтинге
        scores = list(zip(range(limit), resAll[:limit]))

        # Ищем текущего игрока в полученных результатах
        playerScore = None
        for i, res in enumerate(resAll):
            if res[0] == player:
                playerScore = i, (player, res[1])
            break

        # Если игрок не был найден, добавляем его с нулем очков
        if playerScore == None:
            idx = len(resAll) + 1
            playerScore = idx, (player, 0)
        scores.append(playerScore)

        return scores

    def _createTable(self):
        query = f'''CREATE TABLE IF NOT EXISTS {
            self.game} (name TEXT PRIMARY KEY, score INTEGER)'''
        self.cursor.execute(query)
        self.conn.commit()
