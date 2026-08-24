#!/bin/bash
# YAML检查脚本
# 检查GitHub Actions YAML文件语法

# 检查yamllint是否可用
if ! command -v yamllint &> /dev/null; then
    echo "错误: yamllint 未安装"
    exit 1
fi

# 定位仓库中的工作流文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
YAML_FILE="$REPOSITORY_ROOT/.github/workflows/api-test.yml"
echo "正在检查YAML文件语法..."
echo "检查文件: $YAML_FILE"
if yamllint "$YAML_FILE"; then
    echo "✓ $YAML_FILE 语法正确"
else
    echo "✗ $YAML_FILE 语法错误"
    exit 1
fi

echo "所有YAML文件检查完成"
