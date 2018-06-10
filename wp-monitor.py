#!/usr/bin/env python

from wordpress.connection import WpDatabase


def main():
    with WpDatabase('wp-monitor.db') as conn:
        conn.insert_instance('LocalWp', 'user@localhost', 'test/wordpress-test')

        for instance in conn.get_instances():
            print "Name: {} Version: {}".format(instance.name, instance.check_version())

if __name__ == '__main__':
    main()
