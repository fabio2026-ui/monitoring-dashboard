#!/usr/bin/env python3
"""
简化报告系统
老板要求：减少系统健康报告频率
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class ReducedReportSystem:
    """简化报告系统"""
    
    def __init__(self, config_file: str = "report_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.last_report_time = self.config.get("last_report_time")
        self.report_count = self.config.get("report_count", 0)
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.default_config()
    
    def default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "report_frequency": "reduced",  # reduced, minimal, critical_only
            "daily_report_limit": 2,  # 每天最多2次完整报告
            "minimal_report_interval_hours": 6,  # 最小化报告间隔6小时
            "critical_alerts_only": True,  # 只报告关键警报
            "last_report_time": None,
            "report_count": 0,
            "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat()
        }
    
    def should_generate_report(self, report_type: str = "full") -> bool:
        """判断是否应该生成报告"""
        now = datetime.now()
        
        # 检查日期重置
        current_date = now.strftime("%Y-%m-%d")
        if self.config.get("last_reset_date") != current_date:
            self.config["last_reset_date"] = current_date
            self.config["report_count"] = 0
            self.save_config()
        
        # 根据报告类型判断
        if report_type == "full":
            # 完整报告：每天最多2次
            if self.config["report_count"] >= self.config["daily_report_limit"]:
                return False
            
            # 检查时间间隔
            if self.last_report_time:
                last_time = datetime.fromisoformat(self.last_report_time)
                hours_since_last = (now - last_time).total_seconds() / 3600
                if hours_since_last < 6:  # 至少6小时间隔
                    return False
            
            return True
            
        elif report_type == "minimal":
            # 最小化报告：每6小时一次
            if self.last_report_time:
                last_time = datetime.fromisoformat(self.last_report_time)
                hours_since_last = (now - last_time).total_seconds() / 3600
                if hours_since_last < self.config["minimal_report_interval_hours"]:
                    return False
            return True
            
        elif report_type == "critical":
            # 关键警报：总是报告
            return True
        
        return False
    
    def record_report_generated(self, report_type: str = "full"):
        """记录报告生成"""
        now = datetime.now()
        self.config["last_report_time"] = now.isoformat()
        
        if report_type == "full":
            self.config["report_count"] += 1
        
        self.save_config()
    
    def generate_minimal_report(self, priority_system) -> Dict[str, Any]:
        """生成最小化报告"""
        ranking = priority_system.get_priority_ranking()
        alerts = priority_system.check_progress_vs_priority()
        
        # 只获取关键警报
        critical_alerts = [a for a in alerts if a["severity"] == "high"]
        
        # 统计信息
        total_projects = len(priority_system.projects["projects"])
        in_progress = len([p for p in priority_system.projects["projects"].values() 
                          if p["current_status"] == "in_progress"])
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "report_type": "minimal",
            "summary": {
                "total_projects": total_projects,
                "in_progress": in_progress,
                "critical_alerts_count": len(critical_alerts)
            },
            "top_projects": ranking[:3],
            "critical_alerts": critical_alerts[:2] if critical_alerts else [],
            "status": "all_ok" if not critical_alerts else "critical_alerts_present"
        }
        
        return report
    
    def generate_critical_report(self, priority_system) -> Dict[str, Any]:
        """生成关键警报报告"""
        alerts = priority_system.check_progress_vs_priority()
        critical_alerts = [a for a in alerts if a["severity"] == "high"]
        
        if not critical_alerts:
            return None
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "report_type": "critical",
            "critical_alerts": critical_alerts,
            "total_critical": len(critical_alerts),
            "urgent_action_required": True
        }
        
        return report
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def print_report(self, report: Dict[str, Any]):
        """打印报告"""
        if not report:
            return
        
        report_type = report.get("report_type", "unknown")
        
        if report_type == "minimal":
            print("📊 项目状态快速检查")
            print("=" * 30)
            
            summary = report["summary"]
            print(f"总项目: {summary['total_projects']} | 进行中: {summary['in_progress']}")
            
            if report["top_projects"]:
                print(f"\n🏆 优先级前三:")
                for i, project in enumerate(report["top_projects"], 1):
                    status_emoji = "✅" if project["current_status"] == "in_progress" else "🔄"
                    print(f"  {i}. {project['name']} {status_emoji}")
                    print(f"     优先级: {project['priority_score']} | 进度: {project['progress']}%")
            
            if report["critical_alerts"]:
                print(f"\n🚨 关键警报 ({len(report['critical_alerts'])}个):")
                for alert in report["critical_alerts"]:
                    print(f"  • {alert['project_name']}: {alert['issue']}")
            else:
                print(f"\n✅ 无关键警报")
            
            print(f"\n📅 检查时间: {datetime.now().strftime('%H:%M')}")
            print("=" * 30)
            
        elif report_type == "critical":
            print("🚨 紧急警报报告")
            print("=" * 40)
            
            print(f"发现 {report['total_critical']} 个关键问题需要立即关注:")
            
            for i, alert in enumerate(report["critical_alerts"], 1):
                print(f"\n{i}. {alert['project_name']}")
                print(f"   问题: {alert['issue']}")
                print(f"   优先级: {alert['priority_score']}")
                print(f"   当前进度: {alert['progress']}%")
            
            print(f"\n⚠️  需要立即采取行动!")
            print("=" * 40)
            
        elif report_type == "full":
            # 完整报告由主系统处理
            pass


def main():
    """主函数 - 简化报告系统"""
    print("📊 简化报告系统启动")
    print("=" * 40)
    
    # 初始化系统
    report_system = ReducedReportSystem()
    
    # 检查配置
    print(f"报告频率: {report_system.config['report_frequency']}")
    print(f"每日完整报告限制: {report_system.config['daily_report_limit']}次")
    print(f"最小化报告间隔: {report_system.config['minimal_report_interval_hours']}小时")
    print(f"只报告关键警报: {report_system.config['critical_alerts_only']}")
    
    # 检查是否应该生成报告
    if report_system.should_generate_report("minimal"):
        print(f"\n✅ 可以生成最小化报告")
        
        # 导入优先级系统
        try:
            from project_priority_system import ProjectPrioritySystem
            priority_system = ProjectPrioritySystem()
            
            # 生成最小化报告
            report = report_system.generate_minimal_report(priority_system)
            report_system.print_report(report)
            
            # 记录报告生成
            report_system.record_report_generated("minimal")
            
        except ImportError:
            print("⚠️  无法导入优先级系统")
            
    else:
        print(f"\n⏸️  未到报告时间")
        if report_system.last_report_time:
            last_time = datetime.fromisoformat(report_system.last_report_time)
            now = datetime.now()
            hours_since = (now - last_time).total_seconds() / 3600
            print(f"上次报告: {last_time.strftime('%H:%M')} ({hours_since:.1f}小时前)")
    
    print(f"\n📅 系统状态: 简化报告模式已启用")
    print(f"最后重置: {report_system.config.get('last_reset_date', 'N/A')}")
    print(f"今日报告次数: {report_system.config.get('report_count', 0)}")
    print("=" * 40)


if __name__ == "__main__":
    main()