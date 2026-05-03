# 纯 Token 认证方案（无需 SSH）

## 问题分析
`ssh-keygen` 命令不可用，但可以使用 **Token** 方式推送。

---

## 步骤 1：确认 Token 格式

在 GitHub 生成 Token 后，确保格式正确：
- Token 格式：`ghp_xxxxxxxxxxxxxxxxxxxx`（以 `ghp_` 开头）
- 或者：`github_pat_xxxxxxxxxxx`（Personal Access Token）

---

## 步骤 2：重新设置远程仓库

```bash
# 先查看当前远程仓库
git remote -v

# 移除旧的
git remote remove origin

# 添加新的（包含Token）
git remote add origin https://wangpei1989:ghp_你的TOKEN@github.com/wangpei1989/sa-ecommerce.git

# 推送
git push -u origin main
```

---

## 如果还没有 Token

### 1. 打开 GitHub Token 页面
https://github.com/settings/tokens

### 2. 点击 "Generate new token" → "Generate new token (classic)"

### 3. 配置 Token
```
Name: git-push
Expiration: 30 days（或自定义）
Scopes: ✅ repo (Full control of private repositories)
```

### 4. 点击 "Generate token"

### 5. ⚠️ 立即复制 Token（只显示一次！）

### 6. 执行：
```bash
git remote add origin https://wangpei1989:粘贴你的TOKEN@github.com/wangpei1989/sa-ecommerce.git
git push -u origin main
```

---

## 一行命令解决

把下面的 `你的TOKEN` 替换为你的 GitHub Token：

```bash
git remote set-url origin https://wangpei1989:你的TOKEN@github.com/wangpei1989/sa-ecommerce.git && git push -u origin main
```

---

## 验证 Token 是否有效

```bash
curl -u wangpei1989:你的TOKEN https://api.github.com/user
```

如果返回 JSON 用户信息，说明 Token 有效。
