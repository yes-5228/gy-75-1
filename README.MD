# 小区电梯维保系统

基于 Flask + Vue 的小区电梯维保管理系统，覆盖维保计划制定、巡检记录上传、故障报修、维修跟踪统计等核心流程。项目采用前后端分离与模块化目录，适合继续扩展鉴权、文件上传和多小区管理。

## 功能

- 维保计划：创建计划、选择电梯、指定日期和执行人、更新执行状态。
- 巡检记录：登记巡检人员、检查内容、结果和附件地址。
- 故障报修：提交故障类型、优先级、报修人和故障描述。
- 维修跟踪：为报修单追加维修过程、处理状态和费用。
- 统计总览：展示电梯数量、未关闭故障、已完成维修和累计费用。

## 项目结构

```text
backend/
  app/
    routes/       Flask 蓝图路由
    services/     业务服务
    repositories/ 数据提交辅助
    models.py     SQLAlchemy 数据模型
    seed.py       示例数据
  run.py
  requirements.txt
frontend/
  src/
    api/          接口封装
    components/   通用组件
    views/        业务视图
    App.vue
docker-compose.yml
README.MD
```

## 本地运行

Windows 下推荐使用一键启动脚本，它会使用独立端口启动后端和前端，并把日志写入 `.logs/`：

```powershell
.\scripts\start-dev.ps1
```

默认访问地址：`http://127.0.0.1:19024`

如需重置本地 SQLite 示例数据：

```powershell
.\scripts\reset-db.ps1
```

### 后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

后端默认地址：`http://127.0.0.1:5000`

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

## Docker Compose 启动

```bash
docker compose up --build
```

- 前端访问：`http://127.0.0.1:8080`
- 后端健康检查：`http://127.0.0.1:5000/api/health`
- SQLite 数据通过 `backend-data` 卷持久化。

## API 概览

- `GET /api/health`
- `GET /api/communities`
- `GET /api/elevators`
- `GET|POST /api/maintenance-plans`
- `PATCH /api/maintenance-plans/<id>`
- `GET|POST /api/inspections`
- `GET|POST /api/faults`
- `GET|POST /api/tracking`
- `GET /api/statistics`
