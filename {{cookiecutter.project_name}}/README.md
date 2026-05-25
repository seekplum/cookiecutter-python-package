# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

[![LICENSE](https://img.shields.io/github/license/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}.svg)](https://github.com/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}/blob/master/LICENSE)[![coveralls](https://coveralls.io/repos/github/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}/badge.svg?branch=master)](https://coveralls.io/github/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}?branch=master) [![pypi version](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_name }}) [![pyversions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_name }})

## 目录结构

```text
➜  tree -L 1 -a
.
├── .bumpversion.cfg    # `bumpversion`工具的配置文件，用于自动更新版本
├── .gitignore          # 维护git仓库需要忽略文件
├── .gitlab-ci.yml      # gitlab ci的配置文件
├── .pylintrc           # pylint 配置文件
├── CHANGELOG.md        # 记录模块的变化
├── README.md           # 项目自述文件
├── bin                 # 项目二进制程序
├── docs                # 项目文档
├── {{cookiecutter.project_name}}          # 核心代码模块
└── tests               # 单元测试目录

```

## 安装环境依赖

1.安装 [uv](https://github.com/astral-sh/uv)

```bash
# 推荐
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或
pip install uv
```

2.安装项目依赖环境

```bash
uv sync
```


## 运行单元测试

```bash
uv run poe test
```

## 检查 Python 代码规范

```bash
uv run poe lint
```

## 更新版本

```bash
# 小版本
bumpversion patch

# 中版本
bumpversion minor
```

## 详细文档

见[项目文档目录](docs/README.md)
