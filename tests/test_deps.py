import unittest
import yaml


from tests.temp_env import TempEnv
import asmm


class TestDependencies(unittest.TestCase):

    def setUp(self):
        self.temp_env = TempEnv(self)
        self.temp_env.make_dirs(".asmm")

    def tearDown(self):
        self.temp_env.cleanup()

    def test_list_deps(self):
        expected_dependencies = [
            "file://../other-proj",
            "https://github.com/user/project/archive/master.zip",
        ]
        self._write_project_file({
            "dependencies": expected_dependencies,
        })
        dependencies = asmm.list_dependencies(self.temp_env.name)
        self.assertListEqual(expected_dependencies, dependencies)

    def _write_project_file(self, yml):
        path = self.temp_env.path_into(".asmm/config.yml")
        with open(path, 'w') as file:
            yaml.dump(yml, file)
