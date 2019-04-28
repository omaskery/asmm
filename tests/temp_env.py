import tempfile
import unittest
import os


class TempEnv:
    """
    Utility to reduce boilerplate when testing an
    application in a temporary folder, allowing easy
    generation of filesystem states and subsequent
    assertions to be made
    """

    def __init__(self, test_case: unittest.TestCase):
        """
        :param test_case: parent test case to use for performing assertions
        """

        self._test_case = test_case

        self.dir = tempfile.TemporaryDirectory()
        self.name = self.dir.name

    def path_into(self, *names):
        """
        Generate a filepath relative to the temporary directory created
        by this utility class
        :param names: list of path components to combine before being prefixed
          with the directory path
        :return: generated filepath
        """
        return os.path.join(self.name, *names)

    def make_dirs(self, *names, **kwargs):
        """
        Creates directories specified within the temporary folder
        :param names: list of path components to combine into path of folder to create
        :param kwargs: keyword parameters to pass through to os.makedirs
        :return: path to newly created folder
        """

        path = os.path.join(self.name, *names)
        os.makedirs(path, **kwargs)
        return path

    def make_file(self, *names, content=None, **kwargs):
        """
        Creates file specified within the temporary folder, optionally with given content
        :param names: list of path components to combine into path of file to create
        :param content: optional content to write into the created file
        :param kwargs: keyword parameters to pass through to open call
        :return: path to newly created file
        """

        path = os.path.join(self.name, *names)
        with open(path, 'w', **kwargs) as file:
            if content is not None:
                file.write(content)
            return file.name

    def cleanup(self):
        """Cleans up the temporary directory, typically called in the tearDown() method of test
        """
        self.dir.cleanup()

    def assert_file_exists(self, path, with_content=None, message=None, prefix_tgt_dir=True):
        """
        Asserts that a file exists, optionally asserting its contents.
        :param path: path to the file to check for existence
        :param with_content: optional contents to assert the file contains
        :param message: optional message to display if any assertions fail
        :param prefix_tgt_dir: determines whether path should be prefixed with temporary folder path
        """

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
        """
        Asserts that a folder exists
        :param path: path to the folder to check for existence
        :param message: optional message to display if any assertions fail
        :param prefix_tgt_dir: determines whether path should be prefixed with temporary folder path
        """

        if prefix_tgt_dir:
            expected_path = os.path.join(self.name, path)
        else:
            expected_path = path

        if not os.path.isdir(expected_path):
            if message is None:
                message = f"expected folder '{path}' to exist"
            self._test_case.fail(message)
