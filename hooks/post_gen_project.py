# -*- coding: utf-8 -*-
"""Post generation script"""

from __future__ import print_function

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(file_path: str) -> None:
    """
    Remove a file with the given path.

    :param file_path Path of the file.
    :type file_path str
    """
    file_path = os.path.join(PROJECT_DIRECTORY, file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        shutil.rmtree(file_path)


def check_file_required(option: str, file_path: str) -> None:
    if option.lower() in ("y", "yes"):
        return
    remove_file(file_path)


def remove_files() -> None:
    check_file_required("{{ cookiecutter.use_gitlab_ci }}", ".gitlab-ci.yml")
    check_file_required("{{ cookiecutter.use_github_ci }}", ".github")


def main() -> None:
    remove_files()


if __name__ == "__main__":
    main()
