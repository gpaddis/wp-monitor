import unittest
from wordpress.connection import WpDatabase

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.db = WpDatabase(':memory:')
        self.db.insert_instance('Wordpress Test', None, 'path/to/installation')

    def tearDown(self):
        self.db.conn.close()

    def test_get_instances(self):
        self.assertEqual(1, len(self.db.get_instances()))

    def test_get_last_saved_version(self):
        self.assertEqual(None, self.db.get_last_saved_version(1))
        self.db.update_version(1, '4.5.8')
        self.assertEqual('4.5.8', self.db.get_last_saved_version(1)[1])

    def test_update_same_version(self):
        self.db.update_version(1, '4.5.8')
        before_update = self.db.get_last_saved_version(1)[2]
        self.db.update_version(1, '4.5.8')
        after_update = self.db.get_last_saved_version(1)[2]

        self.assertEqual('4.5.8', self.db.get_last_saved_version(1)[1])
        self.assertGreater(after_update, before_update)

    def test_update_next_version(self):
        self.db.update_version(1, '4.5.8')
        self.db.update_version(1, '4.5.9')
        self.assertEqual('4.5.9', self.db.get_last_saved_version(1)[1])
