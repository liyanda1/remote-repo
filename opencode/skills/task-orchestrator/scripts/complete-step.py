#!/usr/bin/env python3
"""
SubAgent调用：标记步骤完成
用法: python complete-step.py --step 1 --status success [--result "结果描述"]

自动操作 ~/.config/opencode/task-orchestrator/ 下的文件
"""

import argparse
import json
import os
from datetime import datetime
from config import get_plans_dir, get_logs_dir, get_state_dir, ensure_dir


def load_plan(plan_path):
    """加载任务计划"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_plan(plan_path, plan):
    """保存任务计划"""
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)


def find_plan_by_task_id(task_id):
    """通过任务ID查找计划文件"""
    plans_dir = get_plans_dir()
    if not os.path.exists(plans_dir):
        return None
    
    for f in os.listdir(plans_dir):
        if f.endswith('.json'):
            plan_path = os.path.join(plans_dir, f)
            try:
                with open(plan_path, 'r', encoding='utf-8') as file:
                    plan = json.load(file)
                    if plan.get('task_id') == task_id:
                        return plan_path
            except:
                pass
    return None


def main():
    parser = argparse.ArgumentParser(description='标记步骤完成（由subAgent调用）')
    parser.add_argument('--plan', '-p', help='任务计划文件路径')
    parser.add_argument('--task-id', '-t', help='任务ID（替代plan参数）')
    parser.add_argument('--step', '-s', type=int, required=True, help='步骤ID')
    parser.add_argument('--status', required=True, choices=['success', 'failed'], help='完成状态')
    parser.add_argument('--result', '-r', help='执行结果描述')
    parser.add_argument('--error', '-e', help='错误信息（失败时）')
    
    args = parser.parse_args()
    
    # 确定计划文件路径
    plan_path = args.plan
    if not plan_path and args.task_id:
        plan_path = find_plan_by_task_id(args.task_id)
    
    if not plan_path:
        # 尝试从当前状态获取
        state_path = os.path.join(get_state_dir(), "current.json")
        if os.path.exists(state_path):
            with open(state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
                plan_path = state.get('active_plan')
    
    if not plan_path or not os.path.exists(plan_path):
        print(f"❌ 错误: 找不到任务计划文件")
        return
    
    plan = load_plan(plan_path)
    
    # 更新步骤状态
    for step in plan['steps']:
        if step['id'] == args.step:
            step['status'] = args.status
            step['completed_at'] = datetime.now().isoformat()
            if args.result:
                step['result'] = args.result
            if args.error:
                step['error'] = args.error
            break
    
    # 检查是否所有步骤完成
    all_completed = all(s['status'] in ['success', 'failed', 'cancelled'] for s in plan['steps'])
    any_failed = any(s['status'] == 'failed' for s in plan['steps'])
    
    if all_completed:
        plan['overall_status'] = 'failed' if any_failed else 'completed'
    
    save_plan(plan_path, plan)
    
    # 写入日志
    log_path = os.path.join(get_logs_dir(), f"step-{args.step}.log")
    ensure_dir(log_path)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.now().isoformat()}] 步骤 {args.step} {args.status}\n")
        if args.result:
            f.write(f"结果: {args.result}\n")
        if args.error:
            f.write(f"错误: {args.error}\n")
    
    print(f"✅ 步骤 {args.step} 已标记为 {args.status}")


if __name__ == '__main__':
    main()
