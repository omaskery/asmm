"""
This module assembles missions based on the missions and
test_missions folders, the resulting missions are placed
in the appropriate build/missions or build/test_missions
folders. During this process the contents of the assets
folder is merged into each mission, as well as the assets
folder of each dependency.
"""
import shutil
import os


def build(target_directory):
    """
    Builds the project specified by the given directory
    :param target_directory: directory of the project to build
    """

    def _tgt_dir(path):
        return os.path.join(target_directory, path)

    build_dir = _tgt_dir("build")
    assets_dir = _tgt_dir("assets")

    os.makedirs(build_dir, exist_ok=True)
    for mission_kind in ["missions", "test_missions"]:
        mission_dir = _tgt_dir(mission_kind)
        missions = _list_folders_in(mission_dir)
        for mission in missions:
            src_path = os.path.join(mission_dir, mission)
            dst_path = os.path.join(build_dir, mission_kind, mission)
            _build_mission(assets_dir, src_path, dst_path)


def _build_mission(assets_dir, src_path, dst_path):
    """
    Builds a single mission by combining a template and the shared assets
    :param assets_dir: folder of shared assets to merge into the template
    :param src_path: folder to initially clone as a template
    :param dst_path: folder to create, containing the final mission
    """

    if os.path.isdir(dst_path):
        shutil.rmtree(dst_path)
    shutil.copytree(src_path, dst_path)
    _merge_folders(assets_dir, dst_path)


def _merge_folders(src_folder, dst_folder):
    """
    Takes files from the source directory and copies them into the
    destination directory
    :param src_folder: source directory to copy from
    :param dst_folder: target directory to copy into
    """

    for root_dir, folders, files in os.walk(src_folder):
        path_relative_to_assets = os.path.relpath(root_dir, src_folder)
        path_into_dst = os.path.join(dst_folder, path_relative_to_assets)
        os.makedirs(path_into_dst, exist_ok=True)

        for file in files:
            src_file_path = os.path.join(root_dir, file)
            dst_file_path = os.path.join(path_into_dst, file)
            shutil.copy(src_file_path, dst_file_path)


def _list_folders_in(path):
    """
    Lists folders in the specified directory
    :param path: directory to list folders in
    :return: a list of folder names in the specified directory
    """

    return [
        entry_name
        for entry_name in os.listdir(path)
        if os.path.isdir(os.path.join(path, entry_name))
    ]
