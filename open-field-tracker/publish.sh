#!/bin/bash
# Open Field Tracker 一键发布脚本

echo "🚀 Open Field Tracker 发布脚本"
echo "================================"
echo ""

# 检查 Git
echo "📋 检查 Git 配置..."
git config --global user.name "Tianyi Liu"
git config --global user.email "liutianyi@example.com"
echo "✅ Git 配置完成"
echo ""

# 检查 GitHub CLI
echo "📋 检查 GitHub CLI..."
if ! command -v gh &> /dev/null; then
    echo "正在安装 GitHub CLI..."
    brew install gh
fi
echo "✅ GitHub CLI 已安装"
echo ""

# 登录 GitHub
echo "🔐 请登录 GitHub..."
gh auth login
echo ""

# 创建仓库
echo "📦 创建 GitHub 仓库..."
cd ~/Desktop/open-field-tracker
gh repo create open-field-tracker --public --source=. --push
echo "✅ 仓库创建并推送完成"
echo ""

# 创建 Release
echo "🏷️  创建 Release v1.0.0..."
gh release create v1.0.0 --title "v1.0.0 - Initial Release" --notes "First release of Open Field Tracker"
echo "✅ Release 创建完成"
echo ""

echo "================================"
echo "🎉 步骤 1-3 完成！"
echo ""
echo "下一步："
echo "1. 访问 https://zenodo.org/ 用 GitHub 登录"
echo "2. 启用 open-field-tracker 仓库集成"
echo "3. 等待 DOI 生成（约 10 分钟）"
echo "4. 运行 update_doi.sh 更新 DOI"
echo ""
