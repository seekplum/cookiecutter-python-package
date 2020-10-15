# -*- coding: utf-8 -*-

import os

import six

from invoke import task

root = os.path.dirname(os.path.abspath(__file__))
package_name = '{{cookiecutter.project_slug}}'


@task
def clean(ctx):
    """清除项目中无效文件
    """
    ctx.run('rm -rf build dist', echo=True)
    ctx.run("find . -name '*.pyc' -exec rm -f {} +", echo=True)
    ctx.run("find . -name '*.pyo' -exec rm -f {} +", echo=True)
    ctx.run("find . -name '__pycache__' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name 'htmlcov' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '.coverage*' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '.pytest_cache' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '.benchmarks' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '*.egg-info' -exec rm -rf {} +", echo=True)


@task(clean)
def sdist(ctx):
    ctx.run('python setup.py sdist', echo=True)


@task(clean)
def upload(ctx, name="private"):
    """上传包到指定pip源
    """
    ctx.run('python setup.py sdist upload -r %s' % name, echo=True)


@task(sdist)
def tupload(ctx, name="private"):
    """上传包到指定pip源
    """
    ctx.run('twine upload dist/* -r %s' % name, echo=True)


@task(clean)
def check(ctx, job=4):
    """检查代码规范
    """
    ctx.run("pylint --rcfile=.pylintrc -j %s --output-format parseable {{cookiecutter.project_slug}}" % job, echo=True)
    ctx.run("pylint --rcfile=.pylintrc -j %s --output-format parseable tests --ignore=test.py "
            "--disable=C0111,W0201,R0201" % job,
            echo=True)
    ctx.run("mypy {{cookiecutter.project_slug}}", echo=True)
    if six.PY3:
        ctx.run("black {{cookiecutter.project_slug}} --check", echo=True)
    ctx.run("isort --check-only {{cookiecutter.project_slug}}", echo=True)


@task(clean)
def unittest(ctx):
    """运行单元测试和计算测试覆盖率
    """
    ctx.run("export PYTHONPATH=`pwd` && pytest --cov={{cookiecutter.project_slug}} tests",
            encoding="utf-8",
            pty=True,
            echo=True)


@task(clean)
def coverage(ctx):
    """运行单元测试和计算测试覆盖率
    """
    ctx.run(
        "export PYTHONPATH=`pwd` && "
        "coverage run --source={{cookiecutter.project_slug}} -m pytest tests && "
        "coverage report -m",
        encoding="utf-8",
        pty=True,
        echo=True)


@task(clean)
def unittestone(ctx, source, test):
    """运行单元测试和计算测试覆盖率

    inv unittestone --source tests.demo --test tests/test_demo.py
    """
    ctx.run("export PYTHONPATH=`pwd` && "
            "pytest -vv -rsxS -q --cov-report term-missing --cov {source} {test}".format(source=source, test=test),
            encoding="utf-8",
            pty=True,
            echo=True)


@task(clean)
def coverageone(ctx, source, test):
    """运行单元测试和计算测试覆盖率

    inv coverageone --source tests.demo --test tests/test_demo.py
    """
    ctx.run("export PYTHONPATH=`pwd` && "
            "coverage run --source={source} -m pytest -vv -rsxS -q {test} && "
            "coverage report -m".format(source=source, test=test),
            encoding="utf-8",
            pty=True,
            echo=True)


@task(clean)
def format(ctx):
    """格式化代码
    """
    ctx.run(
        "autoflake --remove-all-unused-imports --recursive --remove-unused-variables "
        "--in-place {{cookiecutter.project_slug}} --exclude=__init__.py",
        echo=True)
    if six.PY3:
        ctx.run("black {{cookiecutter.project_slug}}", echo=True)
    ctx.run("isort --force-single-line-imports {{cookiecutter.project_slug}}", echo=True)


@task
def lock(ctx):
    """生成版本文件

    1.安装Pipenv

    pip install pipenv

    2.安装项目依赖包

    pipenv install --dev --skip-lock
    """
    ctx.run('if [ -f "Pipfile.lock" ]; then pipenv lock -v --keep-outdated ; else pipenv lock --pre --clear ; fi',
            echo=False)
