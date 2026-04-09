#!/usr/bin/env python3
"""
立即启动所有9个收入项目
目标：实现 $93,790.35/月 收入
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
import threading

# 项目配置
PROJECTS = [
    {
        "name": "AutoContentFactory",
        "port": 5000,
        "path": "/home/node/.openclaw/workspace/highspeed-projects/auto-content-factory",
        "command": "python src/main.py",
        "revenue_target": 10444.53,
        "status": "stopped"
    },
    {
        "name": "AI Token Platform",
        "port": 5001,
        "path": "/home/node/.openclaw/workspace/highspeed-projects/ai-token-platform",
        "command": "python backend/main.py",
        "revenue_target": 19976.79,
        "status": "stopped"
    },
    {
        "name": "AI Customer Service",
        "port": 5002,
        "path": "/home/node/.openclaw/workspace/highspeed-projects/ai-customer-service",
        "command": "python main.py",
        "revenue_target": 4833.27,
        "status": "stopped"
    },
    {
        "name": "DataAnalyst AI",
        "port": 5003,
        "path": "/home/node/.openclaw/workspace/auto-projects/DataAnalystAI",
        "command": "python main.py",
        "revenue_target": 7258.18,
        "status": "stopped"
    },
    {
        "name": "TrendMaster AI",
        "port": 5004,
        "path": "/home/node/.openclaw/workspace/auto-projects/TrendMasterAI",
        "command": "python main.py",
        "revenue_target": 6866.26,
        "status": "stopped"
    },
    {
        "name": "CodeGenius AI",
        "port": 5005,
        "path": "/home/node/.openclaw/workspace",
        "command": "python codegenius_ai_enhanced.py",
        "revenue_target": 10898.41,
        "status": "stopped"
    },
    {
        "name": "AI Digital Products",
        "port": 5007,
        "path": "/home/node/.openclaw/workspace/highspeed-projects/ai-digital-products",
        "command": "python simple_server.py",
        "revenue_target": 7170.87,
        "status": "stopped"
    },
    {
        "name": "AI Trading Signal",
        "port": 5007,
        "path": "/home/node/.openclaw/workspace/highspeed-projects/ai-trading-signal",
        "command": "python main.py",
        "revenue_target": 15954.76,
        "status": "stopped"
    },
    {
        "name": "AI Data Consulting",
        "port": 5008,
        "path": "/home/node/.openclaw/workspace/highspeed-projects/ai-data-consulting",
        "command": "python enhanced_server.py",
        "revenue_target": 10387.29,
        "status": "stopped"
    }
]

def check_port(port):
    """检查端口是否被占用"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def start_project(project):
    """启动单个项目"""
    print(f"🚀 启动项目: {project['name']} (端口: {project['port']})")
    
    # 检查项目目录是否存在
    if not os.path.exists(project['path']):
        print(f"  ⚠️  项目目录不存在: {project['path']}")
        project['status'] = 'missing'
        return False
    
    # 检查端口是否已被占用
    if check_port(project['port']):
        print(f"  ✅ 端口 {project['port']} 已被占用，服务可能已在运行")
        project['status'] = 'running'
        return True
    
    try:
        # 切换到项目目录
        os.chdir(project['path'])
        
        # 启动项目（后台运行）
        cmd = f"{project['command']} --port {project['port']} > /tmp/{project['name'].lower().replace(' ', '_')}.log 2>&1 &"
        subprocess.run(cmd, shell=True, check=True)
        
        # 等待服务启动
        time.sleep(2)
        
        # 检查是否启动成功
        if check_port(project['port']):
            print(f"  ✅ 启动成功！服务运行在 http://localhost:{project['port']}")
            project['status'] = 'running'
            
            # 记录启动日志
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "project": project['name'],
                "port": project['port'],
                "status": "started",
                "revenue_target": project['revenue_target']
            }
            
            with open("/tmp/project_startup_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            return True
        else:
            print(f"  ❌ 启动失败，端口 {project['port']} 未响应")
            project['status'] = 'failed'
            return False
            
    except Exception as e:
        print(f"  ❌ 启动错误: {str(e)}")
        project['status'] = 'error'
        return False

def start_all_projects():
    """启动所有项目"""
    print("=" * 60)
    print("🚀 启动所有9个收入项目 - 实现 $93,790.35/月 收入")
    print("=" * 60)
    
    total_revenue = sum(p['revenue_target'] for p in PROJECTS)
    print(f"💰 总收入目标: ${total_revenue:,.2f}/月")
    print()
    
    # 清理旧的启动日志
    if os.path.exists("/tmp/project_startup_log.json"):
        os.remove("/tmp/project_startup_log.json")
    
    # 启动所有项目
    success_count = 0
    threads = []
    
    for project in PROJECTS:
        # 使用线程并行启动
        thread = threading.Thread(target=start_project, args=(project,))
        threads.append(thread)
        thread.start()
        time.sleep(0.5)  # 稍微错开启动时间
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 统计结果
    success_count = sum(1 for p in PROJECTS if p['status'] == 'running')
    
    print("\n" + "=" * 60)
    print("📊 启动结果汇总")
    print("=" * 60)
    
    for project in PROJECTS:
        status_icon = "✅" if project['status'] == 'running' else "❌"
        print(f"{status_icon} {project['name']}: {project['status']} (端口: {project['port']}, 目标: ${project['revenue_target']:,.2f}/月)")
    
    print("\n" + "=" * 60)
    print(f"🎯 启动完成: {success_count}/{len(PROJECTS)} 个项目成功启动")
    
    if success_count == len(PROJECTS):
        print("✅ 所有项目已成功启动！")
        print(f"💰 预计月收入: ${total_revenue:,.2f}")
        print("🌐 服务地址:")
        for project in PROJECTS:
            print(f"  - {project['name']}: http://localhost:{project['port']}")
    else:
        print(f"⚠️  {len(PROJECTS) - success_count} 个项目启动失败")
        print("请检查日志文件: /tmp/[project_name].log")
    
    # 保存启动状态
    status_report = {
        "timestamp": datetime.now().isoformat(),
        "total_projects": len(PROJECTS),
        "successful": success_count,
        "failed": len(PROJECTS) - success_count,
        "total_revenue_target": total_revenue,
        "projects": PROJECTS
    }
    
    with open("/home/node/.openclaw/workspace/project_startup_status.json", "w") as f:
        json.dump(status_report, f, indent=2)
    
    print(f"\n📄 状态报告已保存: /home/node/.openclaw/workspace/project_startup_status.json")
    
    return success_count == len(PROJECTS)

def check_services():
    """检查所有服务状态"""
    print("\n🔍 检查服务状态...")
    
    all_running = True
    for project in PROJECTS:
        if check_port(project['port']):
            print(f"  ✅ {project['name']}: 运行中 (端口: {project['port']})")
        else:
            print(f"  ❌ {project['name']}: 未运行 (端口: {project['port']})")
            all_running = False
    
    return all_running

def main():
    """主函数"""
    print("💰 收入实现计划 - 启动所有项目")
    print(f"目标: ${sum(p['revenue_target'] for p in PROJECTS):,.2f}/月")
    print()
    
    # 检查当前服务状态
    print("📋 当前服务状态检查...")
    running_count = sum(1 for p in PROJECTS if check_port(p['port']))
    print(f"当前运行中: {running_count}/{len(PROJECTS)} 个项目")
    
    if running_count == len(PROJECTS):
        print("✅ 所有项目已在运行中！")
        return True
    
    # 启动所有项目
    print("\n🚀 开始启动所有项目...")
    success = start_all_projects()
    
    if success:
        print("\n🎉 所有项目启动成功！")
        print("下一步: 启动收入监控和客户获取系统")
        
        # 启动收入监控
        print("\n📊 启动收入监控系统...")
        try:
            revenue_monitor_path = "/home/node/.openclaw/workspace/revenue_monitoring_system.py"
            if os.path.exists(revenue_monitor_path):
                subprocess.run(f"python {revenue_monitor_path} > /tmp/revenue_monitor.log 2>&1 &", shell=True)
                print("✅ 收入监控系统已启动")
            else:
                print("⚠️  收入监控系统文件不存在")
        except Exception as e:
            print(f"❌ 启动收入监控系统失败: {e}")
        
        # 生成启动报告
        report = {
            "status": "success",
            "message": "所有项目已成功启动",
            "timestamp": datetime.now().isoformat(),
            "next_steps": [
                "1. 验证所有服务可访问",
                "2. 启动客户获取引擎",
                "3. 开始收入跟踪",
                "4. 发送每日报告"
            ]
        }
        
        with open("/home/node/.openclaw/workspace/startup_complete_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 启动完成报告: /home/node/.openclaw/workspace/startup_complete_report.json")
        
    else:
        print("\n⚠️  部分项目启动失败")
        print("请检查日志文件并手动启动失败的项目")
        
        # 生成错误报告
        error_report = {
            "status": "partial_failure",
            "timestamp": datetime.now().isoformat(),
            "failed_projects": [p['name'] for p in PROJECTS if p['status'] != 'running'],
            "next_steps": [
                "1. 检查 /tmp/[project_name].log 日志",
                "2. 手动启动失败项目",
                "3. 验证端口占用情况"
            ]
        }
        
        with open("/home/node/.openclaw/workspace/startup_error_report.json", "w") as f:
            json.dump(error_report, f, indent=2)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)