#!/usr/bin/env python3
"""
简单服务状态检查 - 不使用requests模块
检查所有9个项目服务的运行状态
"""

import subprocess
import json
import time
from datetime import datetime

def check_service(port):
    """使用curl检查服务状态"""
    try:
        # 使用curl检查服务
        cmd = f"curl -s -o /dev/null -w '%{{http_code}}' --connect-timeout 5 http://localhost:{port}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            status_code = result.stdout.strip()
            if status_code.isdigit():
                return int(status_code)
        return 0
    except:
        return 0

def get_service_name(port):
    """根据端口获取服务名称"""
    service_names = {
        5000: "AutoContentFactory",
        5001: "AI Token Platform",
        5002: "AI Customer Service",
        5003: "DataAnalyst AI",
        5004: "TrendMaster AI",
        5005: "CodeGenius AI",
        5006: "AI Digital Products",
        5007: "AI Trading Signal",
        5008: "AI Data Consulting"
    }
    return service_names.get(port, f"Service-{port}")

def main():
    print("🔍 检查所有9个项目服务状态...")
    print("=" * 50)
    
    ports = list(range(5000, 5009))
    results = []
    total_healthy = 0
    
    for port in ports:
        service_name = get_service_name(port)
        print(f"检查 {service_name} (端口 {port})...", end=" ")
        
        start_time = time.time()
        status_code = check_service(port)
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒
        
        if status_code == 200:
            status = "✅ 健康"
            total_healthy += 1
        elif status_code > 0:
            status = f"⚠️ 异常 (HTTP {status_code})"
        else:
            status = "❌ 离线"
        
        print(f"{status} - {response_time:.1f}ms")
        
        results.append({
            "port": port,
            "service_name": service_name,
            "status_code": status_code,
            "status": "healthy" if status_code == 200 else "unhealthy",
            "response_time_ms": round(response_time, 1),
            "timestamp": datetime.now().isoformat()
        })
    
    print("=" * 50)
    print(f"📊 总结: {total_healthy}/9 个服务健康")
    
    # 生成JSON报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_services": len(ports),
        "healthy_services": total_healthy,
        "unhealthy_services": len(ports) - total_healthy,
        "health_percentage": round((total_healthy / len(ports)) * 100, 1),
        "services": results
    }
    
    # 保存报告
    with open("service_status_report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 报告已保存到: service_status_report.json")
    
    # 检查是否所有服务都健康
    if total_healthy == len(ports):
        print("🎉 所有服务正常运行！可以开始推广！")
        return True
    else:
        print(f"⚠️  {len(ports) - total_healthy} 个服务需要检查")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)