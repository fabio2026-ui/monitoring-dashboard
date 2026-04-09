# 用户管理系统 - 所有项目共享
# 创建时间: 2026-03-28 09:52 UTC

import json
import logging
import hashlib
import secrets
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    SUPPORT = "support"
    GUEST = "guest"

class SubscriptionPlan(Enum):
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

@dataclass
class User:
    """用户定义"""
    user_id: str
    email: str
    username: str
    hashed_password: str
    role: UserRole
    subscription: SubscriptionPlan
    projects: List[str] = field(default_factory=list)  # 用户参与的项目
    tokens: Dict[str, int] = field(default_factory=dict)  # 各项目的token余额
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_login: Optional[float] = None
    is_active: bool = True
    is_verified: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "role": self.role.value,
            "subscription": self.subscription.value,
            "projects": self.projects,
            "tokens": self.tokens,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "is_active": self.is_active,
            "is_verified": self.is_verified
        }

@dataclass
class Project:
    """项目定义"""
    project_id: str
    name: str
    description: str
    owner_id: str
    team_members: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "team_members": self.team_members,
            "settings": self.settings,
            "created_at": self.created_at,
            "is_active": self.is_active
        }

@dataclass
class Payment:
    """支付记录"""
    payment_id: str
    user_id: str
    amount: float
    currency: str = "USD"
    project_id: Optional[str] = None
    subscription_plan: Optional[SubscriptionPlan] = None
    tokens_purchased: Optional[int] = None
    status: str = "pending"
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "currency": self.currency,
            "project_id": self.project_id,
            "subscription_plan": self.subscription_plan.value if self.subscription_plan else None,
            "tokens_purchased": self.tokens_purchased,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

class UserManager:
    """用户管理系统 - 所有项目共享"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.users: Dict[str, User] = {}
        self.projects: Dict[str, Project] = {}
        self.payments: Dict[str, Payment] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.config = self._load_config(config_path)
        
        # 初始化默认项目
        self._initialize_default_projects()
        
        # 创建默认管理员用户
        self._create_default_admin()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "password_min_length": 8,
            "session_timeout": 86400,  # 24小时
            "max_login_attempts": 5,
            "token_price": 0.01,  # 每个token的价格（美元）
            "subscription_plans": {
                "free": {"monthly_price": 0, "tokens": 100, "features": ["basic_access"]},
                "basic": {"monthly_price": 9.99, "tokens": 1000, "features": ["basic_access", "api_access"]},
                "professional": {"monthly_price": 29.99, "tokens": 5000, "features": ["basic_access", "api_access", "priority_support"]},
                "enterprise": {"monthly_price": 99.99, "tokens": 25000, "features": ["basic_access", "api_access", "priority_support", "custom_integration"]}
            },
            "security": {
                "require_email_verification": True,
                "enable_2fa": False,
                "password_history": 5
            }
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"无法加载配置文件 {config_path}: {e}")
        
        return default_config
    
    def _initialize_default_projects(self):
        """初始化默认项目"""
        default_projects = [
            ("ai_token_platform", "AI Token平台", "多语言AI Token计费和管理平台"),
            ("autocontent_factory", "AutoContentFactory", "全自动内容生成工厂"),
            ("codegenius_ai", "CodeGenius AI", "全自动代码开发平台"),
            ("trendmaster_ai", "TrendMaster AI", "全自动趋势分析平台"),
            ("dataanalyst_ai", "DataAnalyst AI", "全自动数据分析平台"),
            ("supportbot_ai", "SupportBot AI", "全自动客户支持平台")
        ]
        
        for project_id, name, description in default_projects:
            project = Project(
                project_id=project_id,
                name=name,
                description=description,
                owner_id="system"
            )
            self.projects[project_id] = project
        
        logger.info(f"已初始化 {len(default_projects)} 个默认项目")
    
    def _create_default_admin(self):
        """创建默认管理员用户"""
        admin_email = "admin@openclaw.ai"
        admin_password = self._hash_password("Admin123!")
        
        admin_user = User(
            user_id="admin_001",
            email=admin_email,
            username="admin",
            hashed_password=admin_password,
            role=UserRole.ADMIN,
            subscription=SubscriptionPlan.ENTERPRISE,
            projects=list(self.projects.keys()),
            tokens={project_id: 10000 for project_id in self.projects.keys()},
            is_verified=True
        )
        
        self.users[admin_user.user_id] = admin_user
        logger.info("已创建默认管理员用户")
    
    def _hash_password(self, password: str) -> str:
        """哈希密码"""
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ":" + salt
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """验证密码"""
        try:
            stored_hash, salt = hashed_password.split(":")
            return hashlib.sha256((password + salt).encode()).hexdigest() == stored_hash
        except:
            return False
    
    def _generate_user_id(self) -> str:
        """生成用户ID"""
        return f"user_{int(time.time())}_{secrets.token_hex(4)}"
    
    def _generate_session_token(self) -> str:
        """生成会话令牌"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, email: str, username: str, password: str, 
                     role: UserRole = UserRole.USER) -> Tuple[bool, str, Optional[User]]:
        """注册新用户"""
        # 检查邮箱是否已存在
        for user in self.users.values():
            if user.email == email:
                return False, "邮箱已被注册", None
        
        # 检查用户名是否已存在
        for user in self.users.values():
            if user.username == username:
                return False, "用户名已被使用", None
        
        # 检查密码长度
        if len(password) < self.config["password_min_length"]:
            return False, f"密码长度至少为{self.config['password_min_length']}个字符", None
        
        # 创建用户
        user_id = self._generate_user_id()
        hashed_password = self._hash_password(password)
        
        user = User(
            user_id=user_id,
            email=email,
            username=username,
            hashed_password=hashed_password,
            role=role,
            subscription=SubscriptionPlan.FREE,
            projects=[],  # 新用户默认不加入任何项目
            tokens={},  # 新用户没有token
            metadata={"registration_source": "web"}
        )
        
        self.users[user_id] = user
        logger.info(f"用户注册成功: {username} ({email})")
        
        return True, "注册成功", user
    
    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[str], Optional[User]]:
        """用户登录"""
        # 查找用户
        user = None
        for u in self.users.values():
            if u.email == email:
                user = u
                break
        
        if not user:
            return False, "用户不存在", None, None
        
        if not user.is_active:
            return False, "用户账户已被禁用", None, None
        
        # 验证密码
        if not self._verify_password(password, user.hashed_password):
            return False, "密码错误", None, None
        
        # 更新最后登录时间
        user.last_login = time.time()
        
        # 创建会话
        session_token = self._generate_session_token()
        self.sessions[session_token] = {
            "user_id": user.user_id,
            "created_at": time.time(),
            "last_activity": time.time(),
            "ip_address": "unknown",
            "user_agent": "unknown"
        }
        
        logger.info(f"用户登录成功: {user.username} ({user.email})")
        
        return True, "登录成功", session_token, user
    
    def logout(self, session_token: str) -> bool:
        """用户登出"""
        if session_token in self.sessions:
            del self.sessions[session_token]
            logger.info("用户登出成功")
            return True
        return False
    
    def get_user_by_token(self, session_token: str) -> Optional[User]:
        """通过会话令牌获取用户"""
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # 检查会话是否过期
        if time.time() - session["last_activity"] > self.config["session_timeout"]:
            del self.sessions[session_token]
            return None
        
        # 更新最后活动时间
        session["last_activity"] = time.time()
        
        user_id = session["user_id"]
        return self.users.get(user_id)
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """更新用户资料"""
        if user_id not in self.users:
            return False, "用户不存在"
        
        user = self.users[user_id]
        
        # 允许更新的字段
        allowed_fields = ["username", "metadata"]
        
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(user, field, value)
            elif field == "email":
                # 邮箱需要验证
                return False, "邮箱修改需要验证流程"
            elif field == "password":
                # 密码需要特殊处理
                if len(value) < self.config["password_min_length"]:
                    return False, f"密码长度至少为{self.config['password_min_length']}个字符"
                user.hashed_password = self._hash_password(value)
        
        logger.info(f"用户资料更新成功: {user.username}")
        return True, "资料更新成功"
    
    def assign_user_to_project(self, user_id: str, project_id: str, 
                              role: UserRole = UserRole.USER) -> Tuple[bool, str]:
        """将用户分配到项目"""
        if user_id not in self.users:
            return False, "用户不存在"
        
        if project_id not in self.projects:
            return False, "项目不存在"
        
        user = self.users[user_id]
        project = self.projects[project_id]
        
        # 检查用户是否已在项目中
        if project_id in user.projects:
            return False, "用户已在项目中"
        
        # 添加用户到项目
        user.projects.append(project_id)
        
        # 初始化用户的项目token
        if project_id not in user.tokens:
            user.tokens[project_id] = 0
        
        # 添加用户到项目成员列表
        if user_id not in project.team_members:
            project.team_members.append(user_id)
        
        logger.info(f"用户 {user.username} 已分配到项目 {project.name}")
        return True, "用户分配成功"
    
    def purchase_tokens(self, user_id: str, project_id: str, 
                       token_amount: int, payment_method: str = "stripe") -> Tuple[bool, str, Optional[Payment]]:
        """购买token"""
        if user_id not in self.users:
            return False, "用户不存在", None
        
        if project_id not in self.projects:
            return False, "项目不存在", None
        
        user = self.users[user_id]
        
        # 检查用户是否在项目中
        if project_id not in user.projects:
            return False, "用户不在该项目中", None
        
        # 计算价格
        price = token_amount * self.config["token_price"]
        
        # 创建支付记录
        payment_id = f"pay_{int(time.time())}_{secrets.token_hex(6)}"
        payment = Payment(
            payment_id=payment_id,
            user_id=user_id,
            amount=price,
            project_id=project_id,
            tokens_purchased=token_amount,
            status="completed"  # 模拟支付成功
        )
        
        self.payments[payment_id] = payment
        
        # 添加token到用户账户
        if project_id in user.tokens:
            user.tokens[project_id] += token_amount
        else:
            user.tokens[project_id] = token_amount
        
        logger.info(f"用户 {user.username} 购买了 {token_amount} 个token (项目: {project_id}, 价格: ${price:.2f})")
        
        return True, "购买成功", payment
    
    def use_tokens(self, user_id: str, project_id: str, 
                  token_amount: int, description: str = "") -> Tuple[bool, str]:
        """使用token"""
        if user_id not in self.users:
            return False, "用户不存在"
        
        if project_id not in self.projects:
            return False, "项目不存在"
        
        user = self.users[user_id]
        
        # 检查用户是否在项目中
        if project_id not in user.projects:
            return False, "用户不在该项目中"
        
        # 检查token余额
        current_tokens = user.tokens.get(project_id, 0)
        if current_tokens < token_amount:
            return False, f"token不足。当前: {current_tokens}, 需要: {token_amount}"
        
        # 扣除token
        user.tokens[project_id] = current_tokens - token_amount
        
        # 记录使用历史
        if "token_usage" not in user.metadata:
            user.metadata["token_usage"] = []
        
        user.metadata["token_usage"].append({
            "timestamp": time.time(),
            "project_id": project_id,
            "amount": token_amount,
            "description": description,
            "remaining": user.tokens[project_id]
        })
        
        logger.info(f"用户 {user.username} 使用了 {token_amount} 个token (项目: {project_id}, 描述: {description})")
        
        return True, "token使用成功"
    
    def upgrade_subscription(self, user_id: str, new_plan: SubscriptionPlan) -> Tuple[bool, str, Optional[Payment]]:
        """升级订阅计划"""
        if user_id not in self.users:
            return False, "用户不存在", None
        
        user = self.users[user_id]
        
        # 检查是否已经是该计划
        if user.subscription == new_plan:
            return False, "用户已在该订阅计划中", None
        
        # 获取价格
        plan_config = self.config["subscription_plans"].get(new_plan.value)
        if not plan_config:
            return False, "订阅计划不存在", None
        
        price = plan_config["monthly_price"]
        
        # 创建支付记录
        payment_id = f"sub_{int(time.time())}_{secrets.token_hex(6)}"
        payment = Payment(
            payment_id=payment_id,
            user_id=user_id,
            amount=price,
            subscription_plan=new_plan,
            status="completed"  # 模拟支付成功
        )
        
        self.payments[payment_id] = payment
        
        # 更新用户订阅
        old_plan = user.subscription
        user.subscription = new_plan
        
        #