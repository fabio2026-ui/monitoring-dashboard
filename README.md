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
