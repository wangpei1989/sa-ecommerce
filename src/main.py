"""
南非跨境电商 Agent - 运行入口
"""
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent import build_agent
from coze_coding_utils.runtime_ctx.context import new_context

# 创建 FastAPI 应用
app = FastAPI(title="South African E-commerce Agent")

# 全局 agent 实例
_agent_instance = None

def get_agent():
    """获取或创建 Agent 实例"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = build_agent()
    return _agent_instance

@app.post("/stream_run")
async def stream_run(request: Request):
    """处理流式运行请求"""
    try:
        body = await request.json()
        
        ctx = new_context(method="stream_run")
        run_id = ctx.run_id
        session_id = body.get("session_id", "default")
        query = body.get("query", "")
        
        agent = get_agent()
        
        async def event_generator():
            try:
                run_config = {
                    "recursion_limit": 100,
                    "configurable": {"thread_id": session_id}
                }
                
                async for chunk in agent.astream(
                    {"messages": [("user", query)]},
                    config=run_config,
                    stream_mode="messages",
                ):
                    if chunk and len(chunk) >= 2:
                        msg = chunk[1]
                        if hasattr(msg, "content") and msg.content:
                            yield f"data: {json.dumps({'type': 'message', 'content': msg.content}, ensure_ascii=False)}\n\n"
            except asyncio.CancelledError:
                yield f"data: {json.dumps({'type': 'end'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        return StreamingResponse(
            iter([f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"]),
            media_type="text/event-stream"
        )

def main():
    """启动服务"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
