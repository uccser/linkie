import os
import unittest
from subprocess import run
from linkie import Linkie

class LinkieTestSuite(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.default_working_directory = os.getcwd()

    def setUp(self):
        os.chdir(self.default_working_directory)

    def test_basic(self):
        os.chdir('./linkie/tests/assets/basic/')
        linkie = Linkie()
        self.assertEqual(linkie.run(), 0)

    def test_broken(self):
        os.chdir('./linkie/tests/assets/broken/')
        linkie = Linkie()
        self.assertEqual(linkie.run(), 1)

    def test_multiple(self):
        os.chdir('./linkie/tests/assets/multiple/')
        linkie = Linkie()
        self.assertEqual(linkie.run(), 0)

    def test_excluded_directories(self):
        os.chdir('./linkie/tests/assets/excluded_directories/')
        linkie = Linkie()
        self.assertEqual(linkie.run(), 0)

    def test_excluded_directories_custom(self):
        os.chdir('./linkie/tests/assets/excluded_directories_custom/')
        linkie = Linkie('linkie.yaml')
        self.assertEqual(linkie.run(), 0)

    def test_file_types(self):
        os.chdir('./linkie/tests/assets/file_types/')
        linkie = Linkie()
        self.assertEqual(linkie.run(), 0)

    def test_file_types_custom(self):
        os.chdir('./linkie/tests/assets/file_types_custom/')
        linkie = Linkie('linkie.yaml')
        self.assertEqual(linkie.run(), 1)

    def test_skip_urls(self):
        os.chdir('./linkie/tests/assets/skip_urls/')
        linkie = Linkie()
        self.assertEqual(linkie.run(), 0)
        self.assertEqual(len(linkie.urls), 2)

    def test_skip_urls_custom(self):
        os.chdir('./linkie/tests/assets/skip_urls_custom/')
        linkie = Linkie('linkie.yaml')
        self.assertEqual(linkie.run(), 0)
        self.assertEqual(len(linkie.urls), 1)

    def test_command_line_basic(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/basic/')
        self.assertEqual(linkie.returncode, 0)

    def test_command_line_broken(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/broken/')
        self.assertEqual(linkie.returncode, 1)

    def test_command_line_multiple(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/multiple/')
        self.assertEqual(linkie.returncode, 0)

    def test_command_line_excluded_directories(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/excluded_directories/')
        self.assertEqual(linkie.returncode, 0)

    def test_command_line_excluded_directories_custom(self):
        linkie = run(['linkie', 'linkie.yaml'], cwd='./linkie/tests/assets/excluded_directories_custom/')
        self.assertEqual(linkie.returncode, 0)

    def test_command_line_file_types(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/file_types/')
        self.assertEqual(linkie.returncode, 0)

    def test_command_line_file_types_custom(self):
        linkie = run(['linkie', 'linkie.yaml'], cwd='./linkie/tests/assets/file_types_custom/')
        self.assertEqual(linkie.returncode, 1)


if __name__ == '__main__':
    unittest.main()
