#!/bin/bash
# 自动化发布脚本 - 需要 GitHub Token

set -e

echo "🚀 Open Field Tracker 自动化发布"
echo "=================================="
echo ""

# 检查参数
if [ -z "$1" ]; then
    echo "使用方法: ./auto-release.sh <GITHUB_TOKEN>"
    echo ""
    echo "获取 GitHub Token:"
    echo "1. 访问 https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 勾选 'repo' 权限"
    echo "4. 复制生成的 token"
    echo ""
    exit 1
fi

GITHUB_TOKEN=$1
REPO="tonyliurice/open-field-tracker"

echo "📦 步骤 1: 创建 GitHub Release"
echo "-------------------------------"

# 创建 Release
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO/releases \
  -d '{
    "tag_name": "v1.0.0",
    "name": "v1.0.0 - Initial Release",
    "body": "First release of Open Field Tracker\n\nFeatures:\n- Trajectory analysis\n- Heatmap generation\n- Statistical reports\n- Batch processing",
    "draft": false,
    "prerelease": false
  }'

echo ""
echo "✅ GitHub Release 创建成功！"
echo ""

echo "📋 步骤 2: 启用 Zenodo 集成"
echo "---------------------------"
echo ""
echo "请手动完成以下步骤："
echo "1. 访问 https://zenodo.org/"
echo "2. 点击 'Log in' → 'Log in with GitHub'"
echo "3. 授权 Zenodo 访问"
echo "4. 访问 https://zenodo.org/account/settings/github/"
echo "5. 找到 'tonyliurice/open-field-tracker'，点击开关启用"
echo ""

echo "⏳ 步骤 3: 等待 Zenodo 处理"
echo "--------------------------"
echo "Release 创建后，Zenodo 会自动检测到并生成 DOI"
echo "等待时间: 5-10 分钟"
echo ""

echo "🔍 步骤 4: 获取 DOI"
echo "------------------"
echo "访问 https://zenodo.org/account/settings/github/"
echo "找到你的仓库，点击链接查看 DOI"
echo ""

echo "✏️  步骤 5: 更新项目文件"
echo "----------------------"
echo "获取 DOI 后，运行: ./update-doi.sh <DOI>"
echo ""

echo "=================================="
echo "🎉 自动化发布完成！"
