"""Manages the dependencies of a project
"""
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
