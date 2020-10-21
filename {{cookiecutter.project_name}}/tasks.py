# -*- coding: utf-8 -*-

import os

from invoke import task

root = os.path.dirname(os.path.abspath(__file__))
package_name = "{{cookiecutter.project_slug}}"


@task
def clean(ctx):
    """清除项目中无效文件
    """
    ctx.run("rm -rf build dist", echo=True)
    ctx.run("find . -name '*.pyc' -exec rm -f {} +", echo=True)
    ctx.run("find . -name '*.pyo' -exec rm -f {} +", echo=True)
    ctx.run("find . -name '__pycache__' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name 'htmlcov' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '.coverage' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '.pytest_cache' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '.benchmarks' -exec rm -rf {} +", echo=True)
    ctx.run("find . -name '*.egg-info' -exec rm -rf {} +", echo=True)


@task(clean)
def sdist(ctx):
    ctx.run("python setup.py sdist", echo=True)


@task(clean)
def upload(ctx, name="private"):
    """上传包到指定pip源
    """
    ctx.run("python setup.py sdist upload -r %s" % name, echo=True)


@task(sdist)
def tupload(ctx, name="private"):
    """上传包到指定pip源
    """
    ctx.run("twine upload dist/* -r %s" % name, echo=True)


@task(clean)
def check(ctx, job=4):
    """检查代码规范
    """
    ctx.run("isort --check-only --diff {{cookiecutter.project_slug}}", echo=True)
    {% if cookiecutter.python_version[0] == "3" %}ctx.run("black --check {{cookiecutter.project_slug}}", echo=True){% endif %}
    {% if cookiecutter.use_pylint.lower() in ("y", "yes") %}ctx.run("pylint --rcfile=.pylintrc -j %s --output-format parseable {{cookiecutter.project_slug}}" % job, echo=True)
    ctx.run("pylint --rcfile=.pylintrc -j %s --output-format parseable tests --ignore=test.py "
            "--disable=C0111,W0201,R0201" % job,
            echo=True)
    {% else %}ctx.run("flake8 {{cookiecutter.project_slug}}", echo=True){% endif %}
    ctx.run("mypy {{cookiecutter.project_slug}}", echo=True)


@task(clean)
def unittest(ctx):
    """运行单元测试和计算测试覆盖率

    pytest --cov-config=.coveragerc --cov={{cookiecutter.project_slug}} --cov-fail-under=100 tests
    """
    ctx.run(
        "export PYTHONPATH=`pwd` && pytest tests", encoding="utf-8", pty=True, echo=True
    )


@task(clean)
def coverage(ctx):
    """运行单元测试和计算测试覆盖率
    """
    ctx.run(
        "export PYTHONPATH=`pwd` && "
        "coverage run --rcfile=.coveragerc --source={{cookiecutter.project_slug}} -m pytest tests && "
        "coverage report -m --fail-under=100",
        encoding="utf-8",
        pty=True,
        echo=True,
    )


@task(clean)
def unittestone(ctx, source, test):
    """运行单元测试和计算测试覆盖率

    inv unittestone --source {{cookiecutter.project_slug}}.fib --test tests/test_fib.py
    """
    ctx.run(
        "export PYTHONPATH=`pwd` && "
        "pytest -vv -rsxS -q --cov-config=.coveragerc --cov-report term-missing "
        "--cov --cov-fail-under=100 {source} {test}".format(source=source, test=test),
        encoding="utf-8",
        pty=True,
        echo=True,
    )


@task(clean)
def coverageone(ctx, source, test):
    """运行单元测试和计算测试覆盖率

    inv coverageone --source {{cookiecutter.project_slug}}.fib --test tests/test_fib.py
    """
    ctx.run(
        "export PYTHONPATH=`pwd` && "
        "coverage run --rcfile=.coveragerc --source={source} -m pytest -vv -rsxS -q {test} && "
        "coverage report -m".format(source=source, test=test),
        encoding="utf-8",
        pty=True,
        echo=True,
    )


@task(clean)
def format(ctx):
    """格式化代码
    """
    autoflake_args = [
        "--remove-all-unused-imports",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
        "--exclude=__init__.py",
    ]
    ctx.run(
        "autoflake {args} {{cookiecutter.project_slug}}".format(args=" ".join(autoflake_args)),
        echo=True,
    )
    ctx.run("isort {{cookiecutter.project_slug}}", echo=True)
    {% if cookiecutter.python_version[0] == "3" %}ctx.run("black {{cookiecutter.project_slug}}", echo=True){% endif %}


@task(clean)
def formatone(ctx, source):
    """格式化单个文件
    """
    autoflake_args = [
        "--remove-all-unused-imports",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
    ]
    ctx.run(
        "autoflake {args} {source}".format(source=source, args=" ".join(autoflake_args)),
        echo=True,
    )
    ctx.run("isort {source}".format(source=source), echo=True)
    {% if cookiecutter.python_version[0] == "3" %}ctx.run("black {source}".format(source=source), echo=True){% endif %}


@task
def lock(ctx):
    """生成版本文件

    1.安装Pipenv

    pip install pipenv

    2.安装项目依赖包

    pipenv install --deploy --dev --skip-lock
    """
    ctx.run(
        'if [ -f "Pipfile.lock" ]; then pipenv lock -v --keep-outdated ; else pipenv lock --pre --clear ; fi',
        echo=False,
    )
