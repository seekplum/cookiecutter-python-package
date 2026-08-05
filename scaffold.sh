#!/bin/bash

KIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$KIT_ROOT/template"

function info() { echo -e "\033[34m[INFO]\033[0m $*"; }
function error() { echo -e "\033[31m[ERROR]\033[0m $*" >&2; }
function success() { echo -e "\033[32m[OK]\033[0m $*"; }

function parse_args() {
    out_dir=""
    project_name=""
    project_slug=""
    project_tag=""
    description=""
    pip_index_url=""
    version=""
    debug=0
    author=seekplum
    email=1131909224m@sina.cn

    while [[ $# -gt 0 ]]; do
        case "$1" in
        --outdir)
            out_dir="$2"
            shift 2
            ;;
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
        --version)
            version="$2"
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

function require_copier() {
    if ! command -v copier >/dev/null 2>&1; then
        error "未找到 copier，请先安装: pip install copier jinja2-time"
        exit 1
    fi
}

function require_command() {
    local command_name="$1"
    if ! command -v "$command_name" >/dev/null 2>&1; then
        error "未找到 $command_name，无法还原模板"
        exit 1
    fi
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

    local file
    while IFS= read -r -d '' file; do
        if [[ "$debug" -eq 1 ]]; then
            info "[DRY-RUN] sd -s '$from' '$to' '$file'"
        else
            sd -s "$from" "$to" "$file"
        fi
    done < <(rg --hidden --no-ignore -0 -l -F \
        -g '!{.git,.venv,test.sh}' -- "$from" .)
}

function read_copier_answer() {
    local answers_file="$1"
    local key="$2"
    awk -v prefix="$key: " 'index($0, prefix) == 1 { print substr($0, length(prefix) + 1); exit }' "$answers_file"
}

function parse_restore_args() {
    local project_dir=""
    local -a cli_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
        --project-dir)
            if [[ $# -lt 2 ]]; then
                error "$1 缺少参数值"
                exit 1
            fi
            project_dir="$2"
            shift 2
            ;;
        --project-name | --project-slug | --project-tag | --description | --pip-index-url | --version | --email | --author)
            if [[ $# -lt 2 ]]; then
                error "$1 缺少参数值"
                exit 1
            fi
            cli_args+=("$1" "$2")
            shift 2
            ;;
        --debug)
            cli_args+=("$1")
            shift
            ;;
        --*)
            error "未知选项: $1"
            exit 1
            ;;
        *)
            error "未知参数: $1，请使用 --project-dir 指定项目目录"
            exit 1
            ;;
        esac
    done

    if [[ -z "$project_dir" ]]; then
        error "--project-dir 是 restore 的必填参数"
        exit 1
    fi
    if [[ ! -d "$project_dir" ]]; then
        error "项目目录不存在: $project_dir"
        exit 1
    fi

    RESTORE_PROJECT_DIR="$(cd "$project_dir" && pwd)"
    RESTORE_ANSWERS_FILE="$RESTORE_PROJECT_DIR/.copier-answers.yml"
    if [[ ! -f "$RESTORE_ANSWERS_FILE" ]]; then
        error "缺少 $RESTORE_ANSWERS_FILE"
        exit 1
    fi

    local -a answer_args=()
    local option key value
    while IFS='|' read -r option key; do
        value="$(read_copier_answer "$RESTORE_ANSWERS_FILE" "$key")"
        [[ -n "$value" ]] && answer_args+=("$option" "$value")
    done <<'EOF'
--project-name|project_name
--project-slug|project_slug
--project-tag|project_tag
--description|description
--pip-index-url|pip_index_url
--version|version
--author|author
--email|email
EOF

    parse_args "${answer_args[@]}" "${cli_args[@]}"
}

function gen_project() {
    parse_args "$@"
    require_copier

    if [[ -z "$out_dir" ]]; then
        error "--outdir 是必填参数"
        exit 1
    fi
    if [[ -z "$project_name" || "$project_name" == "." || "$project_name" == ".." || "$project_name" == */* ]]; then
        error "project_name 不合法，中止生成"
        exit 1
    fi

    if ! mkdir -p "$out_dir" || ! out_dir="$(cd "$out_dir" && pwd)"; then
        error "无法创建或访问输出目录: $out_dir"
        exit 1
    fi
    local target="$out_dir/$project_name"

    # 模板使用了 jinja2-time 扩展（unsafe 特性），需要 --trust
    local cmd="copier copy --trust --defaults"
    cmd+=" -d project_name=${project_name}"
    cmd+=" -d project_slug=${project_slug}"
    cmd+=" -d project_tag=${project_tag}"
    [[ -n "$description" ]] && cmd+=" -d description='${description}'"
    [[ -n "$pip_index_url" ]] && cmd+=" -d pip_index_url=${pip_index_url}"
    [[ -n "$version" ]] && cmd+=" -d version=${version}"
    cmd+=" -d author=${author}"
    cmd+=" -d email=${email}"
    cmd+=" -d use_github_ci=true -d use_drone_ci=false -d use_gitlab_ci=false"
    cmd+=" $KIT_ROOT $target"
    rm -rf "$target"

    info "生成项目到: $target"
    run_cmd "$cmd 1>/dev/null"
}

function restore_start_kit() {
    parse_restore_args "$@"

    local project_source_dir="$RESTORE_PROJECT_DIR/src/$project_slug"
    local template_source_dir="$TEMPLATE_DIR/src/{{ project_slug }}"
    local rendered_source_dir="$TEMPLATE_DIR/src/$project_slug"

    if [[ "$RESTORE_PROJECT_DIR" == "$TEMPLATE_DIR" ]]; then
        error "项目目录不能是模板目录本身"
        exit 1
    fi
    if [[ ! "$project_slug" =~ ^[a-zA-Z][_a-zA-Z0-9]+$ ]]; then
        error "project_slug 不合法: $project_slug"
        exit 1
    fi
    if [[ ! -d "$project_source_dir" ]]; then
        error "缺少项目源码目录: $project_source_dir"
        exit 1
    fi

    require_command rsync
    require_command rg
    require_command sd
    require_command perl

    info "从项目同步到模板: $RESTORE_PROJECT_DIR -> $TEMPLATE_DIR"
    if [[ "$debug" -eq 1 ]]; then
        info "[DRY-RUN] rsync 项目文件并还原 copier 占位符"
        return
    fi

    if ! rsync -a \
        --exclude '.git/' --exclude '.venv/' --exclude '.devbox/' \
        --exclude 'uv.lock' --exclude '.copier-answers.yml' --exclude '.env' \
        --exclude 'dist/' \
        --exclude '__pycache__/' --exclude '*.pyc' \
        --exclude '.pytest_cache/' --exclude '.ruff_cache/' --exclude '.mypy_cache/' \
        --exclude '.benchmarks/' --exclude '.coverage' --exclude 'htmlcov/' \
        "$RESTORE_PROJECT_DIR/" "$TEMPLATE_DIR/"; then
        error "项目文件同步失败"
        exit 1
    fi

    cd "$TEMPLATE_DIR" || exit 1

    sd_replace "$project_name" "{{ project_name }}"
    sd_replace "$project_slug" "{{ project_slug }}"
    sd_replace "$project_tag" "{{ project_tag }}"
    [[ -n "$description" ]] && sd_replace "$description" "{{ description }}"
    [[ -n "$pip_index_url" ]] && sd_replace "$pip_index_url" "{{ pip_index_url }}"
    [[ -n "$version" ]] && sd_replace "$version" "{{ version }}"
    sd_replace "$author" "{{ author }}"
    sd_replace "$email" "{{ email }}"
    # shellcheck disable=SC2016
    sd_replace "$build_version" '{% raw %}${{% endraw %}{{ project_slug.upper() }}_BUILD_TAG{% raw %}}{% endraw %}'

    if [[ ! -d "$rendered_source_dir" ]]; then
        error "缺少项目源码目录: $rendered_source_dir"
        exit 1
    fi
    rm -rf "$template_source_dir"
    mv "$rendered_source_dir" "$template_source_dir"

    perl -pi -e "s/## \[\{\{ version \}\}\] - \d{4}-\d{2}-\d{2}/## [{{ version }}] - {% now 'utc', '%Y-%m-%d' %}/" \
        "$TEMPLATE_DIR/CHANGELOG.md"

    local file
    while IFS= read -r -d '' file; do
        # 转义 GitHub 表达式，避免 copier 将其中的 {{...}} 当成 Jinja 表达式。
        perl -pi -e 's/\$(\{\{(?!%).*?\}\})/QZWXRAWSTARTQZWX\$\1QZWXRAWENDQZWX/g' "$file"
        sd -s 'QZWXRAWSTARTQZWX' '{% raw %}' "$file"
        sd -s 'QZWXRAWENDQZWX' '{% endraw %}' "$file"
        mv -f "$file" "$file.jinja"
    done < <(rg -0 -l --hidden --no-ignore -g '!.git' -g '!*.jinja' -g '!*.pyc' \
        -e '\{\{\s*(project_|version|description|pip_index_url|author|email)|project_slug\.upper|\{\%' \
        "$TEMPLATE_DIR")

    success "已同步生成项目到模板，并还原为占位符"
}

case "$1" in
"gen")
    shift
    gen_project "$@"
    ;;
"restore")
    shift
    restore_start_kit "$@"
    ;;
*)
    cat <<EOF
用法: $0 gen --outdir <目录> [选项]
      $0 restore --project-dir <目录> [选项]

子命令:
  gen   基于 copier 模板生成新项目
  restore   将已有项目还原为 copier 模板占位符

选项:
  --outdir       <dir>    生成项目的父目录（gen 必填）
  --project-dir   <dir>    要同步回模板的项目目录（restore 必填）
  --project-name  <name>   项目名称（必填）
  --project-slug  <slug>   项目标识，默认由 project-name 转换（小写、空格和连字符转下划线）
  --project-tag   <tag>    项目标签，默认由 project-slug 去掉 _web 后缀
  --description   <desc>   项目描述
  --pip-index-url <url>    pip 镜像源地址
  --version       <version> 项目版本
  --author        <author> 作者，默认 seekplum
  --email         <email>  邮箱地址，默认 1131909224m@sina.cn
  --debug                  仅打印命令，不实际执行

示例:
  $0 gen --outdir /tmp/out-copier --project-name "plum-tools"
  $0 restore --project-dir ~/path/to/plum-tools --project-name "plum-tools"
EOF
    exit 1
    ;;
esac
