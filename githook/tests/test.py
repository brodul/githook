from ConfigParser import ConfigParser
import io
import os
import tempfile
import sys

# python 2.6 support
if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

from scripttest import TestFileEnvironment

here = os.path.dirname(__file__)
is_travis = os.getenv("TRAVIS") == 'true', "Skip test on travis"


class GithookTestCase(unittest.TestCase):

    def setUp(self):
        import githook

        githook.app.config['TESTING'] = True
        self.app = githook.app.test_client()
        self.ct = "application/x-www-form-urlencoded"

        CONFIG = os.path.join(here, "config/okconfig.ini")
        config = ConfigParser()
        config.read(CONFIG)
        githook.app.config["iniconfig"] = config

    def test_get(self):
        request = self.app.get('/')
        self.assertEqual(request.status_code, 302)

    def test_post_branch(self):
        with open(os.path.join(here, "json/branch.json")) as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload': json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "OK")

    def test_no_section(self):
        with open(os.path.join(here, "json/nosection.json")) as f:
            json = f.readline()
        response = self.app.post(
            '/',
            data={'payload': json},
            content_type=self.ct
        )
        self.assertEqual(response.data, "No section mached!")


class ConfigTestTest(unittest.TestCase):

    def setUp(self):
        import githook

        self.githook = githook
        self.githook.app.config['TESTING'] = True
        self.okconfig = os.path.join(here, "config/okconfig.ini")

        self.config = ConfigParser()

    def test_config_ok(self):
        self.config.read(self.okconfig)
        self.assertEqual(self.githook.test_config(self.config),
            [])

    def test_no_name(self):
        sample = ("[no-name]\n"
                 "owner=brodul\n"
                 "branch=master\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Section "no-name" must have "name" option!'])

    def test_no_owner(self):
        sample = ("[no-owner]\n"
                 "name=test\n"
                 "branch=master\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Section "no-owner" must have "owner" option!'])

    def test_no_cmd(self):
        sample = ("[no-cmd]\n"
                 "name=test\n"
                 "owner=brodul\n"
                 "branch=master")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Section "no-cmd" must have "cmd" option!'])

    def test_no_tag_branch(self):
        sample = ("[no-branch-no-tag]\n"
                 "name=test\n"
                 "owner=brodul\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
            ['Please put tag OR branch option in the "no-branch-no-tag" section!'])

    def test_tag_branch(self):
        sample = ("[branch-tag]\n"
                 "name=test\n"
                 "owner=brodul\n"
                 "branch=master\n"
                 "tag=lol\n"
                 "cmd=ls")
        self.config.readfp(io.BytesIO(sample))
        self.assertEqual(self.githook.test_config(self.config),
        ['Please put only tag OR branch option in the "branch-tag" section!'])


class CLITest(unittest.TestCase):

    def setUp(self):
        import githook

        self.githook = githook
        self.githook.app.config['TESTING'] = True

        self.tempdir = tempfile.mkdtemp()
        self.env = TestFileEnvironment(
            os.path.join(self.tempdir,'test-output'),
            ignore_hidden=False)

    @unittest.skipIf(*is_travis)
    def test_no_config(self):
        result = self.env.run('bin/python %s' % os.path.join(here, "..", "__init__.py"),
            expect_error=True,
            cwd=os.path.join(here, '../', '../')
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, u'CRITICAL:root:Configuration file not found. Please specify one.\n')

    # TODO This loops. :D Need another way of testing daemons.
    @unittest.skipIf(True, 'It loops')
    def test_ok_config(self):
        self.env.run('bin/python -m githook -c githook/tests/config/okconfig.ini',
            cwd=os.path.join(here, '../', '../')
        )

if __name__ == '__main__':
    unittest.main()
