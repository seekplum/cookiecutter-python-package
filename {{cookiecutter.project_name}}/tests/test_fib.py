# -*- coding: utf-8 -*-
"""
#=============================================================================
#  ProjectName: {{cookiecutter.project_name}}
#     FileName: fib.py
#       Author: {{ cookiecutter.author }}
#        Email: huangjiandong95@sina.com
#=============================================================================
"""

import pytest

from {{ cookiecutter.project_slug }}.fib import fib


@pytest.mark.parametrize("n, result", [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
])
def test_fib(n, result):
    assert fib(n) == result
