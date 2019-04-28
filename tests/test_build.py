import unittest


from tests.temp_env import TempEnv
import asmm


class TestBuild(unittest.TestCase):

    def setUp(self):
        self.temp_env = TempEnv(self)
        asmm.initialise(self.temp_env.name)

    def tearDown(self):
        self.temp_env.cleanup()

    def test_build_doesnt_crash(self):
        asmm.build(self.temp_env.name)

    def test_build_folder_created(self):
        asmm.build(self.temp_env.name)
        self.temp_env.assert_folder_exists("build")

    def test_mission_folders_created(self):
        self.temp_env.make_dirs("missions/mission1")
        self.temp_env.make_file("missions/mission1/mission.sqm")
        self.temp_env.make_dirs("missions/mission2")
        self.temp_env.make_file("missions/mission2/mission.sqm")
        asmm.build(self.temp_env.name)
        self.temp_env.assert_folder_exists("build")
        self.temp_env.assert_folder_exists("build/missions/mission1")
        self.temp_env.assert_file_exists("build/missions/mission1/mission.sqm")
        self.temp_env.assert_folder_exists("build/missions/mission2")
        self.temp_env.assert_file_exists("build/missions/mission2/mission.sqm")

    def test_test_mission_folders_created(self):
        self.temp_env.make_dirs("test_missions/mission1")
        self.temp_env.make_file("test_missions/mission1/mission.sqm")
        self.temp_env.make_dirs("test_missions/mission2")
        self.temp_env.make_file("test_missions/mission2/mission.sqm")
        asmm.build(self.temp_env.name)
        self.temp_env.assert_folder_exists("build")
        self.temp_env.assert_folder_exists("build/test_missions/mission1")
        self.temp_env.assert_file_exists("build/test_missions/mission1/mission.sqm")
        self.temp_env.assert_folder_exists("build/test_missions/mission2")
        self.temp_env.assert_file_exists("build/test_missions/mission2/mission.sqm")

    def test_assets_copied_to_missions(self):
        self.temp_env.make_dirs("missions/mission")
        self.temp_env.make_file("missions/mission/mission.sqm")
        self.temp_env.make_file("assets/asset1.sqf", content="asset1")
        self.temp_env.make_dirs("assets/subdir")
        self.temp_env.make_file("assets/subdir/asset2.sqf", content="asset2")
        asmm.build(self.temp_env.name)
        self.temp_env.assert_file_exists("build/missions/mission/asset1.sqf", with_content="asset1")
        self.temp_env.assert_file_exists("build/missions/mission/subdir/asset2.sqf", with_content="asset2")

    def test_assets_copied_to_test_missions(self):
        self.temp_env.make_dirs("test_missions/mission")
        self.temp_env.make_file("test_missions/mission/mission.sqm")
        self.temp_env.make_file("assets/asset1.sqf", content="asset1")
        self.temp_env.make_dirs("assets/subdir")
        self.temp_env.make_file("assets/subdir/asset2.sqf", content="asset2")
        asmm.build(self.temp_env.name)
        self.temp_env.assert_file_exists("build/test_missions/mission/asset1.sqf", with_content="asset1")
        self.temp_env.assert_file_exists("build/test_missions/mission/subdir/asset2.sqf", with_content="asset2")
