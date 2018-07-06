#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Post generation script"""

import os


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(file_path):
    """
    Remove a file with the given path.

    :param file_path Path of the file.
    :type file_path str
    """
    os.remove(os.path.join(PROJECT_DIRECTORY, file_path))


if __name__ == '__main__':
    if '{{ cookiecutter.use_bumpversion }}'.lower() in ('n', 'no'):
        remove_file('.bumpversion.cfg')

    if '{{ cookiecutter.use_pytest }}'.lower() in ('n', 'no'):
        remove_file('pytest.ini')
