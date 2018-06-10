#!/usr/bin/env python

from wordpress.connection import WpDatabase


def main():
    with WpDatabase('wp-monitor.db') as conn:
        # conn.insert_instance('Another WP Instance', 'seconduser@localhost', 'test/wordpress-test')

        for instance in conn.get_instances():
            current_version = instance.check_version()
            print "Name: {} Version: {}".format(instance.name, current_version)

            conn.update_version(instance.key, current_version)

if __name__ == '__main__':
    main()
