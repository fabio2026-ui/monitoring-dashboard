#!/usr/bin/env python3
"""
Token Optimizer Skill - OpenClaw AI代理Token优化工具
基于老板分享的今日头条文章主题开发
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

class TokenOptimizer:
    """Token优化器核心类"""
    
    def __init__(self):
        self.optimization_rules = self._load_optimization_rules()
        self.usage_history = []
        self.stats = {
            "total_tokens_saved": 0,
            "optimization_count": 0,
            "avg_improvement": 0
        }
    
    def _load_optimization_rules(self) -> List[Dict]:
        """加载优化规则 - 基于搜索到的9个技巧"""
        return [
            {
                "id": "rule_001",
                "name": "明确指令",
                "description": "提供清晰、具体的指令，避免模糊不清的表达",
                "pattern": r"(?:可能|大概|也许|或者|不确定)",
                "suggestion": "请提供更明确的指令，例如：'请生成Python代码来...' 而不是 '可能写个代码'",
                "token_saving": 15
            },
            {
                "id": "rule_002",
                "name": "避免重复",
                "description": "不要重复提问相同的问题",
                "pattern": r"(.+?)(?:\s+|\n+)\1",
                "suggestion": "检测到重复内容，请合并或删除重复部分",
                "token_saving": 30
            },
            {
                "id": "rule_003",
                "name": "合并问题",
                "description": "将多个信息需求合并到一个请求中",
                "pattern": r"(?:还有|另外|此外|同时)(?:.*?)\?",
                "suggestion": "检测到多个问题，建议合并为一个请求",
                "token_saving": 25
            },
            {
                "id": "rule_004",
                "name": "使用上下文",
                "description": "利用对话上下文来避免重复提供信息",
                "pattern": r"(?:之前|刚才|上面|前述)(?:.*?)没有提到",
                "suggestion": "请参考之前的对话上下文，避免重复信息",
                "token_saving": 20
            },
            {
                "id": "rule_005",
                "name": "避免无关内容",
                "description": "不要在对话中引入与任务无关的内容",
                "pattern": r"(?:顺便|随便|闲聊|无关)(?:.*?)",
                "suggestion": "检测到可能无关的内容，建议聚焦核心任务",
                "token_saving": 40
            },
            {
                "id": "rule_006",
                "name": "直接请求所需信息",
                "description": "如果知道需要什么信息，直接请求",
                "pattern": r"(?:能不能|是否可以|可不可以)(?:.*?)\?",
                "suggestion": "建议直接表达需求，例如：'请提供...' 而不是 '能不能提供...'",
                "token_saving": 10
            },
            {
                "id": "rule_007",
                "name": "合理使用搜索功能",
                "description": "需要外部信息时使用搜索功能",
                "pattern": r"(?:最新|实时|当前)(?:.*?)(?:不知道|不清楚|不了解)",
                "suggestion": "检测到需要最新信息，建议使用搜索功能获取",
                "token_saving": 35
            },
            {
                "id": "rule_008",
                "name": "监控Token使用",
                "description": "定期检查Token使用情况",
                "pattern": None,  # 特殊规则，不基于模式
                "suggestion": "建议定期检查Token使用报告",
                "token_saving": 5
            },
            {
                "id": "rule_009",
                "name": "反馈和调整",
                "description": "根据反馈调整策略",
                "pattern": None,  # 特殊规则
                "suggestion": "根据优化效果调整使用策略",
                "token_saving": 10
            }
        ]
    
    def analyze_prompt(self, prompt: str) -> Dict:
        """分析提示词，识别优化机会"""
        analysis = {
            "prompt_length": len(prompt),
            "estimated_tokens": len(prompt) // 4,  # 粗略估计
            "optimizations": [],
            "total_potential_saving": 0,
            "optimized_prompt": prompt,
            "improvement_percentage": 0
        }
        
        # 应用每个优化规则
        for rule in self.optimization_rules:
            if rule["pattern"]:
                matches = re.findall(rule["pattern"], prompt, re.IGNORECASE)
                if matches:
                    optimization = {
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "matches": len(matches),
                        "suggestion": rule["suggestion"],
                        "token_saving": rule["token_saving"] * len(matches)
                    }
                    analysis["optimizations"].append(optimization)
                    analysis["total_potential_saving"] += optimization["token_saving"]
        
        # 计算改进百分比
        if analysis["estimated_tokens"] > 0:
            analysis["improvement_percentage"] = (
                analysis["total_potential_saving"] / analysis["estimated_tokens"] * 100
            )
        
        # 生成优化后的提示词（简化版）
        analysis["optimized_prompt"] = self._generate_optimized_prompt(prompt, analysis["optimizations"])
        
        # 记录使用历史
        self._record_usage(analysis)
        
        return analysis
    
    def _generate_optimized_prompt(self, original_prompt: str, optimizations: List[Dict]) -> str:
        """生成优化后的提示词"""
        optimized = original_prompt
        
        # 应用优化建议（简化实现）
        for opt in optimizations:
            if opt["rule_id"] == "rule_001":  # 明确指令
                optimized = re.sub(r"(可能|大概|也许)", "请", optimized, flags=re.IGNORECASE)
            elif opt["rule_id"] == "rule_002":  # 避免重复
                # 简单的重复检测和移除
                lines = optimized.split('\n')
                unique_lines = []
                for line in lines:
                    if line.strip() and line not in unique_lines:
                        unique_lines.append(line)
                optimized = '\n'.join(unique_lines)
            elif opt["rule_id"] == "rule_006":  # 直接请求
                optimized = re.sub(r"能不能|是否可以|可不可以", "请", optimized, flags=re.IGNORECASE)
        
        return optimized
    
    def _record_usage(self, analysis: Dict):
        """记录使用历史"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "original_length": analysis["prompt_length"],
            "estimated_tokens": analysis["estimated_tokens"],
            "potential_saving": analysis["total_potential_saving"],
            "improvement_percentage": analysis["improvement_percentage"],
            "optimization_count": len(analysis["optimizations"])
        }
        
        self.usage_history.append(record)
        
        # 更新统计
        self.stats["total_tokens_saved"] += analysis["total_potential_saving"]
        self.stats["optimization_count"] += 1
        
        if self.stats["optimization_count"] > 0:
            self.stats["avg_improvement"] = (
                self.stats["total_tokens_saved"] / 
                (sum([h["estimated_tokens"] for h in self.usage_history]) / len(self.usage_history)) * 100
            )
    
    def generate_report(self, days: int = 7) -> Dict:
        """生成Token使用报告"""
        recent_history = [
            h for h in self.usage_history 
            if (datetime.now() - datetime.fromisoformat(h["timestamp"])).days <= days
        ]
        
        if not recent_history:
            return {"error": "No data available for the specified period"}
        
        total_original_tokens = sum([h["estimated_tokens"] for h in recent_history])
        total_potential_saving = sum([h["potential_saving"] for h in recent_history])
        
        report = {
            "period_days": days,
            "analysis_count": len(recent_history),
            "total_original_tokens": total_original_tokens,
            "total_potential_saving": total_potential_saving,
            "average_improvement_percentage": (
                total_potential_saving / total_original_tokens * 100 if total_original_tokens > 0 else 0
            ),
            "estimated_cost_saving_usd": total_potential_saving * 0.000002,  # 假设 $0.002/1K tokens
            "top_optimization_rules": self._get_top_rules(recent_history),
            "recommendations": self._generate_recommendations(recent_history)
        }
        
        return report
    
    def _get_top_rules(self, history: List[Dict]) -> List[Dict]:
        """获取最有效的优化规则"""
        # 简化实现 - 在实际应用中需要更复杂的分析
        return [
            {"rule": "明确指令", "effectiveness": "高", "saving_percentage": 25},
            {"rule": "避免重复", "effectiveness": "高", "saving_percentage": 20},
            {"rule": "合并问题", "effectiveness": "中", "saving_percentage": 15},
            {"rule": "使用搜索功能", "effectiveness": "中", "saving_percentage": 12}
        ]
    
    def _generate_recommendations(self, history: List[Dict]) -> List[str]:
        """生成优化建议"""
        recommendations = [
            "1. 为团队提供Token优化培训",
            "2. 在编写提示词时使用优化检查",
            "3. 定期审查Token使用报告",
            "4. 建立提示词最佳实践库",
            "5. 实施A/B测试验证优化效果"
        ]
        
        avg_improvement = sum([h["improvement_percentage"] for h in history]) / len(history)
        
        if avg_improvement < 10:
            recommendations.append("6. 需要加强基础优化技巧培训")
        elif avg_improvement > 30:
            recommendations.append("6. 优秀！考虑分享优化经验")
        
        return recommendations
    
    def save_report(self, report: Dict, filename: str = "token_optimization_report.json"):
        """保存报告到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已保存到: {filename}")
        return filename


def main():
    """主函数 - 命令行接口"""
    import sys
    
    optimizer = TokenOptimizer()
    
    if len(sys.argv) > 1:
        # 分析提供的提示词
        prompt = ' '.join(sys.argv[1:])
        print(f"🔍 分析提示词: {prompt[:100]}...")
        
        analysis = optimizer.analyze_prompt(prompt)
        
        print(f"\n📊 分析结果:")
        print(f"   原始长度: {analysis['prompt_length']} 字符")
        print(f"   估计Token数: {analysis['estimated_tokens']}")
        print(f"   发现优化机会: {len(analysis['optimizations'])} 个")
        print(f"   潜在节省: {analysis['total_potential_saving']} tokens")
        print(f"   改进百分比: {analysis['improvement_percentage']:.1f}%")
        
        if analysis['optimizations']:
            print(f"\n💡 优化建议:")
            for opt in analysis['optimizations']:
                print(f"   • {opt['rule_name']}: {opt['suggestion']}")
        
        # 生成报告
        report = optimizer.generate_report()
        optimizer.save_report(report)
        
    else:
        # 显示使用说明
        print("""
🤖 Token Optimizer Skill - OpenClaw AI代理Token优化工具
=======================================================

使用方法:
  python3 token_optimizer_skill.py "你的提示词内容"

示例:
  python3 token_optimizer_skill.py "可能写个Python代码来处理数据，另外还需要分析结果"

功能:
  1. 分析提示词的Token使用效率
  2. 识别9种常见的Token浪费模式
  3. 提供优化建议
  4. 生成Token使用报告
  5. 计算潜在的成本节省

基于老板分享的今日头条文章:
  【OpenClaw：停止浪费百分之九十的无效Token】
        """)


if __name__ == "__main__":
    main()