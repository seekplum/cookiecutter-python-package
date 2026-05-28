# -*- coding: utf-8 -*-
"""Post generation script"""

from __future__ import print_function

import os
import shutil
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(file_path: str) -> None:
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
    check_file_required("{{ cookiecutter.use_drone_ci }}", ".drone.yml")
    check_file_required("{{ cookiecutter.use_github_ci }}", ".github")
    remove_file(".github/workflows/publish-docker.yml")


def fix_readme_placeholders() -> None:
    readme_path = Path(PROJECT_DIRECTORY) / "README.md"
    if not readme_path.is_file():
        return

    content = readme_path.read_text(encoding="utf-8")
    content = content.replace("{% raw %}{{ cookiecutter.project_name }}{% endraw %}", "{{ cookiecutter.project_name }}")
    content = content.replace("{% raw %}{{ cookiecutter.description }}{% endraw %}", "{{ cookiecutter.description }}")
    readme_path.write_text(content, encoding="utf-8")


def main() -> None:
    remove_files()
    fix_readme_placeholders()


if __name__ == '__main__':
    main()
