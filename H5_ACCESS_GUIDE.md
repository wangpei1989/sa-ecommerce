# H5 访问指南

## 方式一：Coze 预览页面（Web H5）

部署成功后，通过 Coze 平台的内置预览功能即可在浏览器中访问。

### 操作步骤

1. **部署 Agent**
   - 在 Coze 平台打开您的 Agent
   - 点击「发布」按钮

2. **获取访问地址**
   - 发布成功后，点击「预览」或「对话」按钮
   - 在浏览器中打开预览页面即可体验

3. **分享给用户**
   - 在 Coze 平台可以获取公开访问链接
   - 用户无需登录即可通过链接访问

### 预览页面特点

| 特性 | 说明 |
|------|------|
| 响应式设计 | 自动适配手机/平板/PC |
| 语音输入 | 支持语音对话 |
| 图片上传 | 支持发送图片 |
| 流式响应 | 实时显示回复 |

---

## 方式二：集成到现有 H5 应用

如果您有自己的 H5 应用，可以将 Agent 集成嵌入。

### 集成代码示例

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>南非电商助手</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #006400;
            color: white;
            padding: 15px;
            text-align: center;
        }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }
        .message {
            margin-bottom: 15px;
            max-width: 80%;
        }
        .user-message {
            background: #006400;
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin-left: auto;
        }
        .bot-message {
            background: white;
            color: #333;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .input-area {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #eee;
        }
        .input-area input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 24px;
            outline: none;
        }
        .input-area button {
            background: #006400;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 24px;
            margin-left: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>🛒 南非跨境电商助手</h2>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot-message">
            👋 您好！欢迎使用南非跨境电商助手。<br><br>
            我可以帮您：<br>
            • 📱 注册登录<br>
            • 🔍 商品搜索<br>
            • 🛒 购物车管理<br>
            • 📦 订单处理<br>
            • 💳 多种支付方式<br>
            • 🚚 物流追踪<br>
            • 💰 货币转换<br><br>
            请告诉我您的需求！
        </div>
    </div>
    
    <div class="input-area">
        <input type="text" id="userInput" placeholder="输入您的问题..." />
        <button onclick="sendMessage()">发送</button>
    </div>

    <script>
        // 替换为您的 Agent API 地址
        const API_ENDPOINT = 'https://your-agent-api.coze.cn/open_api/v2/chat';
        const API_TOKEN = 'YOUR_API_TOKEN';
        const BOT_ID = 'YOUR_BOT_ID';

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            // 添加用户消息
            addMessage(message, 'user');
            input.value = '';

            // 调用 Agent API
            try {
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${API_TOKEN}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        bot_id: BOT_ID,
                        user_id: 'h5_user_' + Date.now(),
                        query: message,
                        stream: false
                    })
                });

                const data = await response.json();
                if (data.msg && data.msg === 'success') {
                    // 获取机器人回复
                    addMessage(data.messages?.[0]?.content || '处理中...', 'bot');
                } else {
                    addMessage('抱歉，服务暂时不可用。', 'bot');
                }
            } catch (error) {
                addMessage('网络错误，请稍后重试。', 'bot');
            }
        }

        function addMessage(text, type) {
            const container = document.getElementById('chatContainer');
            const div = document.createElement('div');
            div.className = `message ${type}-message`;
            div.innerHTML = text.replace(/\n/g, '<br>');
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        // 回车发送
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

---

## 方式三：部署为独立 Web 服务

### 使用 FastAPI 部署

```bash
# 安装依赖
pip install fastapi uvicorn

# 运行服务
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 使用 Vercel/Netlify 部署静态页面

1. 将上面的 HTML 保存为 `index.html`
2. 部署到 Vercel 或 Netlify
3. 配置 API 代理到 Agent

---

## 功能演示

部署后，您可以在 H5 页面体验以下功能：

| 功能 | 示例对话 |
|------|---------|
| 用户注册 | "我想注册，手机号+27825551234" |
| 商品搜索 | "搜索手机" |
| 购物车 | "添加到购物车" |
| 订单创建 | "创建订单" |
| 支付 | "使用Ozow支付" |
| 物流追踪 | "追踪物流SA123456" |
| 货币转换 | "100美元转ZAR" |
| 自提点 | "查询Gauteng省自提点" |

---

## 注意事项

1. **API Token 安全**：不要在前端暴露 API Token，使用后端代理
2. **CORS 配置**：如果调用跨域 API，需要配置 CORS
3. **移动端适配**：使用响应式设计，适配各种屏幕尺寸
4. **弱网处理**：添加 loading 状态和错误提示
