import json
import os

import git

from common import file, console

new_data_version = 3
new_env_version = 1
current_data_version = 3
current_env_version = 1
if not os.path.exists("./upgrade/current_version.json"):
    file.write_file("./upgrade/current_version.json",
                    json.dumps({"current_data_version": new_data_version, "current_env_version": new_env_version}))
current_version_json = json.loads(file.read_file("./upgrade/current_version.json"))
current_data_version = current_version_json["current_data_version"]
if "current_env_version" in current_version_json:
    current_env_version = current_version_json["current_env_version"]


def git_init():
    repo = git.Repo("./")
    remote = repo.remote()
    return repo, remote


def upgrade_check(fetch=True):
    if not os.path.exists("./.git"):
        if fetch:
            console.log("Error", "Not a git repository.")
        return False
    repo, remote = git_init()
    if fetch:
        remote.fetch(repo.active_branch)
        try:
            if repo.rev_parse("HEAD") != repo.rev_parse("FETCH_HEAD"):
                return True
        except:
            pass
        if current_data_version != new_data_version:
            return True
    return False

def upgrade_pull():
    if not os.path.exists("./.git"):
        console.log("Error", "Not a git repository.")
        return False
    repo, remote = git_init()
    console.log("Info", "On branch {}".format(repo.active_branch))
    if repo.is_dirty():
        console.log("Error",
                    "The current warehouse is modified and can not be upgraded automatically.")
        checkout_repo = input('Do you want to restore these changes? [y/N]')
        if checkout_repo.lower() == 'yes' or checkout_repo.lower() == 'y':
            repo.index.checkout(force=True)
        if repo.is_dirty():
            exit(1)
    remote.pull()
    if current_env_version != new_env_version:
        os.system("cd ./install && bash install_python_dependency.sh")
        file.write_file("./upgrade/current_version.json",
                        json.dumps({"current_data_version": new_data_version, "current_env_version": new_env_version}))
    if current_data_version != new_data_version and os.path.exists(
            "./upgrade/upgrade_from_{}.py".format(current_data_version)):
        os.system("python3 ./upgrade/upgrade_from_{}.py".format(current_data_version))
        file.write_file("./upgrade/current_version.json",
                        json.dumps({"current_data_version": new_data_version, "current_env_version": new_env_version}))
    console.log("Success", "Upgrade Successful!")
    exit(0)
