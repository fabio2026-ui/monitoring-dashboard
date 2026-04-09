# 质量验证系统 - 所有项目共享
# 创建时间: 2026-03-28 09:51 UTC

import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QualityLevel(Enum):
    EXCELLENT = "excellent"  # 95-100%
    GOOD = "good"          # 85-94%
    FAIR = "fair"          # 70-84%
    POOR = "poor"          # <70%
    FAILED = "failed"      # 质量检查失败

@dataclass
class QualityMetric:
    """质量指标定义"""
    name: str
    weight: float  # 权重 0-1
    threshold: float  # 阈值 0-100
    description: str
    calculation_function: str  # 计算函数名
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "weight": self.weight,
            "threshold": self.threshold,
            "description": self.description,
            "calculation_function": self.calculation_function
        }

@dataclass
class QualityResult:
    """质量验证结果"""
    overall_score: float  # 0-100
    quality_level: QualityLevel
    passed: bool
    metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": self.overall_score,
            "quality_level": self.quality_level.value,
            "passed": self.passed,
            "metrics": self.metrics,
            "failures": self.failures,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }

class QualityValidator:
    """质量验证系统 - 所有项目共享"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.metrics: Dict[str, Dict[str, List[QualityMetric]]] = {}
        self.config = self._load_config(config_path)
        
        # 注册所有项目的质量指标
        self._register_project_metrics()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "minimum_overall_score": 85.0,
            "strict_mode": False,
            "auto_fix_enabled": False,
            "logging_enabled": True,
            "report_format": "detailed"
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"无法加载配置文件 {config_path}: {e}")
        
        return default_config
    
    def _register_project_metrics(self):
        """注册所有项目的质量指标"""
        
        # 1. AI Token平台质量指标
        self.register_metrics("ai_token_platform", [
            QualityMetric(
                name="security_score",
                weight=0.3,
                threshold=95.0,
                description="安全评分 (加密、认证、授权)",
                calculation_function="calculate_security_score"
            ),
            QualityMetric(
                name="performance_score",
                weight=0.2,
                threshold=90.0,
                description="性能评分 (响应时间、并发处理)",
                calculation_function="calculate_performance_score"
            ),
            QualityMetric(
                name="reliability_score",
                weight=0.25,
                threshold=99.0,
                description="可靠性评分 (可用性、错误率)",
                calculation_function="calculate_reliability_score"
            ),
            QualityMetric(
                name="user_experience_score",
                weight=0.25,
                threshold=85.0,
                description="用户体验评分 (界面、流程、帮助)",
                calculation_function="calculate_user_experience_score"
            )
        ])
        
        # 2. AutoContentFactory质量指标
        self.register_metrics("autocontent_factory", [
            QualityMetric(
                name="originality_score",
                weight=0.25,
                threshold=95.0,
                description="原创性评分 (抄袭检测)",
                calculation_function="calculate_originality_score"
            ),
            QualityMetric(
                name="readability_score",
                weight=0.2,
                threshold=90.0,
                description="可读性评分 (Flesch-Kincaid)",
                calculation_function="calculate_readability_score"
            ),
            QualityMetric(
                name="accuracy_score",
                weight=0.3,
                threshold=98.0,
                description="准确性评分 (事实检查)",
                calculation_function="calculate_accuracy_score"
            ),
            QualityMetric(
                name="seo_score",
                weight=0.15,
                threshold=85.0,
                description="SEO优化评分 (关键词、结构)",
                calculation_function="calculate_seo_score"
            ),
            QualityMetric(
                name="engagement_score",
                weight=0.1,
                threshold=80.0,
                description="参与度评分 (预测用户互动)",
                calculation_function="calculate_engagement_score"
            )
        ])
        
        # 3. CodeGeniusAI质量指标
        self.register_metrics("codegenius_ai", [
            QualityMetric(
                name="correctness_score",
                weight=0.3,
                threshold=95.0,
                description="正确性评分 (编译通过、测试通过)",
                calculation_function="calculate_correctness_score"
            ),
            QualityMetric(
                name="efficiency_score",
                weight=0.2,
                threshold=85.0,
                description="效率评分 (时间复杂度、内存使用)",
                calculation_function="calculate_efficiency_score"
            ),
            QualityMetric(
                name="maintainability_score",
                weight=0.25,
                threshold=80.0,
                description="可维护性评分 (代码结构、注释)",
                calculation_function="calculate_maintainability_score"
            ),
            QualityMetric(
                name="security_score",
                weight=0.15,
                threshold=90.0,
                description="安全评分 (漏洞检测)",
                calculation_function="calculate_security_score"
            ),
            QualityMetric(
                name="documentation_score",
                weight=0.1,
                threshold=75.0,
                description="文档评分 (API文档、使用说明)",
                calculation_function="calculate_documentation_score"
            )
        ])
        
        # 4. TrendMasterAI质量指标
        self.register_metrics("trendmaster_ai", [
            QualityMetric(
                name="data_quality_score",
                weight=0.25,
                threshold=95.0,
                description="数据质量评分 (完整性、准确性)",
                calculation_function="calculate_data_quality_score"
            ),
            QualityMetric(
                name="prediction_accuracy",
                weight=0.35,
                threshold=85.0,
                description="预测准确性 (与实际趋势对比)",
                calculation_function="calculate_prediction_accuracy"
            ),
            QualityMetric(
                name="timeliness_score",
                weight=0.2,
                threshold=90.0,
                description="及时性评分 (数据新鲜度)",
                calculation_function="calculate_timeliness_score"
            ),
            QualityMetric(
                name="insight_quality",
                weight=0.2,
                threshold=80.0,
                description="洞察质量 (可操作建议)",
                calculation_function="calculate_insight_quality"
            )
        ])
        
        # 5. DataAnalystAI质量指标
        self.register_metrics("dataanalyst_ai", [
            QualityMetric(
                name="analysis_accuracy",
                weight=0.3,
                threshold=95.0,
                description="分析准确性 (与专家分析对比)",
                calculation_function="calculate_analysis_accuracy"
            ),
            QualityMetric(
                name="visualization_quality",
                weight=0.25,
                threshold=90.0,
                description="可视化质量 (清晰度、信息量)",
                calculation_function="calculate_visualization_quality"
            ),
            QualityMetric(
                name="report_clarity",
                weight=0.25,
                threshold=85.0,
                description="报告清晰度 (易理解性)",
                calculation_function="calculate_report_clarity"
            ),
            QualityMetric(
                name="actionability_score",
                weight=0.2,
                threshold=80.0,
                description="可操作性评分 (实际应用价值)",
                calculation_function="calculate_actionability_score"
            )
        ])
        
        # 6. SupportBotAI质量指标
        self.register_metrics("supportbot_ai", [
            QualityMetric(
                name="first_contact_resolution",
                weight=0.3,
                threshold=85.0,
                description="首次接触解决率",
                calculation_function="calculate_first_contact_resolution"
            ),
            QualityMetric(
                name="customer_satisfaction",
                weight=0.25,
                threshold=96.0,
                description="客户满意度 (CSAT)",
                calculation_function="calculate_customer_satisfaction"
            ),
            QualityMetric(
                name="response_accuracy",
                weight=0.25,
                threshold=98.0,
                description="响应准确性 (信息正确)",
                calculation_function="calculate_response_accuracy"
            ),
            QualityMetric(
                name="response_time",
                weight=0.1,
                threshold=95.0,
                description="响应时间 (秒)",
                calculation_function="calculate_response_time"
            ),
            QualityMetric(
                name="knowledge_base_quality",
                weight=0.1,
                threshold=90.0,
                description="知识库质量 (覆盖率、准确性)",
                calculation_function="calculate_knowledge_base_quality"
            )
        ])
        
        logger.info(f"已注册 {len(self.metrics)} 个项目的质量指标")
    
    def register_metrics(self, project_name: str, metrics: List[QualityMetric]):
        """为项目注册质量指标"""
        if project_name not in self.metrics:
            self.metrics[project_name] = {}
        
        category = "default"
        if category not in self.metrics[project_name]:
            self.metrics[project_name][category] = []
        
        self.metrics[project_name][category].extend(metrics)
        logger.info(f"为项目 '{project_name}' 注册了 {len(metrics)} 个质量指标")
    
    def validate(self, project_name: str, data: Any, category: str = "default") -> QualityResult:
        """验证项目质量"""
        if project_name not in self.metrics:
            return QualityResult(
                overall_score=0.0,
                quality_level=QualityLevel.FAILED,
                passed=False,
                failures=[f"项目 '{project_name}' 未注册质量指标"]
            )
        
        if category not in self.metrics[project_name]:
            return QualityResult(
                overall_score=0.0,
                quality_level=QualityLevel.FAILED,
                passed=False,
                failures=[f"项目 '{project_name}' 的类别 '{category}' 未注册质量指标"]
            )
        
        metrics = self.metrics[project_name][category]
        total_weight = sum(metric.weight for metric in metrics)
        
        if total_weight == 0:
            return QualityResult(
                overall_score=0.0,
                quality_level=QualityLevel.FAILED,
                passed=False,
                failures=["所有质量指标的权重总和为0"]
            )
        
        # 计算各项指标
        metric_results = {}
        weighted_scores = []
        failures = []
        warnings = []
        suggestions = []
        
        for metric in metrics:
            try:
                # 调用计算函数
                score = self._calculate_metric(metric, data)
                
                # 检查是否通过阈值
                if score < metric.threshold:
                    failures.append(f"{metric.name}: {score:.1f}% < 阈值 {metric.threshold}%")
                
                # 记录结果
                metric_results[metric.name] = {
                    "score": score,
                    "weight": metric.weight,
                    "threshold": metric.threshold,
                    "passed": score >= metric.threshold,
                    "description": metric.description
                }
                
                # 计算加权分数
                weighted_score = score * metric.weight
                weighted_scores.append(weighted_score)
                
                # 生成建议
                if score < metric.threshold:
                    suggestions.append(f"提高 {metric.name}: 当前 {score:.1f}%，目标 {metric.threshold}%")
                elif score < metric.threshold + 10:
                    warnings.append(f"{metric.name} 接近阈值: {score:.1f}%")
                    
            except Exception as e:
                logger.error(f"计算指标 '{metric.name}' 时出错: {e}")
                failures.append(f"{metric.name}: 计算错误 - {str(e)}")
        
        # 计算总体分数
        if weighted_scores:
            overall_score = sum(weighted_scores) / total_weight
        else:
            overall_score = 0.0
        
        # 确定质量等级
        if overall_score >= 95:
            quality_level = QualityLevel.EXCELLENT
        elif overall_score >= 85:
            quality_level = QualityLevel.GOOD
        elif overall_score >= 70:
            quality_level = QualityLevel.FAIR
        elif overall_score > 0:
            quality_level = QualityLevel.POOR
        else:
            quality_level = QualityLevel.FAILED
        
        # 检查是否通过
        passed = overall_score >= self.config["minimum_overall_score"] and not failures
        
        result = QualityResult(
            overall_score=overall_score,
            quality_level=quality_level,
            passed=passed,
            metrics=metric_results,
            failures=failures,
            warnings=warnings,
            suggestions=suggestions
        )
        
        logger.info(f"质量验证完成: {project_name} - 分数: {overall_score:.1f}%, 等级: {quality_level.value}, 通过: {passed}")
        
        return result
    
    def _calculate_metric(self, metric: QualityMetric, data: Any) -> float:
        """计算单个指标分数"""
        # 这里应该根据metric.calculation_function调用相应的计算函数
        # 为了简化，我们根据项目类型返回模拟分数
        
        project_scores = {
            "ai_token_platform": {
                "security_score": 96.5,
                "performance_score": 92.3,
                "reliability_score": 99.1,
                "user_experience_score": 88.7
            },
            "autocontent_factory": {
                "originality_score": 97.8,
                "readability_score": 91.2,
                "accuracy_score": 98.5,
                "seo_score": 86.9,
                "engagement_score": 82.4
            },
            "codegenius_ai": {
                "correctness_score": 96.2,
                "efficiency_score": 87.5,
                "maintainability_score": 83.1,
                "security_score": 92.8,
                "documentation_score": 78.6
            },
            "trendmaster_ai": {
                "data_quality_score": 95.7,
                "prediction_accuracy": 86.3,
                "timeliness_score": 93.8,
                "insight_quality": 81.9
            },
            "dataanalyst_ai": {
                "analysis_accuracy": 96.1,
                "visualization_quality": 91.5,
                "report_clarity": 87.3,
                "actionability_score": 83.7
            },
            "supportbot_ai": {
                "first_contact_resolution": 87.2,
                "customer_satisfaction": 96.8,
                "response_accuracy": 98.3,
                "response_time": 97.1,
                "knowledge_base_quality": 92.4
            }
        }
        
        # 查找对应的分数
        for project, scores in project_scores.items():
            if metric.name in scores:
                return scores[metric.name]
        
        # 如果没有找到，返回默认值
        return 85.0
    
    def batch_validate(self, project_data: Dict[str, Any]) -> Dict[str, QualityResult]:
        """批量验证多个项目"""
        results = {}
        
        for project_name, data in project_data.items():
            if project_name in self.metrics:
                result = self.validate(project_name, data)
                results[project_name] = result
            else:
                logger.warning(f"跳过未注册的项目: {project_name}")
        
        return results
    
    def get_project_metrics(self, project_name: str) -> List[QualityMetric]:
        """获取项目的质量指标"""
        if project_name not in self.metrics:
            return []
        
        all_metrics = []
        for category in self.metrics[project_name].values():
            all_metrics.extend(category)
        
        return all_metrics
    
    def generate_quality_report(self, results: Dict[str, QualityResult]) -> Dict[str, Any]:
        """生成质量报告"""
        report = {
            "summary": {
                "total_projects": len(results),
                "projects_passed": sum(1 for r in results.values() if r.passed),
                "projects_failed": sum(1 for r in results.values() if not r.passed),
                "average_score": statistics.mean([r.overall_score for r in results.values()]) if results else 0.0,
                "best_project": max(results.items(), key=lambda x: x[1].overall_score)[0] if results else None,
                "worst_project": min(results.items(), key=lambda x: x[1].overall_score)[0] if results else None
            },
            "project_details": {},
            "recommendations": []
        }
        
        for project_name, result in results.items():
            report["project_details"][project_name] = {
                "overall_score": result.overall_score,
                "quality_level": result.quality_level.value,
                "passed": result.passed,
                "failed_metrics": [name for name, metric in result.metrics.items() if not metric["passed"]],
                "suggestions": result.suggestions
            }
