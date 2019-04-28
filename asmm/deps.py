import os


from .project import load_project, save_project
from .exception import AsmmError


def add_dependency(target_directory, dependency):
    project_file_path = os.path.join(target_directory, ".asmm/config.yml")
    project = load_project(project_file_path)
    if dependency in project.dependencies:
        raise AsmmError(f"project already has dependency '{dependency}'")
    project.dependencies.append(dependency)
    save_project(project, project_file_path)


def list_dependencies(target_directory):
    project_file_path = os.path.join(target_directory, ".asmm/config.yml")
    project = load_project(project_file_path)
    return project.dependencies
