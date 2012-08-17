import unittest
from ConfigParser import ConfigParser


class GithookTestCase(unittest.TestCase):

    def setUp(self):
        import githook

        githook.app.config['TESTING'] = True
        self.app = githook.app.test_client()
        self.ct = "application/x-www-form-urlencoded"

        CONFIG = "tests/config/okconfig.ini"
        config = ConfigParser()
        config.read(CONFIG)
        githook.app.config["iniconfig"] = config

    def test_get(self):
        """docstring for test_get"""
        request = self.app.get('/')
        self.assertEqual(request.status_code, 302)

    def test_post_branch(self):
        """docstring for test_post_branch"""
        with open("tests/json/branch.json") as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload': json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "OK")

    def test_post_tags(self):
        """docstring for test_post_tags"""

        with open("tests/json/tags.json") as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload': json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "OK")

    def test_no_section(self):
        """"""
        with open("tests/json/nosection.json") as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload': json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "Unknown section!")


if __name__ == '__main__':
    unittest.main()
