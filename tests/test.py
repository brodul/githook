from ConfigParser import ConfigParser
import io
import unittest


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
        self.assertEqual(response.data, "No rule mached!")


class BadConfigTest(unittest.TestCase):
    """docstring for BadConfigTest"""

    def setUp(self):
        import githook

        self.githook = githook
        self.githook.app.config['TESTING'] = True

        self.config = ConfigParser()

    def test_no_name(self):
        """docstring for test_no_name"""
        sample = ("[no-name]\n"
                 "owner=brodul\n"
                 "branch=master\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Section "no-name" must have "name" option!'])

    def test_no_owner(self):
        """docstring for test_no_owner"""
        sample = ("[no-owner]\n"
                 "name=test\n"
                 "branch=master\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Section "no-owner" must have "owner" option!'])

    def test_no_cmd(self):
        """docstring for test_no_cmd"""
        sample = ("[no-cmd]\n"
                 "name=test\n"
                 "owner=brodul\n"
                 "branch=master")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Section "no-cmd" must have "cmd" option!'])

    def test_no_tag_branch(self):
        """docstring for no_tag_no_branch"""
        sample = ("[no-branch-no-tag]\n"
                 "name=test\n"
                 "owner=brodul\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Please put tag OR branch option in the "no-branch-no-tag" section!'])

    def test_tag_branch(self):
        """docstring for test_tag_branch"""
        sample = ("[branch-tag]\n"
                 "name=test\n"
                 "owner=brodul\n"
                 "branch=master\n"
                 "tag=lol\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
        ['Please put only tag OR branch option in the "branch-tag" section!'])

if __name__ == '__main__':
    unittest.main()
