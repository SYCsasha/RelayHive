# RelayHive

RelayHive 是一个面向任务接力的 AI 协作后端框架。

## 当前 MVP（后端核心）

- FastAPI 程序入口：`app/main.py`
- Task Center 基础模型：`app/schemas/task.py`
  - 支持父子任务
  - 支持标签与状态
  - 支持事件日志字段
- Tag Protocol v1 数据结构：`app/protocol/tag_protocol.py`
- 任务 API：
  - `POST /api/v1/tasks` 创建任务
  - `GET /api/v1/tasks` 列出任务

## 本地开发

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

测试：

```bash
pytest
```