# FastKit Jobs Service Guide

## 🎯 Overview

The FastKit Jobs Service provides a comprehensive background job scheduling and processing system for FastAPI applications. It supports multiple popular job queue and scheduler libraries with a unified, easy-to-use interface.

## 🚀 Quick Start

### Add Jobs Service to Your Project

```bash
# Choose your preferred job scheduler
fastkit add-service jobs celery      # Production-ready distributed tasks
fastkit add-service jobs rq          # Simple Redis-based jobs
fastkit add-service jobs apscheduler # In-process scheduling
fastkit add-service jobs dramatiq    # Modern Celery alternative
fastkit add-service jobs arq         # Async Redis Queue (FastAPI-friendly)
```

### Basic Usage

After adding the jobs service, you can immediately start creating tasks:

```python
# app/jobs/tasks.py
from app.jobs import task

@task(name="send_email")
def send_email(to: str, subject: str, body: str):
    """Send email notification."""
    # Your email sending logic here
    return f"Email sent to {to}"

@task(
    name="cleanup_task",
    schedule={
        "type": "interval",
        "seconds": 300  # Run every 5 minutes
    }
)
def cleanup_task():
    """Cleanup task that runs every 5 minutes."""
    # Your cleanup logic here
    return "Cleanup completed"
```

## 📋 Supported Job Schedulers

### 1. Celery - Production-Ready Distributed Tasks

**Best for:** Large-scale applications, distributed systems, complex workflows

**Features:**
- Distributed task execution
- Advanced routing and workflows
- Comprehensive monitoring
- Battle-tested in production

**Usage:**
```python
from app.jobs import task, scheduler

# Define task
@task(name="process_data")
def process_data(data_id: int):
    return f"Processed data {data_id}"

# Run immediately
result = scheduler.run_task("process_data", 123)

# Schedule for later
scheduler.schedule_task("process_data", countdown=60, data_id=456)
```

**Worker Commands:**
```bash
# Start Celery worker
celery -A app.jobs.celery_scheduler worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A app.jobs.celery_scheduler beat --loglevel=info
```

### 2. RQ - Simple Redis-Based Jobs

**Best for:** Simple job processing, quick setup, lightweight applications

**Features:**
- Simple and lightweight
- Redis-based storage
- Easy monitoring
- Minimal configuration

**Usage:**
```python
from app.jobs import task, scheduler

@task(name="generate_report")
def generate_report(user_id: int):
    return f"Report generated for user {user_id}"

# Run immediately
job_id = scheduler.run_task("generate_report", 123)

# Schedule for later
job_id = scheduler.schedule_task("generate_report", when=300, user_id=456)
```

**Worker Commands:**
```bash
# Start RQ worker
rq worker --url redis://localhost:6379/0

# Start RQ scheduler (for scheduled tasks)
rqscheduler --host localhost --port 6379 --db 0
```

### 3. APScheduler - In-Process Scheduling

**Best for:** Simple applications, cron-like scheduling, no external dependencies

**Features:**
- In-process execution
- No external broker required
- Cron-like scheduling
- Persistent job stores

**Usage:**
```python
from app.jobs import task, scheduler

@task(
    name="daily_backup",
    schedule={
        "type": "cron",
        "hour": "2",
        "minute": "0"
    }
)
def daily_backup():
    return "Backup completed"

# Start scheduler (call this in your app startup)
scheduler.start()
```

### 4. Dramatiq - Modern Celery Alternative

**Best for:** Modern Python applications, simple distributed tasks, reliability

**Features:**
- Modern Python design
- Simple and reliable
- Good error handling
- Less complex than Celery

**Usage:**
```python
from app.jobs import task

@task(name="process_image")
def process_image(image_path: str):
    return f"Processed image {image_path}"

# Tasks are automatically queued when called
process_image.send("path/to/image.jpg")
```

**Worker Commands:**
```bash
# Start Dramatiq worker
dramatiq app.jobs.tasks
```

### 5. ARQ - Async Redis Queue

**Best for:** FastAPI applications, async tasks, modern async/await patterns

**Features:**
- Async/await native
- FastAPI-friendly
- Redis-based
- Cron job support

**Usage:**
```python
from app.jobs import task, run_task, schedule_task

@task(name="async_process")
async def async_process(data: dict):
    # Async processing logic
    return "Processed"

# Run tasks (these are async)
await run_task("async_process", {"key": "value"})
await schedule_task("async_process", when=60, data={"key": "value"})
```

**Worker Commands:**
```bash
# Start ARQ worker
arq app.jobs.arq_scheduler.ARQScheduler
```

## 🔧 Job Configuration

### Schedule Types

#### 1. Interval Scheduling
```python
@task(
    name="periodic_task",
    schedule={
        "type": "interval",
        "seconds": 60,      # Every minute
        "minutes": 5,       # Every 5 minutes
        "hours": 1,         # Every hour
        "days": 1,          # Every day
        "weeks": 1          # Every week
    }
)
def periodic_task():
    return "Task completed"
```

#### 2. Cron Scheduling
```python
@task(
    name="cron_task",
    schedule={
        "type": "cron",
        "minute": "0",           # At minute 0
        "hour": "2",             # At 2 AM
        "day_of_month": "*",     # Every day
        "month_of_year": "*",    # Every month
        "day_of_week": "1"       # Monday
    }
)
def cron_task():
    return "Cron task completed"
```

#### 3. One-time Scheduling
```python
@task(name="one_time_task")
def one_time_task():
    return "One-time task completed"

# Schedule to run in 5 minutes
scheduler.schedule_task("one_time_task", countdown=300)

# Schedule to run at specific time
from datetime import datetime, timedelta
future_time = datetime.now() + timedelta(hours=1)
scheduler.schedule_task("one_time_task", eta=future_time)
```

## 🏗️ Project Structure

After adding a jobs service, your project structure will include:

```
your-project/
├── app/
│   ├── jobs/
│   │   ├── __init__.py              # Scheduler interface
│   │   ├── {provider}_scheduler.py  # Provider-specific scheduler
│   │   └── tasks.py                 # Example tasks
│   └── ...
└── ...
```

## 🔍 Monitoring and Management

### Task Status Checking

```python
from app.jobs import scheduler

# Get task status
status = scheduler.get_task_status(job_id)
print(f"Status: {status}")

# List all registered tasks
tasks = scheduler.list_tasks()
print(f"Available tasks: {tasks}")
```

### Job Management

```python
# Cancel a scheduled job
scheduler.cancel_task(job_id)

# Pause a job (APScheduler only)
scheduler.pause_task(job_id)

# Resume a paused job (APScheduler only)
scheduler.resume_task(job_id)
```

## 🛠️ Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Redis-based schedulers (Celery, RQ, Dramatiq, ARQ)
REDIS_URL=redis://localhost:6379/0

# Celery-specific
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Job settings
JOB_TIMEOUT=1800  # 30 minutes
JOB_RETRY_LIMIT=3
```

### Application Integration

#### FastAPI Startup Events

```python
# app/main.py
from fastapi import FastAPI
from app.jobs import scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # For APScheduler
    if hasattr(scheduler, 'start'):
        scheduler.start()
    
    # For ARQ
    if hasattr(scheduler, 'connect'):
        await scheduler.connect()

@app.on_event("shutdown")
async def shutdown_event():
    # For APScheduler
    if hasattr(scheduler, 'shutdown'):
        scheduler.shutdown()
    
    # For ARQ
    if hasattr(scheduler, 'close'):
        await scheduler.close()
```

## 📝 Best Practices

### 1. Task Design

```python
# ✅ Good: Idempotent tasks
@task(name="update_user_stats")
def update_user_stats(user_id: int):
    # Safe to run multiple times
    user = get_user(user_id)
    user.stats = calculate_stats(user)
    user.save()

# ❌ Bad: Non-idempotent tasks
@task(name="increment_counter")
def increment_counter():
    # Dangerous if run multiple times
    counter += 1
```

### 2. Error Handling

```python
@task(name="robust_task")
def robust_task(data: dict):
    try:
        # Task logic here
        result = process_data(data)
        return result
    except Exception as e:
        # Log error
        logger.error(f"Task failed: {e}")
        # Re-raise for retry mechanism
        raise
```

### 3. Task Monitoring

```python
@task(name="monitored_task")
def monitored_task(item_id: int):
    logger.info(f"Starting task for item {item_id}")
    
    try:
        result = process_item(item_id)
        logger.info(f"Task completed for item {item_id}")
        return result
    except Exception as e:
        logger.error(f"Task failed for item {item_id}: {e}")
        raise
```

## 🚀 Production Deployment

### Docker Configuration

```dockerfile
# Dockerfile.worker
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# For Celery
CMD ["celery", "-A", "app.jobs.celery_scheduler", "worker", "--loglevel=info"]

# For RQ
# CMD ["rq", "worker", "--url", "redis://redis:6379/0"]

# For Dramatiq
# CMD ["dramatiq", "app.jobs.tasks"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
  
  worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: job-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: job-worker
  template:
    metadata:
      labels:
        app: job-worker
    spec:
      containers:
      - name: worker
        image: your-app:latest
        command: ["celery", "-A", "app.jobs.celery_scheduler", "worker"]
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379/0"
```

## 🔧 Troubleshooting

### Common Issues

1. **Redis Connection Errors**
   ```bash
   # Check Redis is running
   redis-cli ping
   
   # Check connection string
   echo $REDIS_URL
   ```

2. **Tasks Not Executing**
   ```bash
   # Check worker is running
   ps aux | grep celery
   
   # Check queue status
   celery -A app.jobs.celery_scheduler inspect active
   ```

3. **Import Errors**
   ```python
   # Ensure tasks are imported
   from app.jobs import tasks  # This registers tasks
   ```

### Performance Tuning

```python
# Celery optimization
app.conf.update(
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
)

# RQ optimization
worker = Worker(queues, connection=redis_conn)
worker.work(burst=False, logging_level='INFO')
```

## 📚 Examples

### Email Service Integration

```python
@task(name="send_welcome_email")
def send_welcome_email(user_id: int):
    user = User.get(user_id)
    email_service.send_template_email(
        to=user.email,
        template="welcome",
        context={"name": user.name}
    )
    return f"Welcome email sent to {user.email}"

# Usage in your API
@app.post("/register")
async def register_user(user_data: UserCreate):
    user = create_user(user_data)
    
    # Send welcome email asynchronously
    scheduler.run_task("send_welcome_email", user.id)
    
    return {"message": "User created", "user_id": user.id}
```

### Data Processing Pipeline

```python
@task(name="process_uploaded_file")
def process_uploaded_file(file_path: str, user_id: int):
    # Process file
    data = parse_file(file_path)
    
    # Validate data
    validated_data = validate_data(data)
    
    # Store in database
    result = store_data(validated_data, user_id)
    
    # Notify user
    scheduler.run_task("send_processing_complete_email", user_id, result.id)
    
    return f"Processed {len(validated_data)} records"

@task(name="send_processing_complete_email")
def send_processing_complete_email(user_id: int, result_id: int):
    # Send notification email
    pass
```

### Scheduled Reports

```python
@task(
    name="generate_daily_report",
    schedule={
        "type": "cron",
        "hour": "6",
        "minute": "0"
    }
)
def generate_daily_report():
    # Generate report
    report_data = generate_report_data()
    
    # Save report
    report = save_report(report_data)
    
    # Email to administrators
    for admin in get_admin_users():
        scheduler.run_task("send_report_email", admin.id, report.id)
    
    return f"Daily report generated: {report.id}"
```

This comprehensive jobs service provides everything you need for background task processing in your FastAPI applications, from simple scheduled tasks to complex distributed workflows!