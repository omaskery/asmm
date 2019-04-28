"""Manages the dependencies of a project
"""
import urllib.parse
import hashlib
import shutil
import os


from .project import load_project, save_project
from .exception import AsmmError


def add_dependency(target_directory, dependency):
    """
    Add a dependency to the project as a URI to another project
    :param target_directory: directory of the project to modify with new dependency
    :param dependency: URI of project to treat as a dependency
    """
    project_file_path = os.path.join(target_directory, ".asmm/config.yml")
    project = load_project(project_file_path)
    if dependency in project.dependencies:
        raise AsmmError(f"project already has dependency '{dependency}'")
    project.dependencies.append(dependency)
    save_project(project, project_file_path)


def list_dependencies(target_directory):
    """
    Lists the dependencies of the current project
    :param target_directory: path to the directory of the current project
    :return: a list of dependency URIs
    """
    project_file_path = os.path.join(target_directory, ".asmm/config.yml")
    project = load_project(project_file_path)
    return project.dependencies


def remove_dependency(target_directory, dependency):
    """
    Removes a dependency from the project
    :param target_directory: directory of the project to modify
    :param dependency: URI of project dependency to remove
    """
    project_file_path = os.path.join(target_directory, ".asmm/config.yml")
    project = load_project(project_file_path)
    if dependency not in project.dependencies:
        raise AsmmError(f"project has no dependency '{dependency}'")
    project.dependencies.remove(dependency)
    save_project(project, project_file_path)


def sync_dependencies(target_directory, force_all=False):
    """
    Retrieves dependencies from their specified URIs and populates the dependency cache
    :param target_directory: directory of the project to fetch dependencies of
    :param force_all: when set, retrieves all dependencies, otherwise only fetches those not in the cache
    """
    cache_dir = os.path.join(target_directory, ".asmm/cache/deps")
    to_update = list_dependencies(target_directory)
    if not force_all:
        cached_dependencies = os.listdir(cache_dir)
        to_update = [
            dependency for dependency in to_update
            if _dependency_to_cache_name(dependency) not in cached_dependencies
        ]

    while len(to_update) > 0:
        dependency = to_update.pop(0)
        _fetched_dependency = _fetch_dependency(target_directory, cache_dir, dependency)
        # TODO: used fetched dependency to recurse


def _fetch_dependency(target_directory, cache_dir, dependency):
    """
    Retrieves a single dependency via its URI and stores it in the cache
    :param target_directory: directory of the project currently being updated
    :param cache_dir: directory to store cached dependencies in
    :param dependency:
    :return:
    """
    dep_cache_name = _dependency_to_cache_name(dependency)
    target_folder = os.path.join(cache_dir, dep_cache_name)
    uri = urllib.parse.urlsplit(dependency)

    # handle local filesystem URIs
    if uri.scheme == "":
        if os.path.isabs(uri.path):
            filepath = uri.path
        else:
            # FIXME: these relative filepaths are going to really screw with recursive dependencies
            filepath = os.path.join(target_directory, uri.path)
        shutil.copytree(filepath, target_folder)

    # don't handle other URI kinds
    else:
        raise AsmmError(f"unsupported URI scheme '{uri.scheme}'")

    return target_folder


def _dependency_to_cache_name(dependency):
    return hashlib.sha256(dependency.encode()).hexdigest()
