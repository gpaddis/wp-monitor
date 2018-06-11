import sqlite3
import paramiko
from datetime import datetime
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
                wp_path TEXT,
                host TEXT,
                user TEXT
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

    def insert_instance(self, name, wp_path, ssh_host=None, ssh_user=None):
        """ Insert a new Wordpress instance in the database. """
        with self.conn:
            self.c.execute("""
                INSERT INTO wp_instances (name, host, user, wp_path)
                VALUES (:name, :host, :user, :wp_path)
                """,
                {
                    'name': name,
                    'host': ssh_host,
                    'user': ssh_user,
                    'wp_path': wp_path
                })

    def get_instances(self):
        """ Return a list containing all instances in the database. """
        with self.conn:
            self.c.execute("SELECT * from wp_instances")
            instances = self.c.fetchall()
        return [WpInstance(*instance) for instance in instances]

    def get_last_saved_version(self, instance_id):
        """ Get the latest instance version saved in the database. """
        with self.conn:
            self.c.execute("""
                SELECT id, version, last_check FROM wp_instances_versions
                WHERE instance_id = ?
                ORDER BY first_check DESC
            """, (instance_id,))
            return self.c.fetchone()
            # TODO: Return a dictionary?

    def update_version(self, instance_id, version):
        """
        Insert the new version for the given Wordpress instance ID,
        or update the last_check timestamp for the current version.
        """
        with self.conn:
            now = datetime.now()
            last_saved_record = self.get_last_saved_version(instance_id)
            if last_saved_record is not None:
                last_saved_id = last_saved_record[0]
                last_saved_version = last_saved_record[1]
            else:
                last_saved_version = None

            if version != last_saved_version:
                self.c.execute("""
                    INSERT INTO wp_instances_versions (instance_id, version, first_check, last_check)
                    VALUES (?, ?, ?, ?)
                """, (instance_id, version, now, now))
            else:
                self.c.execute("""
                    UPDATE wp_instances_versions
                    SET last_check = ?
                    WHERE id = ?
                """, (now, last_saved_id))

class SSHClient():
    """
    A wrapper around paramiko's SSH client.
    See: https://gist.github.com/acdha/6064215
    """

    def __init__(self, host, username):
        self.host = host
        self.username = username
        self.client = paramiko.SSHClient()
        self.client._policy = paramiko.WarningPolicy()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        self.client.connect(self.host, username=self.username)

    def disconnect(self):
        self.client.close()

    def readfile(self, file_path):
        try:
            sftp_client = self.client.open_sftp()
            remote_file = sftp_client.open(file_path)
            return remote_file.read()
        except:
            return "Unable to read the remote file."
