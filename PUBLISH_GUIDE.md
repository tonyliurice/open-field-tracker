# Open Field Tracker - 一键发布指南

**GitHub 用户名**: tonyliurice  
**作者**: Tianyi Liu  
**ORCID**: 0009-0004-2339-1945

---

## 🚀 快速发布（复制粘贴执行）

### 步骤 1: 打开终端

在 Mac 上按 `Cmd + Space`，输入 `Terminal`，回车打开终端。

### 步骤 2: 进入项目目录

```bash
cd ~/Desktop/open-field-tracker
```

### 步骤 3: 创建 GitHub 仓库

**选项 A: 使用 GitHub CLI（推荐）**

```bash
# 安装 GitHub CLI（如果未安装）
brew install gh

# 登录 GitHub
gh auth login

# 创建仓库并推送
gh repo create open-field-tracker --public --source=. --push
```

**选项 B: 手动创建（如果 CLI 安装失败）**

1. 打开浏览器访问: https://github.com/new
2. 填写信息:
   - Repository name: `open-field-tracker`
   - Description: `A Python toolkit for rat movement trajectory analysis in open field tests`
   - 选择 `Public`
   - **不要勾选** "Initialize this repository with a README"
3. 点击 "Create repository"
4. 复制以下命令执行:

```bash
cd ~/Desktop/open-field-tracker
git remote add origin https://github.com/tonyliurice/open-field-tracker.git
git branch -M main
git push -u origin main
```

**注意**: 如果提示输入用户名密码，输入:
- 用户名: `tonyliurice`
- 密码: 使用 GitHub Personal Access Token（不是登录密码）
  - 创建 Token: https://github.com/settings/tokens
  - 点击 "Generate new token (classic)"
  - 勾选 `repo` 权限
  - 复制生成的 token 作为密码

---

## 📦 Zenodo 集成（获取 DOI）

### 步骤 4: 启用 Zenodo 集成

1. 访问 https://zenodo.org/
2. 点击右上角 "Log in" → 选择 "Log in with GitHub"
3. 授权 Zenodo 访问你的 GitHub 账号
4. 点击右上角用户名 → "GitHub"
5. 找到 `tonyliurice/open-field-tracker`，点击开关启用

### 步骤 5: 创建 Release（触发 Zenodo）

**选项 A: 使用 GitHub CLI**

```bash
gh release create v1.0.0 --title "v1.0.0 - Initial Release" --notes "First release of Open Field Tracker"
```

**选项 B: 网页操作**

1. 访问: https://github.com/tonyliurice/open-field-tracker/releases
2. 点击 "Create a new release"
3. 填写:
   - Choose a tag: `v1.0.0` (输入后点击 "Create new tag")
   - Release title: `v1.0.0 - Initial Release`
   - Description: `First release of Open Field Tracker`
4. 点击 "Publish release"

### 步骤 6: 获取 DOI

1. 等待 5-10 分钟
2. 访问 https://zenodo.org/account/settings/github/
3. 找到 `open-field-tracker`，点击链接查看
4. 复制 DOI（格式: `10.5281/zenodo.xxxxx`）

---

## 🔄 更新 DOI（关键步骤）

### 步骤 7: 替换占位符

假设你的 DOI 是 `10.5281/zenodo.12345678`，执行:

```bash
cd ~/Desktop/open-field-tracker

# 替换所有文件中的占位符
sed -i '' 's/10.5281\/zenodo.placeholder/10.5281\/zenodo.12345678/g' README.md
sed -i '' 's/10.5281\/zenodo.placeholder/10.5281\/zenodo.12345678/g' CITATION.cff
sed -i '' 's/10.5281\/zenodo.placeholder/10.5281\/zenodo.12345678/g' skill/skill.json
sed -i '' 's/10.5281\/zenodo.placeholder/10.5281\/zenodo.12345678/g' skill/README.md
sed -i '' 's/10.5281\/zenodo.placeholder/10.5281\/zenodo.12345678/g' src/open_field_tracker/__init__.py

# 提交更新
git add .
git commit -m "Update DOI to 10.5281/zenodo.12345678"
git push origin main
```

**注意**: 将 `10.5281/zenodo.12345678` 替换为你的真实 DOI！

---

## 🦾 Kimi Skill 发布

### 步骤 8: 提交 Skill

1. 访问 https://kimi.moonshot.cn/
2. 登录你的账号
3. 找到 "智能体" 或 "Skill" 入口
4. 点击 "创建智能体" 或 "发布 Skill"
5. 上传 `~/Desktop/open-field-tracker/skill/` 目录下的文件:
   - `skill.json`
   - `main.py`
   - `README.md`
6. 填写信息:
   - 名称: 旷场实验分析助手
   - 描述: 智能分析大鼠旷场实验数据，生成运动轨迹图和热力图
   - 图标: 可以上传或使用 Emoji 🐭
7. 提交审核

---

## ✅ 验证清单

发布完成后，检查以下链接是否可访问:

- [ ] GitHub 仓库: https://github.com/tonyliurice/open-field-tracker
- [ ] Zenodo 记录: https://doi.org/10.5281/zenodo.xxxxx (你的 DOI)
- [ ] Kimi Skill: https://kimi.moonshot.cn/chat/xxxxxxxx (发布后获得)

---

## 📧 后续维护

### 更新版本

```bash
# 1. 修改版本号
# 编辑 src/open_field_tracker/__init__.py 中的 __version__
# 编辑 skill/skill.json 中的 version

# 2. 提交更改
git add .
git commit -m "Bump version to v1.1.0"
git push origin main

# 3. 创建新 Release
gh release create v1.1.0 --title "v1.1.0" --notes "Update description"

# 4. Zenodo 自动生成新版本 DOI
```

---

## 🆘 常见问题

### Q: 推送时提示 "Permission denied"
**A**: 使用 Personal Access Token 代替密码，或配置 SSH key:
```bash
ssh-keygen -t ed25519 -C "liutianyi@example.com"
cat ~/.ssh/id_ed25519.pub
# 复制内容到 https://github.com/settings/keys → New SSH key
```

### Q: Zenodo 没有自动生成 DOI
**A**: 
1. 确认 GitHub 仓库已公开
2. 确认 Release 已发布
3. 等待 10-15 分钟
4. 检查 https://zenodo.org/account/settings/github/ 是否显示绿色勾

### Q: Kimi Skill 审核不通过
**A**: 
1. 确保代码可运行
2. 提供清晰的说明文档
3. 添加示例数据

---

## 🎉 完成！

发布后你将拥有:
1. ✅ GitHub 开源仓库（可展示技术实力）
2. ✅ Zenodo DOI（可被学术论文引用）
3. ✅ Kimi Skill（用户可直接使用）

**学术引用格式**:
```bibtex
@software{liu_open_field_tracker_2026,
  author = {Liu, Tianyi},
  title = {Open Field Tracker},
  year = {2026},
  publisher = {Zenodo},
  version = {1.0.0},
  doi = {10.5281/zenodo.xxxxx}
}
```

