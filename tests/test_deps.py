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

    def test_add_dependency(self):
        self._write_project_file({
            "dependencies": []
        })
        asmm.add_dependency(self.temp_env.name, "test-dependency")
        project = self._read_project_file()
        self.assertListEqual(project["dependencies"], ["test-dependency"])

    def test_add_multiple_dependencies(self):
        self._write_project_file({
            "dependencies": []
        })
        asmm.add_dependency(self.temp_env.name, "first-dependency")
        asmm.add_dependency(self.temp_env.name, "second-dependency")
        project = self._read_project_file()
        self.assertListEqual(project["dependencies"], ["first-dependency", "second-dependency"])

    def test_add_repeated_dependencies_should_fail(self):
        self._write_project_file({
            "dependencies": []
        })
        asmm.add_dependency(self.temp_env.name, "dep")
        with self.assertRaises(asmm.AsmmError):
            asmm.add_dependency(self.temp_env.name, "dep")

    def test_remove_dependency(self):
        self._write_project_file({
            "dependencies": ["one", "two", "three"]
        })
        asmm.remove_dependency(self.temp_env.name, "two")
        project = self._read_project_file()
        self.assertListEqual(project["dependencies"], ["one", "three"])

    def test_remove_non_existant_dependency_should_fail(self):
        self._write_project_file({
            "dependencies": []
        })
        with self.assertRaises(asmm.AsmmError):
            asmm.remove_dependency(self.temp_env.name, "not-existant")

    def _write_project_file(self, yml):
        path = self.temp_env.path_into(".asmm/config.yml")
        with open(path, 'w') as file:
            yaml.dump(yml, file)

    def _read_project_file(self):
        path = self.temp_env.path_into(".asmm/config.yml")
        with open(path) as file:
            return yaml.load(file, Loader=yaml.SafeLoader)
