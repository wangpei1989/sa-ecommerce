# GitHub 上传指南

## 前置准备

1. **注册 GitHub 账号** (如果没有)
   - 访问 https://github.com
   - 点击 "Sign up" 注册

2. **生成 SSH Key** (推荐，避免每次输入密码)
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   cat ~/.ssh/id_ed25519.pub  # 复制公钥到 GitHub Settings
   ```

## 方法一：命令行上传（推荐）

### 1. 进入项目目录
```bash
cd /workspace/projects
```

### 2. 初始化 Git（如果还没有）
```bash
git init
```

### 3. 配置用户信息
```bash
git config user.name "Your Name"
git config user.email "your_email@example.com"
```

### 4. 添加远程仓库
```bash
# 在 GitHub 创建仓库后复制仓库 URL
git remote add origin https://github.com/username/repository-name.git
# 或使用 SSH
git remote add origin git@github.com:username/repository-name.git
```

### 5. 创建 .gitignore 文件
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/
dist/
build/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Gradle (Android)
android/.gradle/
android/build/
android/app/build/
android/app/release/
android/app/debug/

# Credentials (NEVER commit these)
*.pem
*.key
credentials.json
EOF
```

### 6. 添加文件并提交
```bash
# 添加所有文件
git add .

# 或添加特定文件/目录
git add src/ config/ android/ pyproject.toml README.md

# 提交
git commit -m "feat: 南非跨境电商APP - 初始版本

- 用户端：注册登录、商品搜索、购物车、订单、支付
- 商家端：入驻、商品上架、订单管理、结算
- 物流清关：追踪、自提点、清关流程
- 营销：促销、优惠券、积分系统
- 南非本地化：ZAR货币、11种语言、省份数据"
```

### 7. 推送到 GitHub
```bash
# 首次推送
git push -u origin main

# 之后更新
git push origin main
```

## 方法二：GitHub 网页上传

### 1. 创建仓库
- 登录 GitHub
- 点击右上角 "+" → "New repository"
- 填写仓库名称和描述
- 选择 Public/Private
- 点击 "Create repository"

### 2. 上传文件
- 在仓库页面点击 "uploading an existing file"
- 拖拽文件到上传区域
- 填写提交信息
- 点击 "Commit changes"

## 方法三：GitHub Desktop

### 1. 下载 GitHub Desktop
- 访问 https://desktop.github.com

### 2. 添加仓库
- File → Add Local Repository
- 选择项目目录
- 点击 "Publish repository"

## 分支管理建议

```bash
# 创建开发分支
git checkout -b develop

# 开发完成后合并到 main
git checkout main
git merge develop
git push origin main

# 删除分支
git branch -d develop
git push origin --delete develop
```

## 常见问题

### Q: 推送被拒绝？
```bash
# 可能是远程有更新，先拉取合并
git pull origin main --rebase

# 或强制推送（谨慎使用）
git push -f origin main
```

### Q: 如何更新代码？
```bash
git add .
git commit -m "feat: 新增xxx功能"
git push origin main
```

### Q: 如何克隆仓库到新机器？
```bash
git clone https://github.com/username/repository-name.git
cd repository-name
```

## 安全注意事项

⚠️ **禁止上传的内容：**
- API Keys / Tokens
- 数据库密码
- 私钥文件 (.pem, .key)
- .env 文件
- 用户隐私数据

⚠️ **确保已添加到 .gitignore**

## 自动化部署（可选）

### 使用 GitHub Actions
在 `.github/workflows/` 创建 `deploy.yml`：
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to server
        run: |
          # 部署命令
```

---

## 快速命令汇总

```bash
cd /workspace/projects
git init
git add .
git commit -m "feat: 南非跨境电商APP"
git remote add origin https://github.com/YOUR_USERNAME/sa-ecommerce.git
git push -u origin main
```

只需将 `YOUR_USERNAME` 和 `sa-ecommerce` 替换为你的 GitHub 用户名和仓库名即可。
