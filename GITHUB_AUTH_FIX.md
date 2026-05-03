# GitHub 认证问题解决方案

## 错误原因
```
remote: Invalid username or token. Password authentication is not supported for Git operations.
```
GitHub 已停止支持密码认证，必须使用 **Token** 或 **SSH Key**。

---

## 方案一：使用 Personal Access Token（推荐）

### 1. 生成 Personal Access Token
1. 登录 GitHub → 点击头像 → **Settings**
2. 左侧菜单 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. 点击 **Generate new token (classic)**
5. 设置：
   - **Name**: 随便填，如 `git-push`
   - **Expiration**: 选择过期时间
   - **Scopes**: ✅ 勾选 `repo` (完整仓库权限)
6. 点击 **Generate token**
7. **⚠️ 立即复制保存**，关闭页面后无法找回

### 2. 配置 Git 使用 Token

```bash
# 方法A：使用 Token URL（临时有效）
git remote set-url origin https://wangpei1989:你的TOKEN@github.com/wangpei1989/sa-ecommerce.git

# 方法B：缓存凭证（推荐）
git config --global credential.helper store
git push origin main
# 然后按提示输入：用户名=wangpei1989，密码=你的TOKEN
```

### 3. 推送代码
```bash
git push -u origin main
```

---

## 方案二：使用 SSH Key（永久有效）

### 1. 生成 SSH Key
```bash
ssh-keygen -t ed25519 -C "wangpei1989@example.com"
# 提示时直接回车（使用默认位置）
# 可以设置密码也可以不设置
```

### 2. 查看公钥
```bash
cat ~/.ssh/id_ed25519.pub
# 输出类似：
# ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIxxxxx wangpei1989@example.com
```

### 3. 添加公钥到 GitHub
1. GitHub → **Settings** → **SSH and GPG keys**
2. 点击 **New SSH key**
3. 填写：
   - **Title**: 随便填，如 `My Linux Server`
   - **Key**: 粘贴刚才复制的公钥内容
4. 点击 **Add SSH key**

### 4. 修改远程仓库为 SSH 格式
```bash
git remote set-url origin git@github.com:wangpei1989/sa-ecommerce.git
```

### 5. 推送代码
```bash
git push -u origin main
# 如果设置了密码，输入密码即可
```

---

## 快速修复（复制粘贴）

### 如果选择方案一（Token）：
```bash
git remote set-url origin https://wangpei1989:你的TOKEN@github.com/wangpei1989/sa-ecommerce.git
git push -u origin main
```

### 如果选择方案二（SSH）：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# 回车3次跳过
cat ~/.ssh/id_ed25519.pub
# 复制公钥到 GitHub

git remote set-url origin git@github.com:wangpei1989/sa-ecommerce.git
git push -u origin main
```

---

## 验证连接
```bash
# 测试 SSH 连接
ssh -T git@github.com
# 如果看到 "Hi wangpei1989! You've successfully authenticated" 表示成功
```
