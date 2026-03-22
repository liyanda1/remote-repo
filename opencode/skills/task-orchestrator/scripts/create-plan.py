#!/usr/bin/env python3
"""
创建任务计划脚本
用法: python create-plan.py --task "任务描述" --steps 5 [--cleanup auto|manual|keep]

临时文件存储在 ~/.config/opencode/task-orchestrator/（用户无感知）
"""

import argparse
import json
import os
import uuid
from datetime import datetime
from config import get_plans_dir, get_state_dir, ensure_dir


def create_plan(task_desc, num_steps, output_path=None, cleanup='auto'):
    """创建任务计划文件"""
    
    task_id = str(uuid.uuid4())[:8]
    
    # 使用全局目录存储（用户无感知）
    plans_dir = get_plans_dir()
    if output_path is None:
        output_path = os.path.join(plans_dir, f"task-{task_id}.json")
    
    ensure_dir(output_path)
    
    # 生成步骤模板
    steps = []
    for i in range(1, num_steps + 1):
        steps.append({
            "id": i,
            "name": f"步骤 {i}",
            "description": f"第 {i} 步任务",
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "retry_count": 0,
            "max_retries": 3,
            "timeout_minutes": 30,
            "result": None,
            "error": None
        })
    
    plan = {
        "task_id": task_id,
        "task_description": task_desc,
        "created_at": datetime.now().isoformat(),
        "total_steps": num_steps,
        "current_step": 0,
        "overall_status": "pending",
        "steps": steps,
        "metadata": {
            "mode": "background",
            "auto_advance": False,
            "cleanup": cleanup
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    # 同时创建当前状态文件
    state_path = os.path.join(get_state_dir(), "current.json")
    ensure_dir(state_path)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump({
            "active_plan": output_path,
            "updated_at": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 任务计划已创建")
    print(f"   任务ID: {task_id}")
    print(f"   步骤数: {num_steps}")
    print(f"\n使用方式:")
    print(f"   1. 调用 @executor 执行步骤")
    print(f"   2. 检查状态: python3 scripts/status.py")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='创建任务计划')
    parser.add_argument('--task', '-t', required=True, help='任务描述')
    parser.add_argument('--steps', '-s', type=int, required=True, help='步骤数量')
    parser.add_argument('--output', '-o', help='输出文件路径（高级用户）')
    parser.add_argument('--cleanup', '-c', choices=['auto', 'manual', 'keep'], 
                        default='auto', help='临时文件清理策略（默认auto）')
    
    args = parser.parse_args()
    
    create_plan(args.task, args.steps, args.output, args.cleanup)


if __name__ == '__main__':
    main()
