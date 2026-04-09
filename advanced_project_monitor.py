#!/usr/bin/env python3
"""
高级项目监控系统
实时监控所有项目状态和性能
"""

import json
import time
import socket
import subprocess
import psutil
from datetime import datetime
import threading
import http.server
import socketserver

class ProjectMonitor:
    def __init__(self):
        self.projects = []
        self.load_projects()
        self.status_file = 'project_monitor_status.json'
        self.report_file = 'project_monitor_report.md'
        
    def load_projects(self):
        """加载项目配置"""
        try:
            with open('project_monitor_config.json', 'r') as f:
                config = json.load(f)
                self.projects = config.get('projects', [])
        except:
            # 默认配置
            self.projects = [
                {'name': 'AutoContentFactory', 'port': 5000, 'type': 'content'},
                {'name': 'AI Token Platform', 'port': 5001, 'type': 'finance'},
                {'name': 'AI Customer Service', 'port': 5002, 'type': 'service'},
                {'name': 'DataAnalyst AI', 'port': 5003, 'type': 'analytics'},
                {'name': 'TrendMaster AI', 'port': 5004, 'type': 'prediction'},
                {'name': 'CodeGenius AI', 'port': 5005, 'type': 'development'},
                {'name': 'AI Digital Products', 'port': 5006, 'type': 'products'},
                {'name': 'AI Trading Signal', 'port': 5007, 'type': 'trading'},
                {'name': 'AI Data Consulting', 'port': 5008, 'type': 'consulting'}
            ]
    
    def check_port(self, port):
        """检查端口是否监听"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_process(self, port):
        """检查进程状态"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any(str(port) in str(arg) for arg in cmdline):
                    return {
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': proc.cpu_percent(),
                        'memory': proc.memory_info().rss / 1024 / 1024  # MB
                    }
            except:
                continue
        return None
    
    def check_http(self, port):
        """检查HTTP服务"""
        try:
            import urllib.request
            response = urllib.request.urlopen(f'http://localhost:{port}', timeout=2)
            return response.getcode() == 200
        except:
            return False
    
    def monitor_all(self):
        """监控所有项目"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_projects': len(self.projects),
            'projects': []
        }
        
        for project in self.projects:
            name = project['name']
            port = project['port']
            
            # 检查各项指标
            port_status = self.check_port(port)
            process_info = self.check_process(port)
            http_status = self.check_http(port) if port_status else False
            
            # 计算状态
            if port_status and http_status:
                status = 'running'
            elif port_status:
                status = 'port_only'
            else:
                status = 'stopped'
            
            # 收集数据
            project_data = {
                'name': name,
                'port': port,
                'status': status,
                'port_status': port_status,
                'http_status': http_status,
                'process': process_info,
                'last_check': datetime.now().isoformat()
            }
            
            results['projects'].append(project_data)
            
            # 打印状态
            status_icon = '✅' if status == 'running' else '⚠️' if status == 'port_only' else '❌'
            print(f'{status_icon} {name}: {status} (端口 {port})')
        
        return results
    
    def save_status(self, results):
        """保存状态到文件"""
        with open(self.status_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    def generate_report(self, results):
        """生成监控报告"""
        running = sum(1 for p in results['projects'] if p['status'] == 'running')
        port_only = sum(1 for p in results['projects'] if p['status'] == 'port_only')
        stopped = sum(1 for p in results['projects'] if p['status'] == 'stopped')
        
        report = f'''# 项目监控报告
**生成时间**: {results['timestamp']}
**总项目数**: {results['total_projects']}

## 📊 状态概览
- ✅ 运行中: {running} 个项目
- ⚠️ 仅端口监听: {port_only} 个项目  
- ❌ 停止: {stopped} 个项目

## 🔍 详细状态

'''
        
        for project in results['projects']:
            status_icon = '✅' if project['status'] == 'running' else '⚠️' if project['status'] == 'port_only' else '❌'
            report += f'### {status_icon} {project["name"]} (端口 {project["port"]})\n'
            report += f'- **状态**: {project["status"]}\n'
            report += f'- **端口监听**: {"✅ 是" if project["port_status"] else "❌ 否"}\n'
            report += f'- **HTTP服务**: {"✅ 正常" if project["http_status"] else "❌ 异常"}\n'
            
            if project['process']:
                report += f'- **进程ID**: {project["process"]["pid"]}\n'
                report += f'- **CPU使用**: {project["process"]["cpu"]:.1f}%\n'
                report += f'- **内存使用**: {project["process"]["memory"]:.1f} MB\n'
            
            report += f'- **最后检查**: {project["last_check"]}\n\n'
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def start_monitoring(self, interval=60):
        """开始持续监控"""
        print(f'🚀 开始项目监控 (间隔: {interval}秒)')
        print('=' * 60)
        
        while True:
            print(f'\n📊 监控检查: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            print('-' * 60)
            
            results = self.monitor_all()
            self.save_status(results)
            
            # 每5次检查生成一次报告
            if int(time.time()) % (interval * 5) < interval:
                report = self.generate_report(results)
                print(f'📝 报告已生成: {self.report_file}')
            
            time.sleep(interval)

def main():
    """主函数"""
    monitor = ProjectMonitor()
    
    # 单次检查
    print('🔍 执行单次项目检查...')
    results = monitor.monitor_all()
    monitor.save_status(results)
    report = monitor.generate_report(results)
    
    print(f'\n📊 检查完成:')
    print(f'  总项目数: {results["total_projects"]}')
    print(f'  运行中: {sum(1 for p in results["projects"] if p["status"] == "running")}')
    print(f'  状态文件: {monitor.status_file}')
    print(f'  报告文件: {monitor.report_file}')
    
    # 询问是否开始持续监控
    response = input('\n🚀 是否开始持续监控? (y/n): ')
    if response.lower() == 'y':
        try:
            interval = int(input('监控间隔(秒, 默认60): ') or 60)
            monitor.start_monitoring(interval)
        except KeyboardInterrupt:
            print('\n🛑 监控已停止')
    else:
        print('👋 单次检查完成')

if __name__ == '__main__':
    main()