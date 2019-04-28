import tempfile
import unittest
import os


class TempEnv:

    def __init__(self, test_case: unittest.TestCase):
        self._test_case = test_case

        self.dir = tempfile.TemporaryDirectory()
        self.name = self.dir.name

    def path_into(self, *names):
        return os.path.join(self.name, *names)

    def make_dirs(self, *names, **kwargs):
        path = os.path.join(self.name, *names)
        return os.makedirs(path, **kwargs)

    def make_file(self, *names, content=None, **kwargs):
        path = os.path.join(self.name, *names)
        with open(path, 'w', **kwargs) as file:
            if content is not None:
                file.write(content)
            return file.name

    def cleanup(self):
        self.dir.cleanup()

    def assert_file_exists(self, path, with_content=None, message=None, prefix_tgt_dir=True):
        if prefix_tgt_dir:
            expected_path = os.path.join(self.name, path)
        else:
            expected_path = path

        if not os.path.isfile(expected_path):
            if message is None:
                message = f"expected file '{path}' to exist"
            self._test_case.fail(message)
        elif with_content is not None:
            with open(expected_path) as file:
                contents = file.read()
                if message is None:
                    message = f"expected file '{path}' to to have specific contents"
                self._test_case.assertEqual(with_content, contents, message)

    def assert_folder_exists(self, path, message=None, prefix_tgt_dir=True):
        if prefix_tgt_dir:
            expected_path = os.path.join(self.name, path)
        else:
            expected_path = path

        if not os.path.isdir(expected_path):
            if message is None:
                message = f"expected folder '{path}' to exist"
            self._test_case.fail(message)
