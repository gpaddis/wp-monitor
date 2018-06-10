#!/usr/bin/env python

import re

def get_version(wp_path):
    """
    Get the Wordpress version installed in the given path
    """
    try:
        with open(wp_path + '/wp-includes/version.php') as versionfile:
            content = versionfile.read()
        match = re.search(r"\$wp_version = \'(.+)\';", content)
        if match:
            return match.group(1)
        else:
            raise Exception
    except:
        print "Unable to find Wordpress in the path specified."

def main():
    print get_version('test/wordpress-test')

if __name__ == '__main__':
    main()
