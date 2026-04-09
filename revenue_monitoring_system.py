#!/usr/bin/env python3
"""
收入监控和自动化系统
监控Stripe付款，预测收入，自动化报告
"""

import json
import time
from datetime import datetime, timedelta
import random
import os

class RevenueMonitoringSystem:
    def __init__(self):
        self.projects = {
            "supportbot_ai": {
                "name": "SupportBot AI",
                "stripe_links": {
                    "ai_code_assistant": "https://buy.stripe.com/cNi28r7Bw9Vg95j8EkgQE0f",
                    "ultra_studio": "https://buy.stripe.com/dRm00jaNI2sO4P3dYEgQE0h",
                    "ultra_master": "https://buy.stripe.com/dRmeVd7Bw4AW1CR1bSgQE0i",
                    "smart_factory_lite": "https://buy.stripe.com/8x23cv7Bw5F0bdraMsgQE0g"
                },
                "pricing": {
                    "ai_code_assistant": 19,
                    "ultra_studio": 29,
                    "ultra_master": 79,
                    "smart_factory_lite": 199
                },
                "customers": [],
                "revenue": 0
            },
            "autocontentfactory": {
                "name": "AutoContentFactory",
                "pricing": {"basic": 29, "pro": 99, "enterprise": 299},
                "customers": [],
                "revenue": 0
            }
        }
        
        self.daily_goal = 100  # 美元
        self.weekly_goal = 1000
        self.monthly_goal = 10000
        
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        if os.path.exists("revenue_data.json"):
            with open("revenue_data.json", "r") as f:
                data = json.load(f)
                self.projects = data.get("projects", self.projects)
                self.daily_goal = data.get("daily_goal", 100)
                self.weekly_goal = data.get("weekly_goal", 1000)
                self.monthly_goal = data.get("monthly_goal", 10000)
    
    def save_data(self):
        """保存数据"""
        data = {
            "projects": self.projects,
            "daily_goal": self.daily_goal,
            "weekly_goal": self.weekly_goal,
            "monthly_goal": self.monthly_goal,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("revenue_data.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def simulate_payment(self, project_name, plan="starter"):
        """模拟付款（实际应连接Stripe API）"""
        project = self.projects[project_name]
        
        if plan not in project["pricing"]:
            plan = list(project["pricing"].keys())[0]
        
        amount = project["pricing"][plan]
        
        customer = {
            "id": f"{project_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "project": project_name,
            "plan": plan,
            "amount": amount,
            "currency": "USD",
            "timestamp": datetime.now().isoformat(),
            "status": "paid",
            "email": f"customer{random.randint(1000, 9999)}@example.com"
        }
        
        # 添加到客户列表
        project["customers"].append(customer)
        project["revenue"] += amount
        
        print(f"💰 新付款: {project['name']} - {plan}计划 - ${amount}")
        
        self.save_data()
        return customer
    
    def check_stripe_webhook(self):
        """检查Stripe webhook（模拟）"""
        # 实际应连接Stripe webhook
        # 这里模拟随机付款
        
        projects = list(self.projects.keys())
        project = random.choice(projects)
        
        plans = list(self.projects[project]["pricing"].keys())
        plan = random.choice(plans)
        
        # 30%概率有新付款
        if random.random() < 0.3:
            return self.simulate_payment(project, plan)
        
        return None
    
    def get_revenue_summary(self):
        """获取收入摘要"""
        total_revenue = 0
        total_customers = 0
        
        for project_name, project in self.projects.items():
            total_revenue += project["revenue"]
            total_customers += len(project["customers"])
        
        today = datetime.now().date()
        daily_revenue = 0
        
        for project in self.projects.values():
            for customer in project["customers"]:
                customer_date = datetime.fromisoformat(customer["timestamp"]).date()
                if customer_date == today:
                    daily_revenue += customer["amount"]
        
        return {
            "total_revenue": total_revenue,
            "daily_revenue": daily_revenue,
            "total_customers": total_customers,
            "daily_goal": self.daily_goal,
            "weekly_goal": self.weekly_goal,
            "monthly_goal": self.monthly_goal,
            "daily_progress": (daily_revenue / self.daily_goal * 100) if self.daily_goal > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_forecast(self, days=30):
        """生成收入预测"""
        # 基于当前增长率预测
        summary = self.get_revenue_summary()
        
        if summary["total_customers"] == 0:
            # 如果没有客户，使用保守预测
            daily_growth = 0.5  # 每天0.5个客户
        else:
            # 基于历史数据计算增长率
            daily_growth = summary["total_customers"] / max(1, len(self.projects))
        
        forecast = []
        current_date = datetime.now()
        
        total_predicted = summary["total_revenue"]
        avg_revenue_per_customer = summary["total_revenue"] / max(1, summary["total_customers"])
        
        for day in range(days):
            date = current_date + timedelta(days=day)
            
            # 预测新客户
            new_customers = daily_growth * (1 + day * 0.05)  # 每天增长5%
            daily_revenue = new_customers * avg_revenue_per_customer
            
            total_predicted += daily_revenue
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "predicted_new_customers": round(new_customers, 1),
                "predicted_daily_revenue": round(daily_revenue, 2),
                "predicted_total_revenue": round(total_predicted, 2)
            })
        
        return forecast
    
    def send_alert(self, message, level="info"):
        """发送警报"""
        levels = {
            "info": "ℹ️",
            "warning": "⚠️",
            "success": "✅",
            "error": "❌"
        }
        
        emoji = levels.get(level, "ℹ️")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"{emoji} [{timestamp}] {message}")
        
        # 记录到日志文件
        with open("revenue_alerts.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] [{level.upper()}] {message}\n")
    
    def run_monitoring_cycle(self, duration_minutes=5):
        """运行监控周期"""
        print("📊 收入监控系统启动")
        print("=" * 50)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        cycles = 0
        payments_detected = 0
        
        while time.time() < end_time:
            cycles += 1
            
            print(f"\n🔍 监控周期 #{cycles}")
            print("-" * 30)
            
            # 检查付款
            payment = self.check_stripe_webhook()
            if payment:
                payments_detected += 1
                self.send_alert(f"检测到新付款: {payment['project']} - ${payment['amount']}", "success")
            
            # 生成报告
            summary = self.get_revenue_summary()
            
            print(f"今日收入: ${summary['daily_revenue']:.2f} / ${summary['daily_goal']:.2f}")
            print(f"进度: {summary['daily_progress']:.1f}%")
            print(f"总客户: {summary['total_customers']}")
            print(f"总收入: ${summary['total_revenue']:.2f}")
            
            # 检查目标
            if summary["daily_revenue"] >= summary["daily_goal"]:
                self.send_alert(f"🎉 达成今日收入目标! ${summary['daily_revenue']:.2f}", "success")
            
            # 保存状态
            self.save_data()
            
            # 等待下一周期（实际应使用cron job）
            if time.time() + 30 < end_time:  # 30秒间隔
                time.sleep(30)
            else:
                break
        
        # 最终报告
        print("\n" + "=" * 50)
        print("📈 监控周期完成")
        print(f"   周期数: {cycles}")
        print(f"   检测到付款: {payments_detected}")
        
        summary = self.get_revenue_summary()
        print(f"   今日收入: ${summary['daily_revenue']:.2f}")
        print(f"   总收入: ${summary['total_revenue']:.2f}")
        
        # 生成预测
        if payments_detected > 0:
            forecast = self.generate_forecast(7)
            print("\n🔮 7天收入预测:")
            for day in forecast[:3]:  # 显示前3天
                print(f"   {day['date']}: ${day['predicted_daily_revenue']:.2f} (预计)")
        
        return summary

def main():
    """主函数"""
    print("💰 收入监控和自动化系统")
    print("=" * 50)
    
    monitor = RevenueMonitoringSystem()
    
    # 显示当前状态
    summary = monitor.get_revenue_summary()
    
    print("📊 当前状态:")
    print(f"   总收入: ${summary['total_revenue']:.2f}")
    print(f"   今日收入: ${summary['daily_revenue']:.2f}")
    print(f"   总客户: {summary['total_customers']}")
    print(f"   今日目标进度: {summary['daily_progress']:.1f}%")
    
    # 运行监控（5分钟）
    print("\n🚀 启动监控系统 (5分钟)...")
    final_summary = monitor.run_monitoring_cycle(5)
    
    # 保存最终报告
    report = {
        "final_summary": final_summary,
        "projects": monitor.projects,
        "forecast_30days": monitor.generate_forecast(30),
        "generated_at": datetime.now().isoformat()
    }
    
    with open("revenue_monitoring_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ 监控报告已保存: revenue_monitoring_report.json")
    
    # 下一步建议
    print("\n🎯 下一步建议:")
    
    if final_summary["daily_revenue"] < final_summary["daily_goal"]:
        print("   1. 加强客户获取，联系更多潜在客户")
        print("   2. 提供限时优惠促进销售")
        print("   3. 优化销售话术和演示")
    else:
        print("   1. 扩大客户获取规模")
        print("   2. 考虑提高定价")
        print("   3. 开发新功能增加价值")
    
    print("\n💰 立即行动:")
    print("   1. 访问Stripe仪表板: https://dashboard.stripe.com")
    print("   2. 检查实际付款情况")
    print("   3. 联系标记为'感兴趣'的客户")
    print("   4. 发送跟进消息")

if __name__ == "__main__":
    main()