## 目的

快速创建 python 模块包

## 如何使用

- 1.安装依赖

```bash
pip install copier jinja2-time
```

> 模板中使用了 `jinja2_time.TimeExtension`（unsafe 特性），生成项目时需要加 `--trust`，
> 并保证 `jinja2-time` 与 copier 安装在同一个 Python 环境中。

- 2.根据提示生成项目目录

```bash
copier copy --trust https://github.com/seekplum/cookiecutter-python-package.git ./new-project


# or
git clone https://github.com/seekplum/cookiecutter-python-package.git
copier copy --trust cookiecutter-python-package ./new-project
```

- 3.批量传入参数（无交互），例如：

```bash
copier copy --trust --defaults \
  -d project_name=plum-tools \
  -d version=0.4.1 \
  https://github.com/seekplum/cookiecutter-python-package.git ./plum-tools
```

## 常用命令

- 生成示例项目并校验模板

```bash
./scaffold.sh gen --outdir /tmp/out-copier --project-name "plum-tools" --version "0.4.1"
```

## 模板结构

```text
├── copier.yml       # copier 配置：问题、默认值、排除规则
├── scaffold.sh      # 基于 copier 生成新项目 / 将项目还原为模板
└── template         # 模板内容
    ├── pyproject.toml.jinja
    ├── README.md.jinja
    ├── src/{{ project_slug }}/
    └── ...           # 需要渲染的文件以 .jinja 结尾，其余文件原样复制
```

## 模板与项目同步

copier 的同步是**单向**的：模板是唯一事实来源，官方只支持 模板→项目；反向（项目→模板）使用本仓库的 `scaffold.sh restore`。

### 模板 → 项目（copier 原生）

前提条件：
1. 项目根目录有有效的 `.copier-answers.yml`
2. 模板是带 git tag 的仓库（按 PEP 440 排序，默认取最新 tag）
3. 项目是 git 仓库，且 `git status` 干净

```bash
cd ./new-project
copier check-update                                        # 检查是否有更新
copier update --trust --defaults --vcs-ref=HEAD                    # 更新到模板最新提交，复用旧答案
copier update --trust --defaults --data 'project_name=my-project'  # 复用旧答案，只改一个问题的值
```

其他说明：
- 冲突时默认写入 git 风格冲突标记（`--conflict inline`），也可用 `--conflict rej` 生成 `.rej` 文件；更新后需人工 review 冲突再提交。
- 更新失败可 `copier recopy --trust` 兜底：丢弃智能 diff，按最新模板整体重放，仅保留答案。
- **绝不要手工修改 `.copier-answers.yml`**，否则会导致更新算法产生不可预期行为。
- 项目内被删除的模板文件，更新时自动排除；想找回可 `copier recopy --trust`。

### 项目 → 模板（`scaffold.sh restore`）

```bash
./scaffold.sh restore \
  --project-dir ~/path/to/plum-tools \
  --project-name "plum-tools" \
  --version "0.4.1"
```

流程：将项目文件同步回 `template/`，从 `.copier-answers.yml` 解析答案把具体值替换回 `{{ }}` 占位符，GitHub 表达式 `${{...}}` 转义为 `{% raw %}${{...}}{% endraw %}`，含占位符的文件加上 `.jinja` 后缀。
