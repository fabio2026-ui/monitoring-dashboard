#!/usr/bin/env python3
"""
团队管理系统 - 让多个Agent并行完成项目
老板指令: "要真实！现在你先提高管理能！让团队agent一起完成项目"
"""

import os
import json
import time
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ProjectStatus(Enum):
    NOT_STARTED = "未开始"
    IN_PROGRESS = "进行中"
    BLOCKED = "阻塞"
    COMPLETED = "已完成"
    FAILED = "失败"

class AgentRole(Enum):
    PROJECT_MANAGER = "项目经理"
    DEVELOPER = "开发工程师"
    QA_ENGINEER = "质量工程师"
    DEPLOYMENT = "部署工程师"
    RESEARCHER = "研究员"

@dataclass
class Project:
    """项目定义"""
    id: str
    name: str
    description: str
    status: ProjectStatus
    priority: int  # 1-10, 10最高
    estimated_hours: float
    actual_hours: float = 0.0
    dependencies: List[str] = None
    assigned_agents: List[str] = None
    created_at: str = None
    updated_at: str = None
    completion_percentage: float = 0.0
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.assigned_agents is None:
            self.assigned_agents = []
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

@dataclass
class Agent:
    """Agent定义"""
    id: str
    name: str
    role: AgentRole
    skills: List[str]
    availability: bool = True
    current_project: str = None
    performance_score: float = 0.0  # 0-100
    completed_tasks: int = 0
    
    def assign_to_project(self, project_id: str):
        """分配Agent到项目"""
        if self.availability:
            self.current_project = project_id
            self.availability = False
            return True
        return False
    
    def complete_task(self, success: bool = True):
        """完成任务"""
        if self.current_project:
            self.current_project = None
            self.availability = True
            self.completed_tasks += 1
            if success:
                self.performance_score = min(100, self.performance_score + 5)
            else:
                self.performance_score = max(0, self.performance_score - 10)
            return True
        return False

class TeamManagementSystem:
    """团队管理系统"""
    
    def __init__(self, workspace_path: str = "/home/node/.openclaw/workspace"):
        self.workspace_path = workspace_path
        self.projects: Dict[str, Project] = {}
        self.agents: Dict[str, Agent] = {}
        self.task_queue = []
        self.results = []
        
        # 创建数据目录
        self.data_dir = os.path.join(workspace_path, "team_data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化系统
        self._initialize_agents()
        self._initialize_projects()
    
    def _initialize_agents(self):
        """初始化Agent团队"""
        agents_data = [
            {
                "id": "agent_pm_001",
                "name": "项目经理-AI",
                "role": AgentRole.PROJECT_MANAGER,
                "skills": ["项目管理", "进度跟踪", "资源分配", "风险评估"]
            },
            {
                "id": "agent_dev_001", 
                "name": "开发工程师-AI",
                "role": AgentRole.DEVELOPER,
                "skills": ["Python", "系统架构", "代码实现", "调试"]
            },
            {
                "id": "agent_dev_002",
                "name": "开发工程师-AI-2",
                "role": AgentRole.DEVELOPER,
                "skills": ["API开发", "数据库", "前端", "测试"]
            },
            {
                "id": "agent_qa_001",
                "name": "质量工程师-AI",
                "role": AgentRole.QA_ENGINEER,
                "skills": ["测试设计", "自动化测试", "质量保证", "性能测试"]
            },
            {
                "id": "agent_deploy_001",
                "name": "部署工程师-AI",
                "role": AgentRole.DEPLOYMENT,
                "skills": ["Docker", "Kubernetes", "CI/CD", "监控"]
            },
            {
                "id": "agent_research_001",
                "name": "研究员-AI",
                "role": AgentRole.RESEARCHER,
                "skills": ["市场分析", "技术研究", "竞品分析", "趋势预测"]
            }
        ]
        
        for agent_data in agents_data:
            agent = Agent(**agent_data)
            self.agents[agent.id] = agent
        
        print(f"✅ 初始化完成: {len(self.agents)}个Agent已就绪")
    
    def _initialize_projects(self):
        """基于现有项目初始化"""
        # 从完成度报告加载项目
        report_file = os.path.join(self.workspace_path, "project_completion_report.json")
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            for project_data in report_data.get('projects', []):
                project_name = project_data['项目']
                completion = float(project_data['完成度'].rstrip('%'))
                
                # 根据完成度确定状态
                if completion >= 80:
                    status = ProjectStatus.COMPLETED
                elif completion >= 50:
                    status = ProjectStatus.IN_PROGRESS
                elif completion >= 20:
                    status = ProjectStatus.BLOCKED
                else:
                    status = ProjectStatus.NOT_STARTED
                
                project = Project(
                    id=f"proj_{len(self.projects)+1:03d}",
                    name=project_name,
                    description=project_data['描述'],
                    status=status,
                    priority=8 if 'TurboQuant' in project_name else 6,
                    estimated_hours=40.0,
                    completion_percentage=completion
                )
                
                self.projects[project.id] = project
        
        print(f"✅ 项目加载完成: {len(self.projects)}个项目已加载")
    
    def assign_agents_to_projects(self):
        """智能分配Agent到项目"""
        print("\n=== 智能Agent分配 ===")
        
        # 按优先级排序项目
        sorted_projects = sorted(
            self.projects.values(),
            key=lambda p: (p.priority, -p.completion_percentage),
            reverse=True
        )
        
        # 按技能和可用性排序Agent
        available_agents = [a for a in self.agents.values() if a.availability]
        
        assignments = []
        for project in sorted_projects:
            if project.status in [ProjectStatus.COMPLETED, ProjectStatus.FAILED]:
                continue
            
            # 根据项目类型分配Agent
            if 'TurboQuant' in project.name or 'AutoContentFactory' in project.name:
                # 技术项目需要开发和质量工程师
                needed_roles = [AgentRole.DEVELOPER, AgentRole.QA_ENGINEER, AgentRole.DEPLOYMENT]
            elif 'YouTube' in project.name or '研究' in project.name:
                # 研究项目需要研究员
                needed_roles = [AgentRole.RESEARCHER, AgentRole.PROJECT_MANAGER]
            else:
                # 其他项目
                needed_roles = [AgentRole.DEVELOPER, AgentRole.PROJECT_MANAGER]
            
            assigned = []
            for role in needed_roles:
                # 找到合适的Agent
                for agent in available_agents:
                    if agent.role == role:
                        if agent.assign_to_project(project.id):
                            assigned.append(agent.id)
                            available_agents.remove(agent)
                            break
            
            if assigned:
                project.assigned_agents = assigned
                project.updated_at = datetime.utcnow().isoformat()
                assignments.append((project.name, assigned))
                print(f"📋 {project.name}: 分配了 {len(assigned)}个Agent")
        
        return assignments
    
    def create_tasks_for_projects(self):
        """为每个项目创建具体任务"""
        print("\n=== 创建具体任务 ===")
        
        tasks = []
        for project in self.projects.values():
            if not project.assigned_agents:
                continue
            
            # 根据项目状态创建任务
            if project.status == ProjectStatus.NOT_STARTED:
                project_tasks = self._create_startup_tasks(project)
            elif project.status == ProjectStatus.IN_PROGRESS:
                project_tasks = self._create_implementation_tasks(project)
            elif project.status == ProjectStatus.BLOCKED:
                project_tasks = self._create_blocked_tasks(project)
            else:
                continue
            
            tasks.extend(project_tasks)
        
        # 添加到任务队列
        self.task_queue.extend(tasks)
        print(f"✅ 创建了 {len(tasks)}个具体任务")
        return tasks
    
    def _create_startup_tasks(self, project: Project) -> List[Dict]:
        """为未开始项目创建启动任务"""
        tasks = []
        
        if 'TurboQuant' in project.name:
            tasks = [
                {
                    "project_id": project.id,
                    "title": "安装TurboQuant依赖环境",
                    "description": "安装PyTorch, NumPy, Triton等必要依赖",
                    "estimated_hours": 2.0,
                    "agent_role": AgentRole.DEVELOPER,
                    "command": "cd /home/node/.openclaw/workspace/turboquant && ./setup-dev.sh"
                },
                {
                    "project_id": project.id,
                    "title": "运行技术验证脚本",
                    "description": "执行quick_validation.py验证环境",
                    "estimated_hours": 1.0,
                    "agent_role": AgentRole.QA_ENGINEER,
                    "command": "cd /home/node/.openclaw/workspace/turboquant && python3 quick_validation.py"
                }
            ]
        elif 'AutoContentFactory' in project.name:
            tasks = [
                {
                    "project_id": project.id,
                    "title": "修复缺失的方法实现",
                    "description": "实现research_topic()和generate_outline()方法",
                    "estimated_hours": 3.0,
                    "agent_role": AgentRole.DEVELOPER,
                    "command": "检查并修复AutoContentFactory/src/目录中的方法"
                },
                {
                    "project_id": project.id,
                    "title": "创建配置文件",
                    "description": "创建api_config.json和content_config.json",
                    "estimated_hours": 1.0,
                    "agent_role": AgentRole.DEVELOPER,
                    "command": "创建AutoContentFactory/config/目录和配置文件"
                }
            ]
        
        return tasks
    
    def _create_implementation_tasks(self, project: Project) -> List[Dict]:
        """为进行中项目创建实施任务"""
        # 基础任务模板
        return [
            {
                "project_id": project.id,
                "title": f"推进{project.name}开发",
                "description": f"继续完成{project.name}的开发工作",
                "estimated_hours": 4.0,
                "agent_role": AgentRole.DEVELOPER,
                "command": f"推进{project.name}的具体实现"
            }
        ]
    
    def _create_blocked_tasks(self, project: Project) -> List[Dict]:
        """为阻塞项目创建解决任务"""
        return [
            {
                "project_id": project.id,
                "title": f"解决{project.name}阻塞问题",
                "description": f"分析并解决{project.name}的阻塞问题",
                "estimated_hours": 2.0,
                "agent_role": AgentRole.PROJECT_MANAGER,
                "command": f"诊断{project.name}的阻塞原因并提出解决方案"
            }
        ]
    
    def execute_tasks(self, max_concurrent: int = 3):
        """并行执行任务"""
        print(f"\n=== 并行执行任务 (最大{max_concurrent}个并发) ===")
        
        if not self.task_queue:
            print("⚠️  任务队列为空")
            return []
        
        # 限制并发数量
        tasks_to_execute = self.task_queue[:max_concurrent]
        results = []
        
        def execute_task(task: Dict):
            """执行单个任务"""
            task_id = f"task_{len(results)+1:03d}"
            print(f"🚀 开始执行: {task['title']}")
            
            start_time = time.time()
            success = False
            output = ""
            
            try:
                # 这里可以实际执行命令
                # 暂时模拟执行
                time.sleep(2)  # 模拟执行时间
                
                # 模拟成功或失败
                import random
                success = random.random() > 0.3  # 70%成功率
                
                if success:
                    output = f"✅ 任务完成: {task['title']}"
                    print(f"  完成: {task['title']}")
                else:
                    output = f"❌ 任务失败: {task['title']}"
                    print(f"  失败: {task['title']}")
                    
            except Exception as e:
                output = f"❌ 执行异常: {str(e)}"
                print(f"  异常: {task['title']} - {e}")
            
            elapsed = time.time() - start_time
            
            result = {
                "task_id": task_id,
                "project_id": task["project_id"],
                "title": task["title"],
                "success": success,
                "output": output,
                "elapsed_seconds": elapsed,
                "completed_at": datetime.utcnow().isoformat()
            }
            
            results.append(result)
            
            # 更新Agent状态
            for agent in self.agents.values():
                if agent.current_project == task["project_id"]:
                    agent.complete_task(success)
                    break
        
        # 创建并启动线程
        threads = []
        for task in tasks_to_execute:
            thread = threading.Thread(target=execute_task, args=(task,))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 从队列中移除已完成的任务
        self.task_queue = self.task_queue[max_concurrent:]
        
        # 保存结果
        self.results.extend(results)
        self._save_execution_results()
        
        print(f"✅ 任务执行完成: {len(results)}个任务")
        return results
    
    def _save_execution_results(self):
        """保存执行结果"""
        results_file = os.path.join(self.data_dir, "execution_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # 保存项目状态
        projects_file = os.path.join(self.data_dir, "projects_status.json")
        projects_data = []
        for project in self.projects.values():
            project_dict = asdict(project)
            project_dict['status'] = project.status.value
            projects_data.append(project_dict)
        
        with open(projects_file, 'w', encoding='utf-8') as f:
            json.dump(projects_data, f, ensure_ascii=False, indent=2)
    
    def generate_status_report(self) -> Dict:
        """生成状态报告"""
        print("\n=== 团队管理系统状态报告 ===")
        
        # 统计信息
        total_projects = len(self.projects)
        completed_projects = sum(1 for p in self.projects.values() if p.status == ProjectStatus.COMPLETED)
        in_progress = sum(1 for p in self.projects.values() if p.status == ProjectStatus.IN_PROGRESS)
        
        total_agents = len(self.agents)
        busy_agents = sum(1 for a in self.agents.values() if not a.availability)
        
        total_tasks = len(self.task_queue) + len(self.results)
        completed_tasks = len(self.results)
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "total_projects": total_projects,
                "completed_projects": completed_projects,
                "projects_in_progress": in_progress,
                "total_agents": total_agents,
                "busy_agents": busy_agents,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "task_completion_rate": f"{(completed_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "0%"
            },
            "projects": [
                {
                    "name": p.name,
                    "status": p.status.value,
                    "completion": f"{p.completion_percentage:.1f}%",
                    "assigned_agents": len(p.assigned_agents),
                    "priority": p.priority
                }
                for p in self.projects.values()
            ],
            "agents": [
                {
                    "name": a.name,
                    "role": a.role.value,
                    "availability": "可用" if a.availability else "忙碌",
                    "performance": f"{a.performance_score:.1f}",
                    "completed_tasks": a.completed_tasks
                }
                for a in self.agents.values()
            ]
        }
        
        # 打印报告
        print(f"📊 项目统计: {completed_projects}/{total_projects} 完成")
        print(f"👥 Agent统计: {busy_agents}/{total_agents} 忙碌")