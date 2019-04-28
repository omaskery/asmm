import yaml
import os


def initialise(target_directory):
    os.makedirs(target_directory, exist_ok=True)
    asmm_folder = os.path.join(target_directory, ".asmm")
    os.makedirs(asmm_folder, exist_ok=True)
    os.makedirs(os.path.join(target_directory, "missions"), exist_ok=True)
    os.makedirs(os.path.join(target_directory, "test_missions"), exist_ok=True)
    os.makedirs(os.path.join(target_directory, "assets"), exist_ok=True)
    os.makedirs(os.path.join(asmm_folder, "cache/deps"), exist_ok=True)
    project = {
        "dependencies": []
    }

    with open(os.path.join(asmm_folder, "config.yml"), "w") as project_file:
        yaml.dump(project, project_file)
