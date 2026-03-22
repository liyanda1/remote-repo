#!/usr/bin/env python3
"""
配置文件 - 管理临时文件存储路径
"""

import os


def get_orchestrator_dir():
    """
    获取任务编排器的工作目录
    优先使用 ~/.config/opencode/task-orchestrator/（用户无感知）
    如果不存在则使用当前目录下的 .orchestrator/
    """
    # 优先使用全局配置目录（用户无感知）
    global_dir = os.path.expanduser("~/.config/opencode/task-orchestrator")
    
    # 如果全局目录存在或可以创建，使用它
    try:
        os.makedirs(global_dir, exist_ok=True)
        return global_dir
    except:
        pass
    
    # 回退到当前目录
    local_dir = "./.orchestrator"
    os.makedirs(local_dir, exist_ok=True)
    return local_dir


def get_plans_dir():
    """获取计划文件目录"""
    return os.path.join(get_orchestrator_dir(), "plans")


def get_logs_dir():
    """获取日志目录"""
    return os.path.join(get_orchestrator_dir(), "logs")


def get_state_dir():
    """获取状态目录"""
    return os.path.join(get_orchestrator_dir(), "state")


def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
