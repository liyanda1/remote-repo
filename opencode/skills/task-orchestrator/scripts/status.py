#!/usr/bin/env python3
"""
查看任务执行状态的脚本
用法: python status.py [--plan ./plan.json]

自动从 ~/.config/opencode/task-orchestrator/ 读取状态
"""

import argparse
import json
import os
from datetime import datetime
from config import get_state_dir, get_plans_dir


def load_plan(plan_path):
    """加载任务计划"""
    if not os.path.exists(plan_path):
        return None
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_current_state():
    """加载当前状态"""
    state_path = os.path.join(get_state_dir(), "current.json")
    if not os.path.exists(state_path):
        return None
    with open(state_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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
                        'task_id': plan.get('task_id', 'unknown'),
                        'description': plan.get('task_description', '无描述')[:30],
                        'status': plan.get('overall_status', 'unknown')
                    })
            except:
                pass
    return plans


def format_duration(start, end=None):
    """格式化持续时间"""
    if not start:
        return "N/A"
    
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end) if end else datetime.now()
    
    duration = (end_dt - start_dt).total_seconds()
    
    if duration < 60:
        return f"{int(duration)}秒"
    elif duration < 3600:
        return f"{int(duration / 60)}分{int(duration % 60)}秒"
    else:
        return f"{int(duration / 3600)}时{int((duration % 3600) / 60)}分"


def get_status_icon(status):
    """获取状态图标"""
    icons = {
        'pending': '⏳',
        'running': '🔄',
        'success': '✅',
        'failed': '❌',
        'cancelled': '🚫'
    }
    return icons.get(status, '❓')


def display_status(plan):
    """显示任务状态"""
    print("=" * 60)
    print(f"📋 任务: {plan['task_description']}")
    print(f"🆔 任务ID: {plan['task_id']}")
    print(f"📅 创建时间: {plan['created_at']}")
    print("=" * 60)
    
    # 整体进度
    completed = sum(1 for s in plan['steps'] if s['status'] == 'success')
    total = len(plan['steps'])
    progress_pct = (completed / total) * 100 if total > 0 else 0
    
    print(f"\n📊 整体进度: {completed}/{total} ({progress_pct:.1f}%)")
    print(f"📌 整体状态: {get_status_icon(plan['overall_status'])} {plan['overall_status']}")
    
    # 各步骤详情
    print(f"\n📋 步骤详情:")
    print("-" * 60)
    
    for step in plan['steps']:
        icon = get_status_icon(step['status'])
        duration = ""
        
        if step['status'] == 'running':
            duration = f" (已运行 {format_duration(step['started_at'])})"
        elif step['status'] in ['success', 'failed']:
            duration = f" (耗时 {format_duration(step['started_at'], step['completed_at'])})"
        
        print(f"  {icon} 步骤 {step['id']}: {step['name']} - {step['status']}{duration}")
        
        if step['error']:
            print(f"     ⚠️ 错误: {step['error']}")
    
    # 下一步建议
    print(f"\n💡 下一步:")
    print("-" * 60)
    
    if plan['overall_status'] == 'completed':
        print("   ✅ 所有步骤已完成！")
    elif plan['overall_status'] == 'failed':
        failed_steps = [s for s in plan['steps'] if s['status'] == 'failed']
        print(f"   ❌ 有 {len(failed_steps)} 个步骤失败")
        for step in failed_steps:
            print(f"      重试步骤 {step['id']}: @executor 执行步骤{step['id']}")
    else:
        # 找到下一个待执行的步骤
        next_step = None
        for step in plan['steps']:
            if step['status'] == 'pending':
                next_step = step
                break
        
        if next_step:
            print(f"   ⏭️  执行下一步:")
            print(f"      @executor 执行步骤{next_step['id']}")
        else:
            print("   ⏳ 等待当前步骤完成...")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='查看任务执行状态')
    parser.add_argument('--plan', '-p', help='任务计划文件路径（可选）')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有任务')
    
    args = parser.parse_args()
    
    # 列出所有任务
    if args.list:
        plans = list_all_plans()
        if not plans:
            print("📝 暂无任务计划")
            return
        
        print("📋 所有任务:")
        print("-" * 60)
        for plan in plans:
            icon = get_status_icon(plan['status'])
            print(f"{icon} {plan['task_id']}: {plan['description']}... ({plan['status']})")
        return
    
    # 确定计划文件路径
    plan_path = args.plan
    if not plan_path:
        state = load_current_state()
        if state and 'active_plan' in state:
            plan_path = state['active_plan']
    
    if not plan_path or not os.path.exists(plan_path):
        # 尝试查找任何存在的计划
        plans = list_all_plans()
        if plans:
            plan_path = plans[0]['path']
        else:
            print("📝 暂无任务计划")
            print("   创建新计划:")
            print("   python3 scripts/create-plan.py --task '任务描述' --steps 5")
            return
    
    plan = load_plan(plan_path)
    if not plan:
        print(f"❌ 错误: 无法加载计划文件")
        return
    
    display_status(plan)


if __name__ == '__main__':
    main()
