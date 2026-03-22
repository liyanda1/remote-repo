#!/usr/bin/env python3
"""
执行下一步（分点执行模式）
用法: python next.py [--yes]

自动从 ~/.config/opencode/task-orchestrator/ 读取当前任务
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from config import get_state_dir, get_plans_dir


def load_plan(plan_path):
    """加载任务计划"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_current_state():
    """加载当前状态"""
    state_path = os.path.join(get_state_dir(), "current.json")
    if not os.path.exists(state_path):
        return None
    with open(state_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_next_step(plan):
    """找到下一个待执行的步骤"""
    for step in plan['steps']:
        if step['status'] == 'pending':
            return step
    return None


def list_all_plans():
    """列出所有任务计划"""
    plans_dir = get_plans_dir()
    if not os.path.exists(plans_dir):
        return []
    
    plans = []
    for f in os.listdir(plans_dir):
        if f.endswith('.json'):
            plan_path = os.path.join(plans_dir, f)
            try:
                with open(plan_path, 'r', encoding='utf-8') as file:
                    plan = json.load(file)
                    plans.append({
                        'path': plan_path,
                        'plan': plan
                    })
            except:
                pass
    return plans


def main():
    parser = argparse.ArgumentParser(description='执行下一步')
    parser.add_argument('--yes', '-y', action='store_true', help='跳过确认')
    
    args = parser.parse_args()
    
    # 加载当前状态
    state = load_current_state()
    plan_path = None
    
    if state and 'active_plan' in state:
        plan_path = state['active_plan']
    
    # 如果没有活跃计划，尝试找任何计划
    if not plan_path or not os.path.exists(plan_path):
        plans = list_all_plans()
        if plans:
            # 找第一个未完成的任务
            for p in plans:
                if p['plan'].get('overall_status') not in ['completed', 'failed']:
                    plan_path = p['path']
                    break
            # 如果都完成了，用最后一个
            if not plan_path:
                plan_path = plans[0]['path']
    
    if not plan_path or not os.path.exists(plan_path):
        print("📝 暂无任务计划")
        print("   创建新计划:")
        print("   python3 scripts/create-plan.py --task '任务描述' --steps 5")
        return
    
    plan = load_plan(plan_path)
    
    # 检查是否有正在运行的步骤
    running_steps = [s for s in plan['steps'] if s['status'] == 'running']
    if running_steps:
        print(f"⚠️  有步骤正在执行中:")
        for step in running_steps:
            print(f"   步骤 {step['id']}: {step['name']}")
        print(f"\n请等待当前步骤完成，或使用 status.py 查看进度")
        return
    
    # 找到下一步
    next_step = find_next_step(plan)
    if not next_step:
        print("✅ 所有步骤已完成！")
        return
    
    # 显示步骤信息
    print(f"\n📋 下一步: 步骤 {next_step['id']}")
    print(f"   名称: {next_step['name']}")
    print(f"   描述: {next_step['description']}")
    
    # 确认
    if not args.yes:
        confirm = input(f"\n是否执行? [Y/n]: ").strip().lower()
        if confirm and confirm not in ['y', 'yes']:
            print("已取消")
            return
    
    # 提示用户调用subAgent
    print(f"\n🚀 请执行以下命令启动步骤 {next_step['id']}:")
    print(f"   @executor 执行步骤{next_step['id']}")


if __name__ == '__main__':
    main()
