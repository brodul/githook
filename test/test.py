import os
import unittest

import githook

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        githook.app.config['TESTING'] = True
        self.app = githook.app.test_client()
        self.ct = "application/x-www-form-urlencoded"

        CONFIG = "test/config/okconfig.ini"
        githook.config.read(CONFIG)

    def test_get(self):
        """docstring for test_get"""
        request = self.app.get('/')
        self.assertEqual(request.status_code, 302)

    def test_post_branch(self):
        """docstring for test_post_branch"""
        with open("test/json/branch.json") as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload':json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "OK")

    def test_post_tags(self):
        """docstring for test_post_tags"""

        with open("test/json/tags.json") as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload':json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "OK")


if __name__ == '__main__':
    unittest.main()
