#!/usr/bin/env python3
"""
清理临时文件脚本
用法: python cleanup.py [--plan ./plan.json] [--force] [--all]

默认清理 ~/.config/opencode/task-orchestrator/ 下的临时文件
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from config import get_orchestrator_dir, get_plans_dir


def load_plan(plan_path):
    """加载任务计划"""
    if not os.path.exists(plan_path):
        return None
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def should_cleanup(plan):
    """判断是否应该清理"""
    cleanup = plan.get('metadata', {}).get('cleanup', 'auto')
    
    if cleanup == 'keep':
        return False
    
    if cleanup == 'auto':
        overall_status = plan.get('overall_status', '')
        return overall_status in ['completed', 'failed', 'cancelled']
    
    return None


def cleanup_orchestrator_dir(force=False, all_tasks=False):
    """清理临时文件目录"""
    orch_dir = get_orchestrator_dir()
    
    if not os.path.exists(orch_dir):
        print("📝 临时目录不存在，无需清理")
        return True
    
    if all_tasks:
        # 清理所有任务
        if not force:
            confirm = input(f"确认删除所有任务数据? [y/N]: ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("已取消")
                return False
        
        try:
            shutil.rmtree(orch_dir)
            print(f"✅ 已清理所有任务数据")
            return True
        except Exception as e:
            print(f"❌ 清理失败: {e}")
            return False
    else:
        # 只清理已完成的任务
        plans_dir = get_plans_dir()
        if not os.path.exists(plans_dir):
            print("📝 无任务数据需要清理")
            return True
        
        cleaned = 0
        for f in os.listdir(plans_dir):
            if f.endswith('.json'):
                plan_path = os.path.join(plans_dir, f)
                try:
                    plan = load_plan(plan_path)
                    if plan and should_cleanup(plan):
                        os.remove(plan_path)
                        cleaned += 1
                except:
                    pass
        
        if cleaned > 0:
            print(f"✅ 已清理 {cleaned} 个已完成的任务")
        else:
            print("📝 没有需要清理的已完成任务")
        return True


def main():
    parser = argparse.ArgumentParser(description='清理临时文件')
    parser.add_argument('--plan', '-p', help='任务计划文件路径')
    parser.add_argument('--force', '-f', action='store_true', help='强制清理，不提示确认')
    parser.add_argument('--all', '-a', action='store_true', help='清理所有任务数据')
    
    args = parser.parse_args()
    
    cleanup_orchestrator_dir(force=args.force, all_tasks=args.all)


if __name__ == '__main__':
    main()
