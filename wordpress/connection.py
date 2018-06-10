import sqlite3
from instance import WpInstance


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
        with self.conn:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS wp_instances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                server TEXT,
                wp_path TEXT
            )""")

            self.c.execute("""
                CREATE TABLE IF NOT EXISTS wp_instances_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance_id INTEGER,
                version TEXT,
                first_check DATETIME,
                last_check DATETIME,
                FOREIGN KEY (instance_id) REFERENCES wp_instances(id)
            )""")

    def insert_instance(self, name, server, wp_path):
        """ Insert a new Wordpress instance in the database. """
        with self.conn:
            self.c.execute("""
                INSERT INTO wp_instances (name, server, wp_path)
                VALUES (:name, :server, :wp_path)
                """,
                           {'name': name, 'server': server, 'wp_path': wp_path})

    def get_instances(self):
        """ Return a list containing all instances in the database. """
        with self.conn:
            self.c.execute("SELECT * from wp_instances")
            instances = self.c.fetchall()
        return [WpInstance(*instance) for instance in instances]