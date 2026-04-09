#!/usr/bin/env python3
"""
报告调度系统
根据老板要求减少报告频率，智能调度报告生成
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any
import os
import subprocess

class ReportScheduler:
    """报告调度系统"""
    
    def __init__(self, schedule_file: str = "report_schedule.json"):
        self.schedule_file = schedule_file
        self.schedule = self.load_schedule()
        
    def load_schedule(self) -> Dict[str, Any]:
        """加载调度配置"""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.default_schedule()
    
    def default_schedule(self) -> Dict[str, Any]:
        """默认调度配置"""
        return {
            "schedule": {
                "full_reports": [
                    {"time": "09:00", "enabled": True},
                    {"time": "18:00", "enabled": True}
                ],
                "minimal_reports": [
                    {"time": "03:00", "enabled": True},
                    {"time": "09:00", "enabled": True},
                    {"time": "15:00", "enabled": True},
                    {"time": "21:00", "enabled": True}
                ],
                "critical_checks": [
                    {"interval_minutes": 30, "enabled": True}
                ]
            },
            "last_executions": {},
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
    
    def should_run_report(self, report_type: str, schedule_time: str = None) -> bool:
        """判断是否应该运行报告"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # 获取上次执行时间
        last_exec_key = f"{report_type}_{schedule_time}" if schedule_time else report_type
        last_execution = self.schedule["last_executions"].get(last_exec_key)
        
        if report_type == "full":
            # 完整报告：检查是否到预定时间
            if schedule_time and current_time == schedule_time:
                if last_execution:
                    last_time = datetime.fromisoformat(last_execution)
                    # 确保今天还没执行过这个时间点的报告
                    if last_time.date() == now.date():
                        return False
                return True
                
        elif report_type == "minimal":
            # 最小化报告：检查是否到预定时间
            if schedule_time and current_time == schedule_time:
                if last_execution:
                    last_time = datetime.fromisoformat(last_execution)
                    # 确保至少6小时间隔
                    hours_since = (now - last_time).total_seconds() / 3600
                    if hours_since < 6:
                        return False
                return True
                
        elif report_type == "critical":
            # 关键检查：检查时间间隔
            if last_execution:
                last_time = datetime.fromisoformat(last_execution)
                minutes_since = (now - last_time).total_seconds() / 60
                if minutes_since < 30:  # 30分钟间隔
                    return False
            return True
        
        return False
    
    def record_execution(self, report_type: str, schedule_time: str = None):
        """记录执行时间"""
        now = datetime.now()
        exec_key = f"{report_type}_{schedule_time}" if schedule_time else report_type
        self.schedule["last_executions"][exec_key] = now.isoformat()
        self.save_schedule()
    
    def run_full_report(self):
        """运行完整报告"""
        print(f"⏰ [{datetime.now().strftime('%H:%M')}] 运行完整报告...")
        try:
            result = subprocess.run(
                ["python3", "project_priority_system.py"],
                capture_output=True,
                text=True,
                cwd="/home/node/.openclaw/workspace"
            )
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  警告: {result.stderr}")
        except Exception as e:
            print(f"❌ 运行完整报告失败: {e}")
    
    def run_minimal_report(self):
        """运行最小化报告"""
        print(f"⏰ [{datetime.now().strftime('%H:%M')}] 运行最小化报告...")
        try:
            result = subprocess.run(
                ["python3", "reduced_report_system.py"],
                capture_output=True,
                text=True,
                cwd="/home/node/.openclaw/workspace"
            )
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  警告: {result.stderr}")
        except Exception as e:
            print(f"❌ 运行最小化报告失败: {e}")
    
    def run_critical_check(self):
        """运行关键检查"""
        print(f"⏰ [{datetime.now().strftime('%H:%M')}] 运行关键检查...")
        try:
            # 导入优先级系统进行检查
            from project_priority_system import ProjectPrioritySystem
            priority_system = ProjectPrioritySystem()
            alerts = priority_system.check_progress_vs_priority()
            
            critical_alerts = [a for a in alerts if a["severity"] == "high"]
            
            if critical_alerts:
                print("🚨 发现关键警报，需要立即报告!")
                for alert in critical_alerts[:3]:
                    print(f"  • {alert['project_name']}: {alert['issue']}")
                # 这里可以添加通知逻辑
            else:
                print("✅ 无关键警报")
                
        except ImportError:
            print("⚠️  无法导入优先级系统")
        except Exception as e:
            print(f"❌ 运行关键检查失败: {e}")
    
    def check_and_run_scheduled_reports(self):
        """检查并运行预定报告"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        print(f"📅 报告调度检查 [{current_time}]")
        print("=" * 40)
        
        # 检查完整报告
        for schedule in self.schedule["schedule"]["full_reports"]:
            if schedule["enabled"] and self.should_run_report("full", schedule["time"]):
                print(f"✅ 计划执行完整报告 ({schedule['time']})")
                self.run_full_report()
                self.record_execution("full", schedule["time"])
                break  # 一次只执行一个报告
        
        # 检查最小化报告
        for schedule in self.schedule["schedule"]["minimal_reports"]:
            if schedule["enabled"] and self.should_run_report("minimal", schedule["time"]):
                print(f"✅ 计划执行最小化报告 ({schedule['time']})")
                self.run_minimal_report()
                self.record_execution("minimal", schedule["time"])
                break
        
        # 检查关键检查
        if self.should_run_report("critical"):
            print(f"✅ 执行关键检查")
            self.run_critical_check()
            self.record_execution("critical")
        
        print(f"\n📊 调度状态:")
        print(f"  完整报告次数: {len([k for k in self.schedule['last_executions'] if k.startswith('full_')])}")
        print(f"  最小化报告次数: {len([k for k in self.schedule['last_executions'] if k.startswith('minimal_')])}")
        print(f"  关键检查次数: {self.schedule['last_executions'].get('critical_count', 0)}")
        print("=" * 40)
    
    def save_schedule(self):
        """保存调度配置"""
        with open(self.schedule_file, 'w', encoding='utf-8') as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=2)
    
    def print_schedule(self):
        """打印调度配置"""
        print("📅 报告调度配置")
        print("=" * 40)
        
        schedule = self.schedule["schedule"]
        
        print("完整报告时间:")
        for s in schedule["full_reports"]:
            status = "✅" if s["enabled"] else "❌"
            print(f"  {status} {s['time']}")
        
        print("\n最小化报告时间:")
        for s in schedule["minimal_reports"]:
            status = "✅" if s["enabled"] else "❌"
            print(f"  {status} {s['time']}")
        
        print("\n关键检查:")
        for s in schedule["critical_checks"]:
            status = "✅" if s["enabled"] else "❌"
            print(f"  {status} 每{s['interval_minutes']}分钟")
        
        print(f"\n📊 执行记录:")
        for key, time_str in list(self.schedule["last_executions"].items())[:5]:
            time_obj = datetime.fromisoformat(time_str)
            print(f"  {key}: {time_obj.strftime('%Y-%m-%d %H:%M')}")
        
        print("=" * 40)


def main():
    """主函数"""
    print("🚀 报告调度系统启动")
    print("=" * 40)
    
    # 初始化调度系统
    scheduler = ReportScheduler()
    
    # 打印当前调度
    scheduler.print_schedule()
    
    # 检查并运行预定报告
    scheduler.check_and_run_scheduled_reports()
    
    print(f"\n✅ 调度系统状态: 运行中")
    print(f"📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)


if __name__ == "__main__":
    main()