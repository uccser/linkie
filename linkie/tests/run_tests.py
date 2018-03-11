import unittest
from subprocess import run

class LinkieTestSuite(unittest.TestCase):

    def test_basic(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/basic/')
        self.assertEqual(linkie.returncode, 0)

    def test_broken(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/broken/')
        self.assertEqual(linkie.returncode, 1)

    def test_multiple(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/multiple/')
        self.assertEqual(linkie.returncode, 0)

    def test_excluded_directories(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/excluded_directories/')
        self.assertEqual(linkie.returncode, 0)

    def test_excluded_directories_custom(self):
        linkie = run(['linkie', 'linkie.yaml'], cwd='./linkie/tests/assets/excluded_directories_custom/')
        self.assertEqual(linkie.returncode, 0)

    def test_file_types(self):
        linkie = run('linkie', cwd='./linkie/tests/assets/file_types/')
        self.assertEqual(linkie.returncode, 0)

    def test_file_types_custom(self):
        linkie = run(['linkie', 'linkie.yaml'], cwd='./linkie/tests/assets/file_types_custom/')
        self.assertEqual(linkie.returncode, 1)


if __name__ == '__main__':
    unittest.main()
