import sqlite3

class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("addons/main.db", check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` INT, `join_date` INT, `limit` INT, `step` TEXT);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `limits` (`phone_number` INT, `limit` INT);")
        self.cursor.execute("UPDATE `users` SET `step` = '';")
        self.connection.commit()
        
    def add_user(self, user_id, timestamp):
        self.cursor.execute("INSERT INTO `users` (`user_id`, `join_date`, `limit`, `step`) VALUES (?, ?, ?, ?);", (user_id, timestamp, 0, None))
        self.connection.commit()
        
    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?;", (user_id,))
        result = self.cursor.fetchone()
        
        if result is not None:
            return result
        
        return False
        
    def edit_user(self, user_id, column, value):
        self.cursor.execute(f"UPDATE `users` SET `{column}` = ? WHERE `user_id` = ?;", (value, user_id))
        self.connection.commit()