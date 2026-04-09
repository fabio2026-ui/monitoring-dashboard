#!/usr/bin/env python3
"""
项目优先级管理系统
基于老板指令：记住所有项目，按优先级主动推进，减少提醒需求
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
import os

class ProjectPrioritySystem:
    """项目优先级管理系统"""
    
    def __init__(self, data_file: str = "project_priority_data.json"):
        self.data_file = data_file
        self.projects = self.load_projects()
        self.priority_rules = self.get_priority_rules()
        
    def load_projects(self) -> Dict[str, Any]:
        """加载项目数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.initialize_projects()
    
    def initialize_projects(self) -> Dict[str, Any]:
        """初始化15个项目数据"""
        projects = {
            "projects": {},
            "last_updated": datetime.now().isoformat(),
            "resource_allocation": {},
            "priority_history": []
        }
        
        # 15个项目定义
        project_definitions = [
            {
                "id": "ai_trading_signals",
                "name": "AI交易信号系统",
                "description": "机器学习驱动的交易信号和投资建议系统",
                "income_potential": 30000,  # 美元/月
                "tech_feasibility": 8,  # 1-10分
                "launch_speed": 7,  # 1-10分
                "market_competition": 6,  # 1-10分 (低分=竞争激烈)
                "synergy_effect": 9,  # 1-10分
                "current_status": "ready_to_start",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 0,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_token_platform",
                "name": "AI Token平台",
                "description": "AI代币交易和管理平台",
                "income_potential": 1000000,
                "tech_feasibility": 9,
                "launch_speed": 8,
                "market_competition": 7,
                "synergy_effect": 10,
                "current_status": "in_progress",
                "progress": 40,
                "resource_allocation": 12,
                "last_priority_score": 8.7,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "autocontent_factory",
                "name": "AutoContentFactory",
                "description": "全自动内容生成和分发系统",
                "income_potential": 5000000,
                "tech_feasibility": 8,
                "launch_speed": 9,
                "market_competition": 6,
                "synergy_effect": 9,
                "current_status": "in_progress",
                "progress": 35,
                "resource_allocation": 10,
                "last_priority_score": 8.5,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_digital_products",
                "name": "AI数字产品系统",
                "description": "AI生成和销售数字产品",
                "income_potential": 8000,
                "tech_feasibility": 9,
                "launch_speed": 9,
                "market_competition": 7,
                "synergy_effect": 8,
                "current_status": "ready_to_start",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 8.3,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "codegenius_ai",
                "name": "CodeGeniusAI",
                "description": "AI代码生成和理解引擎",
                "income_potential": 10000000,
                "tech_feasibility": 7,
                "launch_speed": 7,
                "market_competition": 5,
                "synergy_effect": 8,
                "current_status": "in_progress",
                "progress": 30,
                "resource_allocation": 9,
                "last_priority_score": 8.1,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "trendmaster_ai",
                "name": "TrendMasterAI",
                "description": "趋势预测和市场分析AI",
                "income_potential": 8000000,
                "tech_feasibility": 8,
                "launch_speed": 7,
                "market_competition": 6,
                "synergy_effect": 7,
                "current_status": "in_progress",
                "progress": 25,
                "resource_allocation": 8,
                "last_priority_score": 7.9,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "dataanalyst_ai",
                "name": "DataAnalyst AI",
                "description": "自动化数据分析和报告系统",
                "income_potential": 6000000,
                "tech_feasibility": 9,
                "launch_speed": 8,
                "market_competition": 7,
                "synergy_effect": 8,
                "current_status": "in_progress",
                "progress": 20,
                "resource_allocation": 7,
                "last_priority_score": 7.8,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "supportbot_ai",
                "name": "SupportBot AI",
                "description": "AI客户服务和对话引擎",
                "income_potential": 4000000,
                "tech_feasibility": 9,
                "launch_speed": 9,
                "market_competition": 8,
                "synergy_effect": 7,
                "current_status": "in_progress",
                "progress": 45,
                "resource_allocation": 6,
                "last_priority_score": 7.6,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_data_analysis_service",
                "name": "AI数据分析服务",
                "description": "企业级数据分析和咨询服务",
                "income_potential": 6000,
                "tech_feasibility": 8,
                "launch_speed": 6,
                "market_competition": 7,
                "synergy_effect": 6,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 7.5,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_education_content",
                "name": "AI教育内容系统",
                "description": "AI生成教育内容和学习路径",
                "income_potential": 10000,
                "tech_feasibility": 8,
                "launch_speed": 7,
                "market_competition": 6,
                "synergy_effect": 7,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 7.3,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_marketing_automation",
                "name": "AI营销自动化",
                "description": "多渠道营销自动化和客户旅程管理",
                "income_potential": 12000,
                "tech_feasibility": 7,
                "launch_speed": 6,
                "market_competition": 5,
                "synergy_effect": 8,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 7.1,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_health_consultation",
                "name": "AI健康咨询系统",
                "description": "个性化健康数据分析和建议",
                "income_potential": 15000,
                "tech_feasibility": 6,
                "launch_speed": 5,
                "market_competition": 4,
                "synergy_effect": 6,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 6.9,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_legal_documents",
                "name": "AI法律文档系统",
                "description": "法律文档生成和合规检查",
                "income_potential": 25000,
                "tech_feasibility": 5,
                "launch_speed": 4,
                "market_competition": 3,
                "synergy_effect": 5,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 6.7,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_real_estate_analysis",
                "name": "AI房地产分析",
                "description": "房产数据分析和投资建议",
                "income_potential": 40000,
                "tech_feasibility": 4,
                "launch_speed": 3,
                "market_competition": 2,
                "synergy_effect": 4,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 6.5,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ai_recruitment_matching",
                "name": "AI招聘匹配系统",
                "description": "简历分析和职位匹配算法",
                "income_potential": 20000,
                "tech_feasibility": 7,
                "launch_speed": 5,
                "market_competition": 4,
                "synergy_effect": 6,
                "current_status": "pending",
                "progress": 0,
                "resource_allocation": 0,
                "last_priority_score": 6.3,
                "created_at": datetime.now().isoformat()
            }
        ]
        
        for project in project_definitions:
            projects["projects"][project["id"]] = project
        
        self.save_projects(projects)
        return projects
    
    def get_priority_rules(self) -> Dict[str, float]:
        """获取优先级计算规则"""
        return {
            "income_weight": 0.35,
            "tech_weight": 0.25,
            "speed_weight": 0.20,
            "competition_weight": 0.10,
            "synergy_weight": 0.10
        }
    
    def calculate_priority_score(self, project: Dict[str, Any]) -> float:
        """计算项目优先级分数"""
        rules = self.priority_rules
        
        # 收入潜力评分 (0-10分)
        income_score = self.calculate_income_score(project["income_potential"])
        
        # 技术可行性 (1-10分)
        tech_score = project["tech_feasibility"]
        
        # 启动速度 (1-10分)
        speed_score = project["launch_speed"]
        
        # 市场竞争 (1-10分，低分=竞争激烈)
        competition_score = project["market_competition"]
        
        # 协同效应 (1-10分)
        synergy_score = project["synergy_effect"]
        
        # 计算加权分数
        priority_score = (
            income_score * rules["income_weight"] +
            tech_score * rules["tech_weight"] +
            speed_score * rules["speed_weight"] +
            competition_score * rules["competition_weight"] +
            synergy_score * rules["synergy_weight"]
        )
        
        return round(priority_score, 2)
    
    def calculate_income_score(self, income_potential: float) -> float:
        """根据收入潜力计算分数"""
        if income_potential < 10000:
            return 3.0
        elif income_potential < 50000:
            return 6.0
        else:
            return 10.0
    
    def update_all_priorities(self):
        """更新所有项目的优先级"""
        for project_id, project in self.projects["projects"].items():
            old_score = project.get("last_priority_score", 0)
            new_score = self.calculate_priority_score(project)
            
            project["last_priority_score"] = new_score
            project["last_updated"] = datetime.now().isoformat()
            
            # 记录优先级变化
            if old_score != new_score:
                self.projects["priority_history"].append({
                    "project_id": project_id,
                    "project_name": project["name"],
                    "old_score": old_score,
                    "new_score": new_score,
                    "timestamp": datetime.now().isoformat(),
                    "reason": "定期更新"
                })
        
        self.save_projects(self.projects)
    
    def get_priority_ranking(self) -> List[Dict[str, Any]]:
        """获取按优先级排序的项目列表"""
        projects_list = []
        for project_id, project in self.projects["projects"].items():
            projects_list.append({
                "id": project_id,
                "name": project["name"],
                "priority_score": project["last_priority_score"],
                "income_potential": project["income_potential"],
                "current_status": project["current_status"],
                "progress": project["progress"],
                "resource_allocation": project["resource_allocation"]
            })
        
        # 按优先级分数降序排序
        projects_list.sort(key=lambda x: x["priority_score"], reverse=True)
        return projects_list
    
    def allocate_resources(self, total_resources: int = 100):
        """基于优先级分配资源"""
        ranking = self.get_priority_ranking()
        
        # 按优先级分组
        high_priority = [p for p in ranking if p["priority_score"] >= 8.0]
        medium_priority = [p for p in ranking if 7.0 <= p["priority_score"] < 8.0]
        low_priority = [p for p in ranking if p["priority_score"] < 7.0]
        
        # 分配资源比例
        high_resources = int(total_resources * 0.40)
        medium_resources = int(total_resources * 0.35)
        low_resources = int(total_resources * 0.25)
        
        # 分配资源给高优先级项目
        if high_priority:
            resources_per_project = high_resources // len(high_priority)
            for project in high_priority:
                self.projects["projects"][project["id"]]["resource_allocation"] = resources_per_project
        
        # 分配资源给中优先级项目
        if medium_priority:
            resources_per_project = medium_resources // len(medium_priority)
            for project in medium_priority:
                self.projects["projects"][project["id"]]["resource_allocation"] = resources_per_project
        
        # 分配资源给低优先级项目
        if low_priority:
            resources_per_project = low_resources // len(low_priority)
            for project in low_priority:
                self.projects["projects"][project["id"]]["resource_allocation"] = resources_per_project
        
        # 更新资源分配记录
        self.projects["resource_allocation"] = {
            "high_priority": len(high_priority),
            "medium_priority": len(medium_priority),
            "low_priority": len(low_priority),
            "total_resources": total_resources,
            "last_allocated": datetime.now().isoformat()
        }
        
        self.save_projects(self.projects)
    
    def check_progress_vs_priority(self) -> List[Dict[str, Any]]:
        """检查进度是否符合优先级要求"""
        alerts = []
        
        for project_id, project in self.projects["projects"].items():
            priority_score = project["last_priority_score"]
            progress = project["progress"]
            status = project["current_status"]
            
            # 高优先级项目但进度缓慢
            if priority_score >= 8.0 and progress < 30 and status == "in_progress":
                alerts.append({
                    "project_id": project_id,
                    "project_name": project["name"],
                    "priority_score": priority_score,
                    "progress": progress,
                    "issue": "高优先级项目进度缓慢",
                    "severity": "high"
                })
            
            # 中优先级项目但未启动
            elif 7.0 <= priority_score < 8.0 and status == "pending":
                alerts.append({
                    "project_id": project_id,
                    "project_name": project["name"],
                    "priority_score": priority_score,
                    "progress": progress,
                    "issue": "中优先级项目未启动",
                    "severity": "medium"
                })
            
            # 资源分配与优先级不匹配
            resource_allocation = project["resource_allocation"]
            expected_resource = self.get_expected_resource(priority_score)
            
            if abs(resource_allocation - expected_resource) > 5:
                alerts.append({
                    "project_id": project_id,
                    "project_name": project["name"],
                    "priority_score": priority_score,
                    "current_resource": resource_allocation,
                    "expected_resource": expected_resource,
                    "issue": "资源分配与优先级不匹配",
                    "severity": "medium"
                })
        
        return alerts
    
    def get_expected_resource(self, priority_score: float) -> int:
        """根据优先级分数获取期望资源分配"""
        if priority_score >= 8.0:
            return 12  # 高优先级
        elif priority_score >= 7.0:
            return 8   # 中优先级
        else:
            return 4   # 低优先级
    
    def save_projects(self, data: Dict[str, Any]):
        """保存项目数据"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_dashboard_report(self, minimal: bool = False) -> Dict[str, Any]:
        """生成仪表板报告
        
        Args:
            minimal: 是否生成最小化报告（减少频率时使用）
        """
        ranking = self.get_priority_ranking()
        alerts = self.check_progress_vs_priority()
        
        # 统计信息
        total_projects = len(self.projects["projects"])
        in_progress = len([p for p in self.projects["projects"].values() if p["current_status"] == "in_progress"])
        ready_to_start = len([p for p in self.projects["projects"].values() if p["current_status"] == "ready_to_start"])
        pending = len([p for p in self.projects["projects"].values() if p["current_status"] == "pending"])
        
        # 收入潜力统计
        total_income_potential = sum(p["income_potential"] for p in self.projects["projects"].values())
        active_income_potential = sum(p["income_potential"] for p in self.projects["projects"].values() 
                                     if p["current_status"] == "in_progress")
        
        # 最小化报告 - 只包含关键信息
        if minimal:
            report = {
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_projects": total_projects,
                    "in_progress": in_progress,
                    "ready_to_start": ready_to_start,
                    "pending": pending
                },
                "priority_ranking": ranking[:3],  # 只显示前3名
                "critical_alerts": [a for a in alerts if a["severity"] == "high"],  # 只显示高严重性警报
                "status": "minimal_report"
            }
        else:
            # 完整报告
            report = {
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_projects": total_projects,
                    "in_progress": in_progress,
                    "ready_to_start": ready_to_start,
                    "pending": pending,
                    "total_income_potential": f"${total_income_potential:,}/月",
                    "active_income_potential": f"${active_income_potential:,}/月"
                },
                "priority_ranking": ranking[:10],  # 前10名
                "alerts": alerts,
                "resource_allocation": self.projects.get("resource_allocation", {}),
                "recommendations": self.generate_recommendations(),
                "status": "full_report"
            }
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """生成推荐行动"""
        recommendations = []
        ranking = self.get_priority_ranking()
        
        # 检查高优先级但未启动的项目
        high_priority_pending = [
            p for p in ranking 
            if p["priority_score"] >= 8.0 and p["current_status"] in ["ready_to_start", "pending"]
        ]
        
        if high_priority_pending:
            for project in high_priority_pending[:2]:  # 前2个
                recommendations.append(
                    f"立即启动: {project['name']} (优先级: {project['priority_score']}, "
                    f"收入潜力: ${project['income_potential']:,}/月)"
                )
        
        # 检查进度缓慢的高优先级项目
        high_priority_slow = [
            p for p in ranking 
            if p["priority_score"] >= 8.0 and p["current_status"] == "in_progress" and p["progress"] < 40
        ]
        
        if high_priority_slow:
            for project in high_priority_slow[:2]:
                recommendations.append(
                    f"加速推进: {project['name']} (当前进度: {project['progress']}%, "
                    f"优先级: {project['priority_score']})"
                )
        
        # 检查资源分配问题
        alerts = self.check_progress_vs_priority()
        resource_alerts = [a for a in alerts if "资源分配" in a["issue"]]
        
        if resource_alerts:
            for alert in resource_alerts[:3]:
                recommendations.append(
                    f"调整资源: {alert['project_name']} (当前: {alert['current_resource']}%, "
                    f"期望: {alert['expected_resource']}%)"
                )
        
        # 如果没有推荐，添加默认推荐
        if not recommendations:
            recommendations.append("所有项目按优先级正常推进，继续保持当前节奏")
        
        return recommendations
    
    def update_project_progress(self, project_id: str, progress: int, status: str = None):
        """更新项目进度"""
        if project_id in self.projects["projects"]:
            project = self.projects["projects"][project_id]
            project["progress"] = progress
            project["last_updated"] = datetime.now().isoformat()
            
            if status:
                project["current_status"] = status
            
            # 重新计算优先级
            new_score = self.calculate_priority_score(project)
            old_score = project.get("last_priority_score", 0)
            project["last_priority_score"] = new_score
            
            # 记录变化
            if old_score != new_score:
                self.projects["priority_history"].append({
                    "project_id": project_id,
                    "project_name": project["name"],
                    "old_score": old_score,
                    "new_score": new_score,
                    "timestamp": datetime.now().isoformat(),
                    "reason": f"进度更新: {progress}%"
                })
            
            self.save_projects(self.projects)
            return True
        return False


def main(minimal: bool = False):
    """主函数
    
    Args:
        minimal: 是否生成最小化报告（减少频率时使用）
    """
    if minimal:
        print("📊 项目状态快速检查")
        print("=" * 30)
    else:
        print("🚀 项目优先级管理系统启动")
        print("=" * 50)
    
    # 初始化系统
    priority_system = ProjectPrioritySystem()
    
    # 更新所有优先级
    priority_system.update_all_priorities()
    
    # 分配资源
    priority_system.allocate_resources(total_resources=100)
    
    # 生成报告
    report = priority_system.generate_dashboard_report(minimal=minimal)
    
    if minimal:
        # 最小化报告 - 只显示关键信息
        print(f"📊 快速概览:")
        print(f"  总项目: {report['summary']['total_projects']} | 进行中: {report['summary']['in_progress']}")
        print(f"  准备启动: {report['summary']['ready_to_start']} | 待启动: {report['summary']['pending']}")
        
        print(f"\n🏆 优先级前三:")
        for i, project in enumerate(report['priority_ranking'], 1):
            status_emoji = "✅" if project["current_status"] == "in_progress" else "🔄"
            print(f"  {i}. {project['name']} {status_emoji}")
            print(f"     优先级: {project['priority_score']} | 进度: {project['progress']}%")
        
        if report.get('critical_alerts'):
            print(f"\n🚨 关键警报 ({len(report['critical_alerts'])}个):")
            for alert in report['critical_alerts'][:2]:
                print(f"  • {alert['project_name']}: {alert['issue']}")
        else:
            print(f"\n✅ 无关键警报")
        
        print(f"\n📅 检查时间: {datetime.now().strftime('%H:%M')}")
        print("=" * 30)
        
    else:
        # 完整报告
        print(f"📊 系统概览:")
        print(f"  总项目数: {report['summary']['total_projects']}")
        print(f"  进行中: {report['summary']['in_progress']}")
        print(f"  准备启动: {report['summary']['ready_to_start']}")
        print(f"  待启动: {report['summary']['pending']}")
        print(f"  总收入潜力: {report['summary']['total_income_potential']}")
        print(f"  活跃项目收入潜力: {report['summary']['active_income_potential']}")
        
        print(f"\n🏆 优先级排名 (前5名):")
        for i, project in enumerate(report['priority_ranking'][:5], 1):
            status_emoji = "✅" if project["current_status"] == "in_progress" else "🔄"
            print(f"  {i}. {project['name']} {status_emoji}")
            print(f"     优先级: {project['priority_score']} | 收入: ${project['income_potential']:,}/月")
            print(f"     状态: {project['current_status']} | 进度: {project['progress']}%")
        
        if report['alerts']:
            print(f"\n⚠️  需要关注的警报 ({len(report['alerts'])}个):")
            for alert in report['alerts'][:3]:
                severity_emoji = "🚨" if alert["severity"] == "high" else "⚠️"
                print(f"  {severity_emoji} {alert['project_name']}: {alert['issue']}")
        
        print(f"\n💡 推荐行动:")
        for i, recommendation in enumerate(report['recommendations'], 1):
            print(f"  {i}. {recommendation}")
        
        print(f"\n📈 资源分配:")
        alloc = report['resource_allocation']
        print(f"  高优先级项目: {alloc.get('high_priority', 0)}个 (40%资源)")
        print(f"  中优先级项目: {alloc.get('medium_priority', 0)}个 (35%资源)")
        print(f"  低优先级项目: {alloc.get('low_priority', 0)}个 (25%资源)")
        
        print(f"\n✅ 系统状态: 优先级管理已启用")
        print(f"📅 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)


if __name__ == "__main__":
    main()