#!/bin/bash

OUTDIR="/tmp/out-cookiecutter"

function info() { echo -e "\033[34m[INFO]\033[0m $*"; }
function error() { echo -e "\033[31m[ERROR]\033[0m $*" >&2; }
function success() { echo -e "\033[32m[OK]\033[0m $*"; }

function parse_args() {
    project_name=""
    project_slug=""
    project_tag=""
    description=""
    pip_index_url=""
    debug=0
    author=seekplum
    email=1131909224m@sina.cn

    while [[ $# -gt 0 ]]; do
        case "$1" in
        --project-name)
            project_name="$2"
            shift 2
            ;;
        --project-slug)
            project_slug="$2"
            shift 2
            ;;
        --project-tag)
            project_tag="$2"
            shift 2
            ;;
        --description)
            description="$2"
            shift 2
            ;;
        --pip-index-url)
            pip_index_url="$2"
            shift 2
            ;;
        --email)
            email="$2"
            shift 2
            ;;
        --author)
            author="$2"
            shift 2
            ;;
        --debug)
            debug=1
            shift
            ;;
        *)
            error "未知选项: $1"
            exit 1
            ;;
        esac
    done

    if [[ -z "$project_name" ]]; then
        error "--project-name 是必填参数"
        exit 1
    fi

    project_slug="${project_slug:-$(echo "$project_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr '-' '_')}"
    project_tag="${project_tag:-${project_slug//_web/}}"
    project_slug_upper=$(echo "$project_slug" | tr '[:lower:]' '[:upper:]')
    build_version="\${${project_slug_upper}_BUILD_TAG}"
}

function run_cmd() {
    local cmd="$1"
    if [[ -z "$cmd" ]]; then
        error "run_cmd 需要传入命令"
        exit 1
    fi

    info "[DRY-RUN] $cmd"
    if [[ "$debug" -eq 0 ]]; then
        eval "$cmd"
    fi
}

function sd_replace() {
    local from="$1"
    local to="$2"
    if [[ -z "$from" ]]; then
        error "sd_replace 需要非空的搜索字符串"
        exit 1
    fi
    if [[ -z "$to" ]]; then
        error "sd_replace 需要非空的替换字符串"
        exit 1
    fi
    run_cmd "rg --hidden -g '!{.git,.venv,scaffold.sh,cookiecutter.json,test.sh,README.md}' -l -F '$from' | xargs sd -s '$from' '$to'"
}

function gen_project() {
    parse_args "$@"

    local cmd="cookiecutter . --no-input --output-dir $OUTDIR"
    cmd+=" project_name=${project_name}"
    cmd+=" project_slug=${project_slug}"
    cmd+=" project_tag=${project_tag}"
    [[ -n "$description" ]] && cmd+=" description='${description}'"
    [[ -n "$pip_index_url" ]] && cmd+=" pip_index_url=${pip_index_url}"
    cmd+=" author=${author}"
    cmd+=" email=${email}"
    cmd+=" python_version=3.13"
    cmd+=" version=0.0.1"
    cmd+=" use_github_ci=y use_drone_ci=n use_gitlab_ci=n"

    mkdir -p "$OUTDIR"
    if [[ -z "$project_name" || "$project_name" == "/" || "$project_name" == "." ]]; then
        error "project_name 不合法，中止删除操作"
        exit 1
    fi
    local target="$OUTDIR/$project_name"
    if [[ ! "$target" == "$OUTDIR"/* ]]; then
        error "目标路径不在 $OUTDIR 下，中止删除操作"
        exit 1
    fi
    rm -rf "$target"
    run_cmd "$cmd"
}

function restory_start_kit() {
    parse_args "$@"

    sd_replace "$project_name" "{{ cookiecutter.project_name }}"
    sd_replace "$project_slug" "{{ cookiecutter.project_slug }}"
    sd_replace "$project_tag" "{{ cookiecutter.project_tag }}"
    [[ -n "$description" ]] && sd_replace "$description" "{{ cookiecutter.description }}"
    [[ -n "$pip_index_url" ]] && sd_replace "$pip_index_url" "{{ cookiecutter.pip_index_url }}"
    sd_replace "$author" "{{ cookiecutter.author }}"
    sd_replace "$email" "{{ cookiecutter.email }}"
    sd_replace "{{{\"" "{% raw %}{{{{% endraw %}\""
    sd_replace "$build_version" '{% raw %}${{% endraw %}{{ cookiecutter.project_slug.upper() }}_BUILD_TAG{% raw %}}{% endraw %}'
}

case "$1" in
"gen")
    shift
    gen_project "$@"
    ;;
"restore")
    shift
    restory_start_kit "$@"
    ;;
*)
    cat <<EOF
用法: $0 {gen|restore} [选项]

子命令:
  gen       基于 cookiecutter 模板生成新项目
  restore   将已有项目还原为 cookiecutter 模板占位符

选项:
  --project-name  <name>   项目名称（必填）
  --project-slug  <slug>   项目标识，默认由 project-name 转换（小写、空格和连字符转下划线）
  --project-tag   <tag>    项目标签，默认由 project-slug 去掉 _web 后缀
  --description   <desc>   项目描述
  --pip-index-url <url>    pip 镜像源地址
  --author        <author> 作者，默认 seekplum
  --email         <email>  邮箱地址，默认 1131909224m@sina.cn
  --debug                  仅打印命令，不实际执行

示例:
  $0 gen --project-name "plum-tools"
  $0 restore --project-name "plum-tools"
EOF
    exit 1
    ;;
esac
