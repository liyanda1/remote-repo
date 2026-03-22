#!/usr/bin/env python3
"""
后台启动subAgent执行任务的脚本
用法: python run-background.py --plan ./plan.json --step 1
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime


def load_plan(plan_path):
    """加载任务计划"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_plan(plan_path, plan):
    """保存任务计划"""
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)


def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def update_step_status(plan, step_id, status, error=None):
    """更新步骤状态"""
    for step in plan['steps']:
        if step['id'] == step_id:
            step['status'] = status
            if status == 'running':
                step['started_at'] = datetime.now().isoformat()
            elif status in ['success', 'failed', 'cancelled']:
                step['completed_at'] = datetime.now().isoformat()
            if error:
                step['error'] = error
            break
    return plan


def run_subagent(plan_path, step_id, task_description, step_description):
    """
    启动subAgent在后台执行任务
    实际实现中，这里会调用OpenCode的subAgent机制
    """
    
    # 构建subAgent的prompt
    subagent_prompt = f"""
你是一个任务执行Agent，负责完成以下任务的一个步骤。

【整体任务】
{task_description}

【当前步骤】
步骤 {step_id}: {step_description}

【工作要求】
1. 专注于完成当前步骤，不要处理其他步骤
2. 执行完成后，必须更新状态文件
3. 如遇到问题，记录错误信息

【状态文件】
- 计划文件: {plan_path}
- 日志文件: ./.orchestrator/logs/step-{step_id}.log

【执行流程】
1. 读取并理解当前步骤的任务
2. 执行任务
3. 将执行结果写入日志文件
4. 更新计划文件中的步骤状态为 "success" 或 "failed"

请开始执行任务。
"""
    
    # 创建日志文件
    log_path = f"./.orchestrator/logs/step-{step_id}.log"
    ensure_dir(log_path)
    
    # 写入开始日志
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"[{datetime.now().isoformat()}] 步骤 {step_id} 开始执行\n")
        f.write(f"任务: {task_description}\n")
        f.write(f"步骤描述: {step_description}\n")
        f.write("=" * 50 + "\n")
    
    # 注意：这里是一个占位实现
    # 实际集成到OpenCode时，应该使用OpenCode的subAgent启动机制
    # 例如通过某种API或命令启动subAgent
    
    print(f"🚀 已启动subAgent执行步骤 {step_id}")
    print(f"   日志文件: {log_path}")
    print(f"\n在实际OpenCode环境中，这里会:")
    print(f"   1. 启动一个新的Agent实例")
    print(f"   2. 将上述prompt传递给subAgent")
    print(f"   3. subAgent在后台独立运行")
    print(f"   4. 主Agent可以通过status.py监控进度")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='后台启动subAgent执行任务')
    parser.add_argument('--plan', '-p', required=True, help='任务计划文件路径')
    parser.add_argument('--step', '-s', type=int, required=True, help='要执行的步骤ID')
    
    args = parser.parse_args()
    
    # 加载计划
    plan = load_plan(args.plan)
    
    # 找到指定步骤
    step = None
    for s in plan['steps']:
        if s['id'] == args.step:
            step = s
            break
    
    if not step:
        print(f"❌ 错误: 找不到步骤 {args.step}")
        sys.exit(1)
    
    if step['status'] == 'success':
        print(f"⚠️ 步骤 {args.step} 已经完成，跳过")
        sys.exit(0)
    
    # 更新步骤状态为running
    plan = update_step_status(plan, args.step, 'running')
    plan['current_step'] = args.step
    plan['overall_status'] = 'running'
    save_plan(args.plan, plan)
    
    # 启动subAgent
    success = run_subagent(
        args.plan,
        args.step,
        plan['task_description'],
        step['description']
    )
    
    if success:
        print(f"\n✅ 步骤 {args.step} 已提交给subAgent")
        print(f"   使用 'python3 scripts/status.py' 查看执行状态")
    else:
        print(f"\n❌ 启动subAgent失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
