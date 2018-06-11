import re


class WpInstance():
    def __init__(self, key, name, wp_path, host, user):
        self.key = key
        self.name = name
        self.wp_path = wp_path
        self.host = host
        self.user = user

    def check_version(self):
        """
        Get the Wordpress version installed in the given path.
        """
        try:
            content = self.get_content()
            match = re.search(r"\$wp_version = \'(.+)\';", content)
            if match:
                return match.group(1)
            else:
                raise Exception
        except:
            "Unable to find Wordpress in the path specified."

    def get_content(self):
        """
        Get the content of the WordPress version file (locally or on a remote server).
        """
        version_file = self.wp_path + '/wp-includes/version.php'

        if (self.host == None and self.user == None):
            with open(version_file) as versionfile:
                    return versionfile.read()

        from connection import SSHClient
        with SSHClient(self.host, self.user) as conn:
            return conn.readfile(version_file)
