"""
Jules API - Control Plane
FastAPI application for task management and worker coordination.
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import sqlite3
import json

app = FastAPI(
    title="Jules API",
    description="Distributed AI Development System",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cloudflare Access handles auth
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class TaskStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskType(str, Enum):
    BRAINSTORM = "brainstorm"
    IMPLEMENT = "implement"
    REVIEW = "review"
    FIX = "fix"

class TaskCreate(BaseModel):
    repo: str = Field(..., example="atnplex/antigravity-manager")
    prompt: str = Field(..., example="Add dark mode support")
    task_type: TaskType = TaskType.IMPLEMENT
    priority: str = Field(default="normal", pattern="^(low|normal|high)$")

class Task(BaseModel):
    id: str
    repo: str
    prompt: str
    task_type: TaskType
    priority: str
    status: TaskStatus
    branch: Optional[str] = None
    pr_url: Optional[str] = None
    worker_id: Optional[str] = None
    model_used: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    commits: List[str] = []

class WorkerHealth(BaseModel):
    node_id: str
    tailscale_ip: str
    status: str
    last_heartbeat: datetime
    current_task: Optional[str] = None

# --- Database ---

def get_db():
    conn = sqlite3.connect("jules.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            repo TEXT NOT NULL,
            prompt TEXT NOT NULL,
            task_type TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            branch TEXT,
            pr_url TEXT,
            worker_id TEXT,
            model_used TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            commits TEXT DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS workers (
            node_id TEXT PRIMARY KEY,
            tailscale_ip TEXT,
            status TEXT NOT NULL,
            last_heartbeat TEXT NOT NULL,
            current_task TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_workers_status ON workers(status);
    """)
    conn.commit()

init_db()

# --- Task Endpoints ---

@app.post("/api/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    """Create a new development task."""
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    branch = f"jules/{task_id}/{task.prompt[:20].lower().replace(' ', '-')}"
    now = datetime.utcnow().isoformat()

    conn = get_db()
    conn.execute("""
        INSERT INTO tasks (id, repo, prompt, task_type, priority, status, branch, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (task_id, task.repo, task.prompt, task.task_type.value, task.priority, TaskStatus.PENDING.value, branch, now, now))
    conn.commit()

    # TODO: Push to Redis queue

    return Task(
        id=task_id,
        repo=task.repo,
        prompt=task.prompt,
        task_type=task.task_type,
        priority=task.priority,
        status=TaskStatus.PENDING,
        branch=branch,
        created_at=datetime.fromisoformat(now),
        updated_at=datetime.fromisoformat(now),
    )

@app.get("/api/tasks", response_model=List[Task])
async def list_tasks(status: Optional[TaskStatus] = None, limit: int = 50):
    """List all tasks, optionally filtered by status."""
    conn = get_db()
    if status:
        rows = conn.execute("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?", (status.value, limit)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()

    return [Task(**dict(row), commits=json.loads(row["commits"])) for row in rows]

@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**dict(row), commits=json.loads(row["commits"]))

@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: str, status: Optional[TaskStatus] = None, pr_url: Optional[str] = None):
    """Update task status (used by workers)."""
    conn = get_db()
    updates = []
    values = []

    if status:
        updates.append("status = ?")
        values.append(status.value)
    if pr_url:
        updates.append("pr_url = ?")
        values.append(pr_url)

    updates.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())
    values.append(task_id)

    conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", values)
    conn.commit()
    return {"updated": True}

# --- Worker Endpoints ---

@app.post("/api/workers/heartbeat")
async def worker_heartbeat(health: WorkerHealth):
    """Workers call this to report health."""
    conn = get_db()
    conn.execute("""
        INSERT OR REPLACE INTO workers (node_id, tailscale_ip, status, last_heartbeat, current_task)
        VALUES (?, ?, ?, ?, ?)
    """, (health.node_id, health.tailscale_ip, health.status, health.last_heartbeat.isoformat(), health.current_task))
    conn.commit()
    return {"ack": True}

@app.get("/api/workers", response_model=List[WorkerHealth])
async def list_workers():
    """List all registered workers."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM workers ORDER BY last_heartbeat DESC").fetchall()
    return [WorkerHealth(**dict(row)) for row in rows]

# --- WebSocket for Live Updates ---

active_connections: dict[str, WebSocket] = {}

@app.websocket("/ws/task/{task_id}")
async def websocket_task(websocket: WebSocket, task_id: str):
    await websocket.accept()
    active_connections[task_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # Client can send pings
    except WebSocketDisconnect:
        del active_connections[task_id]

# --- Health Check ---

@app.get("/health")
async def health():
    return {"status": "ok", "service": "jules-api"}
