from multiprocessing import cpu_count
from typing import Any, Optional

from invoke import task
from invoke.context import Context

PACKAGE_NAME = "."


def get_source(source: Optional[str] = None, *, ignote_tasks: bool = False) -> str:
    if not source:
        source = PACKAGE_NAME
        if not ignote_tasks:
            source += " tasks.py"
    return source


def ctx_run(ctx: Context, cmd: str, **kwargs: Any) -> None:
    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault("echo", True)
    kwargs.setdefault("pty", True)
    ctx.run(cmd, **kwargs)


@task
def clean_pyc(ctx: Context) -> None:
    """清理 Python 运行文件"""
    ctx_run(ctx, "rm -rf build dist")
    ctx_run(ctx, "find . -name '*.pyc' -exec rm -f {} +")
    ctx_run(ctx, "find . -name '*.pyo' -exec rm -f {} +")
    ctx_run(ctx, "find . -name '*~' -exec rm -f {} +")
    ctx_run(ctx, "find . -name '*.log' -exec rm -f {} +")
    ctx_run(ctx, "find . -name '*.log.*' -exec rm -f {} +")
    ctx_run(ctx, "find . -name '__pycache__' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name '.mypy_cache' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name '.ruff_cache' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name '*.egg-info' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name '.DS_Store' -exec rm -rf {} +")


@task
def clean_test(ctx: Context) -> None:
    """清理测试文件"""
    ctx_run(ctx, "find . -name '.pytest_cache' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name '.coverage' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name 'pytest_coverage*.xml' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name 'pytest_result*.xml' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name 'htmlcov' -exec rm -rf {} +")
    ctx_run(ctx, "find . -name '.benchmarks' -exec rm -rf {} +")


@task(clean_pyc, clean_test)
def clean(_: Context) -> None:
    """清理所有不该进代码库的文件"""


@task
def format(
    ctx: Context, source: Optional[str] = None
) -> None:  # pylint: disable=redefined-builtin
    """格式化代码

    inv format --source tasks.py
    """
    source = get_source(source)
    autoflake_args = [
        "--remove-all-unused-imports",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
        "--exclude=__init__.py",
    ]
    args = " ".join(autoflake_args)
    ctx_run(ctx, f"autoflake {args} {source}")
    ctx_run(ctx, f"isort {source}")
    ctx_run(ctx, f"black {source}")


@task
def lint(ctx: Context, source: Optional[str] = None) -> None:
    """检查代码规范

    inv lint --source tasks.py
    """
    source = get_source(source)
    ctx_run(ctx, f"mypy {source}")
    ctx_run(ctx, f"black --check {source}")
    ctx_run(ctx, f"isort --check-only --diff {source}")
    ctx_run(ctx, f"flake8 {source}")
    ctx_run(ctx, f"pylint {source} --job {cpu_count()}")
    ctx_run(ctx, f"bandit -c pyproject.toml -r {source}")
