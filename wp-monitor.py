#!/usr/bin/env python

from wordpress.connection import WpDatabase

wp_database = 'wp-monitor.db'

def add_instance(conn, name, server, wp_path):
    """ Insert a new instance in the database. """
    conn.insert_instance(name, server, wp_path)

def list_instances(conn):
    """ List all instances with datetime of last_check. """
    instances = conn.get_instances()
    for instance in instances:
        version = conn.get_last_saved_version(instance.key)
        print "{}: Saved Version: {} Last check on: {}".format(instance.name, version[1], version[2])

def update_instances(conn):
    """ Check the version for all instances and update the database. """
    instances = conn.get_instances()
    for instance in instances:
        current_version = instance.check_version()
        conn.update_version(instance.key, current_version)

def main():
    with WpDatabase('wp-monitor.db') as conn:
        update_instances(conn)
        print "Checked the version for all instances and updated the database."
        list_instances(conn)

if __name__ == '__main__':
    main()
