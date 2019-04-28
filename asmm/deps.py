import os


from .project import load_project


def list_dependencies(target_directory):
    project_file_path = os.path.join(target_directory, ".asmm/config.yml")
    project = load_project(project_file_path)
    return project.dependencies
