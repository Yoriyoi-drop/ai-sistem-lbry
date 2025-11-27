"""
Celery application configuration for background tasks

Created: 2025-11-26
"""

from celery import Celery
from celery.schedules import crontab
import os

# Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Create Celery app
celery_app = Celery(
    "infinite_ai_security",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=[
        "apps.api.src.tasks.security_tasks",
        "apps.api.src.tasks.cleanup_tasks",
        "apps.api.src.tasks.notification_tasks",
        "apps.api.src.tasks.report_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    beat_schedule={
        "cleanup-old-scans": {
            "task": "apps.api.src.tasks.cleanup_tasks.cleanup_old_scans",
            "schedule": crontab(hour=2, minute=0),  # Run at 2 AM daily
        },
        "cleanup-expired-sessions": {
            "task": "apps.api.src.tasks.cleanup_tasks.cleanup_expired_sessions",
            "schedule": crontab(minute="*/30"),  # Every 30 minutes
        },
        "generate-daily-reports": {
            "task": "apps.api.src.tasks.report_tasks.generate_daily_security_report",
            "schedule": crontab(hour=8, minute=0),  # Run at 8 AM daily
        },
    },
)

# Task routes
celery_app.conf.task_routes = {
    "apps.api.src.tasks.security_tasks.*": {"queue": "security"},
    "apps.api.src.tasks.notification_tasks.*": {"queue": "notifications"},
    "apps.api.src.tasks.cleanup_tasks.*": {"queue": "maintenance"},
    "apps.api.src.tasks.report_tasks.*": {"queue": "reports"},
}


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f"Request: {self.request!r}")
    return "Task completed successfully"
