# {{ cookiecutter.description }}

[![LICENSE](https://img.shields.io/github/license/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}.svg)](https://github.com/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}/blob/master/LICENSE)[![travis-ci](https://travis-ci.org/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}.svg?branch=master)](https://travis-ci.org/{{ cookiecutter.author }}/{{ cookiecutter.project_name }})[![coveralls](https://coveralls.io/repos/github/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}/badge.svg?branch=master)](https://coveralls.io/github/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}?branch=master) [![pypi version](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_name }}) [![pyversions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_name }})

## 项目的git hooks

由于钩子文件无法提交到 `.git` 中，所以在第一次clone项目中需要执行以下命令，把钩子放到指定位置

```bash
cp -r hooks/* .git/hooks/
```

## 目录结构


```text
➜  tree -L 1 -a
.
├── .bumpversion.cfg    # `bumpversion`工具的配置文件，用于自动更新版本
├── .env                # 环境变量配置,`不会提交到gitlab中`
├── .gitignore          # 维护git仓库需要忽略文件
├── .gitlab-ci.yml      # gitlab ci的配置文件
├── .pylintrc           # pylint 配置文件
├── CHANGELOG.md        # 记录模块的变化
├── MANIFEST.in         # 打包时添加文件或移除文件等的配置
├── Pipfile             # python依赖包版本文件
├── Pipfile.lock        # 根据Pipfile生成的版本锁文件
├── README.md           # 项目自述文件
├── VERSION             # 项目版本文件
├── bin                 # 项目二进制程序
├── docs                # 项目文档
├── {{cookiecutter.project_name}}          # 核心代码模块
├── setup.cfg           # 安装配置文件
├── setup.py            # 安装脚本
├── tasks.py            # 任务执行脚本
└── tests               # 单元测试目录

```

## 安装环境依赖

1.安装pipenv

```bash
pip install pipenv
```

2.安装项目依赖环境

```bash
pipenv --two install --deploy # py2
pipenv --three install --deploy # py3
```

## 运行单元测试

首先需要进入我们安装的虚拟环境

```bash
pipenv shell
```

### 第一种

```bash
inv coverage
```

### 第二种

```bash
inv unittest
```

## 检查Python代码规范

```bash
inv check
```

## 详细文档

见[项目文档目录](docs/README.md)
