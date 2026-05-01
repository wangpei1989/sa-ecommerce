"""
Agent 短期记忆管理器
使用 LangGraph MemorySaver 实现对话历史持久化
"""
from langgraph.checkpoint.memory import MemorySaver
from typing import Optional, TYPE_CHECKING

# 全局单例 checkpointer
_memory_saver: Optional[MemorySaver] = None

def get_memory_saver() -> MemorySaver:
    """获取或创建 MemorySaver 单例"""
    global _memory_saver
    if _memory_saver is None:
        _memory_saver = MemorySaver()
    return _memory_saver

# 兼容旧接口
MemoryManager = MemorySaver
