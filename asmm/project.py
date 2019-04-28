"""
Utilities for manipulating a project file
"""

from dataclasses import dataclass
import yaml


@dataclass
class Project:
    """In memory representation of a project file
    """

    def __init__(self):
        self.dependencies = []


def serialise(project):
    """Serialise a project into a python dict
    :param project: project to serialise
    :return: python dict of object
    """

    return {
        "dependencies": project.dependencies,
    }


def deserialise(project_dict):
    """Deserialise a python dict into a project object
    :param project_dict: dictionary to turn into project object
    :return: project object build from dictionary
    """

    p = Project()
    p.dependencies = project_dict["dependencies"]
    return p


def save_project(project, path):
    """Save a project object to a YAML file at specified path
    :param project: project to save
    :param path: path to YAML file to save project to
    """
    with open(path, 'w') as file:
        yaml.dump(serialise(project), file)


def load_project(path):
    """Load a project object from a YAML file at specified path
    :param path: path to YAML file to load project from
    :return: loaded project object
    """

    with open(path) as file:
        return deserialise(yaml.load(file, Loader=yaml.SafeLoader))
