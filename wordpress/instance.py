import re


class WpInstance():
    def __init__(self, key, name, server, wp_path):
        self.key = key
        self.name = name
        self.server = server
        self.wp_path = wp_path

    def check_version(self):
        """
        Get the Wordpress version installed in the given path.
        """
        try:
            with open(self.wp_path + '/wp-includes/version.php') as versionfile:
                content = versionfile.read()
            match = re.search(r"\$wp_version = \'(.+)\';", content)
            if match:
                return match.group(1)
            else:
                raise Exception
        except:
            "Unable to find Wordpress in the path specified."
