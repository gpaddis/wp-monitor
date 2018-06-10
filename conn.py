import sqlite3


class WpDatabase():
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()

    def __enter__(self):
        """
        Use the object in a content manager.
        See: https://stackoverflow.com/a/865272/7874784
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Close the connection when exiting from the content manager. """
        self.conn.close()

    def create_tables(self):
        """ Create the tables """
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS wp_instances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            server TEXT,
            wp_path TEXT
        )""")
        self.conn.commit()

    def insert_instance(self, name, server, wp_path):
        """ Insert a new Wordpress instance in the database """
        self.c.execute("""
            INSERT INTO wp_instances (name, server, wp_path)
            VALUES (:name, :server, :wp_path)
            """,
            { 'name': name, 'server': server, 'wp_path': wp_path})
        self.conn.commit()

with WpDatabase('wp-monitor.db') as conn:
    conn.insert_instance('Testsite', 'Testserver', '/path/1/2/3/4')
