"""
Jules Worker Daemon
Polls for tasks and executes them using Antigravity.
"""
import os
import sys
import time
import json
import socket
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# Configuration
API_URL = os.getenv("JULES_API_URL", "http://100.x.x.x:8080")  # Tailscale IP
NODE_ID = os.getenv("JULES_NODE_ID", socket.gethostname())
HEARTBEAT_INTERVAL = 30  # seconds
POLL_INTERVAL = 5  # seconds
WORK_DIR = Path(os.getenv("JULES_WORK_DIR", "/tmp/jules-work"))

class Worker:
    def __init__(self):
        self.node_id = NODE_ID
        self.tailscale_ip = self._get_tailscale_ip()
        self.current_task = None
        self.running = True

        WORK_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[Jules Worker] Node: {self.node_id} | IP: {self.tailscale_ip}")

    def _get_tailscale_ip(self) -> str:
        """Get this node's Tailscale IP."""
        try:
            result = subprocess.run(
                ["tailscale", "ip", "-4"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    def heartbeat(self):
        """Send heartbeat to API."""
        try:
            requests.post(f"{API_URL}/api/workers/heartbeat", json={
                "node_id": self.node_id,
                "tailscale_ip": self.tailscale_ip,
                "status": "busy" if self.current_task else "idle",
                "last_heartbeat": datetime.utcnow().isoformat(),
                "current_task": self.current_task,
            }, timeout=5)
        except Exception as e:
            print(f"[Heartbeat] Failed: {e}")

    def poll_task(self) -> dict | None:
        """Poll for pending tasks."""
        try:
            resp = requests.get(f"{API_URL}/api/tasks", params={"status": "pending", "limit": 1}, timeout=5)
            tasks = resp.json()
            return tasks[0] if tasks else None
        except Exception as e:
            print(f"[Poll] Failed: {e}")
            return None

    def claim_task(self, task_id: str) -> bool:
        """Attempt to claim a task."""
        try:
            resp = requests.patch(f"{API_URL}/api/tasks/{task_id}", params={
                "status": "running"
            }, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def execute_task(self, task: dict):
        """Execute task using Antigravity."""
        task_id = task["id"]
        repo = task["repo"]
        prompt = task["prompt"]
        branch = task["branch"]

        print(f"[Execute] Starting {task_id}: {prompt[:50]}...")

        work_path = WORK_DIR / task_id
        work_path.mkdir(exist_ok=True)

        try:
            # Clone repo
            subprocess.run([
                "gh", "repo", "clone", repo, str(work_path),
                "--", "--depth=1"
            ], check=True, timeout=120)

            # Create branch
            subprocess.run([
                "git", "-C", str(work_path),
                "checkout", "-b", branch
            ], check=True)

            # TODO: Run Antigravity here
            # For now, simulate work
            print(f"[Execute] Would run: antigravity --prompt '{prompt}' in {work_path}")
            time.sleep(2)

            # Create PR
            subprocess.run([
                "gh", "pr", "create",
                "--repo", repo,
                "--head", branch,
                "--title", f"[Jules] {prompt[:50]}",
                "--body", f"## \U0001f916 Jules Task {task_id}\n\n**Prompt**: {prompt}\n\n*Auto-generated*",
            ], cwd=work_path, check=True, timeout=60)

            # Update task status
            requests.patch(f"{API_URL}/api/tasks/{task_id}", params={"status": "completed"})
            print(f"[Execute] Completed {task_id}")

        except Exception as e:
            print(f"[Execute] Failed {task_id}: {e}")
            requests.patch(f"{API_URL}/api/tasks/{task_id}", params={"status": "failed"})
        finally:
            self.current_task = None

    def run(self):
        """Main worker loop."""
        last_heartbeat = 0

        while self.running:
            now = time.time()

            # Heartbeat
            if now - last_heartbeat > HEARTBEAT_INTERVAL:
                self.heartbeat()
                last_heartbeat = now

            # Poll for work if idle
            if not self.current_task:
                task = self.poll_task()
                if task and self.claim_task(task["id"]):
                    self.current_task = task["id"]
                    self.execute_task(task)

            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    worker = Worker()
    try:
        worker.run()
    except KeyboardInterrupt:
        print("\n[Worker] Shutting down...")
