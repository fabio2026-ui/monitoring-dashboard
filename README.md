# monitoring-dashboard

监控仪表板 - 自动化部署

## 文件说明
## 📁 项目文件列表

- `revenue_monitoring_system.py`
- `advanced_project_monitor.py`
- `project_priority_system.py`
- `project_priority_dashboard.md`
- `project_monitor_config.json`
- `quality_assurance_system.py`
- `quality_assurance_system_complete.py`
- `auto_fix_quality_issues.py`
- `ai_team_optimization_system.py`
- `active_income_generation_system.py`
- `active_income_execution_plan_v2.json`
- `实战营销优化系统.py`
- `实战营销报告.json`
- `build_marketing_system.py`
- `team_management_system.py`
- `real_team_members.json`
- `team_night_tasks.json`
- `reduced_report_system.py`
- `report_scheduler.py`
- `token_optimizer_skill.py`
- `check_all_services_simple.py`
- `restart_all_projects.py`
- `start_all_projects.py`
- `start_highspeed.py`
- `start_highspeed.sh`
- `start_project_1.py`
- `install_full_dependencies.py`
- `shared-components/ai-workflow/workflow_engine.py`
- `shared-components/quality-system/quality_validator.py`
- `shared-components/user-management/user_manager.py`

这是一个自动化生成的GitHub仓库。

## 部署状态
- ✅ 仓库创建完成
- ⚡ 文件准备中
- 🚀 即将推送完整项目

## 联系
- GitHub: [fabio2026-ui](https://github.com/fabio2026-ui)
- Email: fufansong@gmail.com

## 🐳 Docker 部署
## 🧪 测试

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行特定测试文件
pytest tests/test_monitoring_dashboard.py

# 运行集成测试
pytest tests/test_integration_monitoring_dashboard.py -v
```

### 测试覆盖率

项目使用pytest-cov进行测试覆盖率统计。目标覆盖率:

- **单元测试**: ≥80%
- **集成测试**: ≥70%
- **总体覆盖率**: ≥75%

### 测试类型

1. **单元测试**: 测试单个函数和类
2. **集成测试**: 测试组件之间的交互
3. **端到端测试**: 测试完整工作流程
4. **性能测试**: 测试系统性能
5. **安全测试**: 测试安全漏洞

### 持续集成

GitHub Actions自动运行测试:
- 每次推送到main分支
- 每次拉取请求
- 每天凌晨自动运行

### 测试报告

测试报告可在以下位置查看:
- **GitHub Actions**: 工作流运行详情
- **Codecov**: 代码覆盖率报告
- **测试产物**: HTML覆盖率报告

### 测试最佳实践

- 每个测试应该独立运行
- 使用fixture进行测试数据准备
- 模拟外部依赖
- 测试边界情况和错误场景
- 保持测试快速运行

## 📦 GitHub Container Registry

### 自动构建的容器镜像

每次推送到main分支时，GitHub Actions会自动构建并推送Docker镜像到GitHub Container Registry。

**镜像地址**: `ghcr.io/fabio2026-ui/monitoring-dashboard:latest`

### 拉取和使用镜像

```bash
# 拉取最新镜像
docker pull ghcr.io/fabio2026-ui/monitoring-dashboard:latest

# 运行容器
docker run -d -p 8080:8000 --name monitoring-dashboard ghcr.io/fabio2026-ui/monitoring-dashboard:latest

# 使用docker-compose
version: '3.8'
services:
  monitoring-dashboard:
    image: ghcr.io/fabio2026-ui/monitoring-dashboard:latest
    ports:
      - "8080:8000"
```

### 手动构建和推送

```bash
# 登录到GitHub Container Registry
echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin

# 构建镜像
docker build -t ghcr.io/fabio2026-ui/monitoring-dashboard:latest .

# 推送镜像
docker push ghcr.io/fabio2026-ui/monitoring-dashboard:latest
```


### 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/fabio2026-ui/monitoring-dashboard.git
   cd monitoring-dashboard
   ```

2. **使用Docker部署**
   ```bash
   # 方法1: 使用部署脚本
   ./deploy.sh
   
   # 方法2: 手动部署
   docker-compose build
   docker-compose up -d
   ```

3. **访问应用**
   - 本地访问: http://localhost:8080
   - 容器状态: `docker ps | grep monitoring-dashboard`
   - 查看日志: `docker logs monitoring-dashboard`

### 管理命令

```bash
# 停止容器
docker-compose down

# 重启容器
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker exec -it monitoring-dashboard bash
```

### 生产环境部署

对于生产环境，建议使用:
- **Docker Swarm** 或 **Kubernetes** 进行容器编排
- **Traefik** 或 **Nginx** 作为反向代理
- **Let's Encrypt** 进行SSL证书管理
