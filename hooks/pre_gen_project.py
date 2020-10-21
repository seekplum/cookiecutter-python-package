# -*- coding: utf-8 -*-
"""Pre generation script"""

from __future__ import print_function
import os
import re
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

MODULE_REGEX = r"^[a-zA-Z][_a-zA-Z0-9]+$"
module_names = ["{{ cookiecutter.project_slug }}"]

for module_name in module_names:
    if not re.match(MODULE_REGEX, module_name):
        print("ERROR: %s is not a valid Python module name!" % module_name)
        sys.exit(1)
