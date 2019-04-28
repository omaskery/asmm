import unittest
import yaml


from tests.temp_env import TempEnv
import asmm


class TestInitialisation(unittest.TestCase):

    EXPECTED_DIRECTORIES = [
        "missions",
        "test_missions",
        "assets",
        ".asmm",
        ".asmm/cache/deps"
    ]

    def setUp(self):
        self.temp_env = TempEnv(self)

    def tearDown(self):
        self.temp_env.cleanup()

    def test_init_does_not_crash(self):
        asmm.initialise(target_directory=self.temp_env.name)

    def test_init_makes_expected_folders(self):
        asmm.initialise(target_directory=self.temp_env.name)
        for directory in self.EXPECTED_DIRECTORIES:
            with self.subTest(f"checking for directory {directory}", directory=directory):
                self.temp_env.assert_folder_exists(directory)

    def test_init_makes_project_yml_file(self):
        asmm.initialise(target_directory=self.temp_env.name)
        project_file_path = self.temp_env.path_into(".asmm", "config.yml")
        with open(project_file_path) as project_file:
            _ = yaml.load(project_file, Loader=yaml.SafeLoader)

    def test_init_twice_does_not_crash(self):
        asmm.initialise(target_directory=self.temp_env.name)
        asmm.initialise(target_directory=self.temp_env.name)

    def test_init_twice_does_not_remove_files(self):
        asmm.initialise(target_directory=self.temp_env.name)
        files_to_validate = []
        test_magic = "test magic wow"
        for directory in self.EXPECTED_DIRECTORIES:
            file_name = self.temp_env.make_file(directory, "test.dat", content=test_magic)
            files_to_validate.append((directory, file_name))
        asmm.initialise(target_directory=self.temp_env.name)
        for directory, path in files_to_validate:
            with self.subTest(f"validating '{directory}' folder preserved"):
                self.temp_env.assert_file_exists(path, with_content=test_magic, prefix_tgt_dir=False)
