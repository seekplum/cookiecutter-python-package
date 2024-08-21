# {{ cookiecutter.description }}

[![LICENSE](https://img.shields.io/github/license/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}.svg)](https://github.com/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}/blob/master/LICENSE)[![coveralls](https://coveralls.io/repos/github/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}/badge.svg?branch=master)](https://coveralls.io/github/{{ cookiecutter.author }}/{{ cookiecutter.project_name }}?branch=master) [![pypi version](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_name }}) [![pyversions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_name }})

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

1.安装 invoke

```bash
pip install invoke
```

2.安装项目依赖环境

```bash
inv install --dev
```

3.安装 Git hooks

由于钩子文件无法提交到 `.git` 中，所以在第一次 clone 项目中需要执行以下命令，把钩子放到指定位置，有两种方式，建议使用第一种

第一种

```bash
pre-commit install -t pre-commit
pre-commit install -t pre-push
```

第二种

```bash
cp -r hooks/* .git/hooks/
```

## 运行单元测试

### 第一种

```bash
inv coverage
```

### 第二种

```bash
inv test
```

## 检查 Python 代码规范

```bash
inv lint
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
