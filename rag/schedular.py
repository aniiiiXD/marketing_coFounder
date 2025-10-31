"""
Scheduler - Simple Task Scheduling

Handles periodic tasks like data refresh and cleanup.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Callable, Dict, Any
import time

logger = logging.getLogger(__name__)

class SimpleScheduler:
    """Basic scheduler for periodic tasks"""
    
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.running = False
    
    def add_task(self, name: str, func: Callable, interval_minutes: int):
        """Add a scheduled task"""
        self.tasks[name] = {
            "function": func,
            "interval": interval_minutes * 60,  # Convert to seconds
            "last_run": 0,
            "enabled": True
        }
        logger.info(f"Added scheduled task: {name} (every {interval_minutes} minutes)")
    
    def remove_task(self, name: str):
        """Remove a scheduled task"""
        if name in self.tasks:
            del self.tasks[name]
            logger.info(f"Removed scheduled task: {name}")
    
    def enable_task(self, name: str):
        """Enable a task"""
        if name in self.tasks:
            self.tasks[name]["enabled"] = True
    
    def disable_task(self, name: str):
        """Disable a task"""
        if name in self.tasks:
            self.tasks[name]["enabled"] = False
    
    async def start(self):
        """Start the scheduler"""
        self.running = True
        logger.info("Scheduler started")
        
        while self.running:
            current_time = time.time()
            
            for name, task in self.tasks.items():
                if not task["enabled"]:
                    continue
                
                if current_time - task["last_run"] >= task["interval"]:
                    try:
                        logger.info(f"Running scheduled task: {name}")
                        
                        # Run the task
                        if asyncio.iscoroutinefunction(task["function"]):
                            await task["function"]()
                        else:
                            task["function"]()
                        
                        task["last_run"] = current_time
                        logger.info(f"Completed scheduled task: {name}")
                        
                    except Exception as e:
                        logger.error(f"Error in scheduled task {name}: {e}")
            
            # Sleep for 60 seconds before checking again
            await asyncio.sleep(60)
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("Scheduler stopped")
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get status of all tasks"""
        status = {}
        current_time = time.time()
        
        for name, task in self.tasks.items():
            next_run = task["last_run"] + task["interval"]
            status[name] = {
                "enabled": task["enabled"],
                "interval_minutes": task["interval"] / 60,
                "last_run": datetime.fromtimestamp(task["last_run"]).isoformat() if task["last_run"] > 0 else "Never",
                "next_run": datetime.fromtimestamp(next_run).isoformat(),
                "seconds_until_next": max(0, int(next_run - current_time))
            }
        
        return status