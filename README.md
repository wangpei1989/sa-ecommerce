# South Africa Cross-Border E-commerce Platform

南非跨境电商平台 - Coze Agent 应用

## 最新提交 (v1.0.5)
- ✅ 修复部署构建错误（tool.uv.dev-dependencies弃用警告）
- ✅ 增加UV网络超时配置（300秒）
- ✅ 重新生成uv.lock依赖锁定文件

## 项目状态

| 模块 | 状态 |
|------|------|
| 用户端 | ✅ 完成 |
| 商家端 | ✅ 完成 |
| 物流清关 | ✅ 完成 |
| 营销系统 | ✅ 完成 |
| 本地化 | ✅ 完成 |
| Android打包 | ✅ 完成 |

## 部署说明

### 部署前检查清单
- [x] pyproject.toml - 无 `tool.uv` 配置
- [x] dependency-groups.dev - 已正确配置
- [x] uv.lock - 已生成（130 packages）
- [x] scripts/setup.sh - UV_HTTP_TIMEOUT=300

### 部署步骤
1. 确保代码已提交到 git
2. 在 Coze 平台点击「重新部署」按钮
3. 等待构建完成（约3-5分钟）
4. 验证部署成功

### 常见问题

**Q: 部署仍然失败，显示相同的错误？**
A: 这是旧的部署日志。请确保点击「重新部署」按钮，生成新的 deployment_history_id。

**Q: 如何确认使用了最新配置？**
A: 查看新的部署日志，应显示：
- `Resolved 130 packages` (不是110)
- 无 `tool.uv.dev-dependencies` 警告
- `UV_HTTP_TIMEOUT` 值为 300

## 文件结构

```
/workspace/projects/
├── src/
│   ├── agents/agent.py           # Agent核心配置
│   └── tools/                    # 业务工具集
├── config/
│   └── agent_llm_config.json     # 模型配置
├── android/                      # Android打包配置
├── scripts/
│   └── setup.sh                  # 部署脚本（含超时配置）
├── pyproject.toml                # 项目配置
├── uv.lock                       # 依赖锁定
└── .coze                         # Coze配置
```
