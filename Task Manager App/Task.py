import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Task:
    """Represents a single task with basic properties."""
    
    def __init__(self, title: str, description: str = "", priority: str = "medium"):
        self.id = int(datetime.now().timestamp() * 1000)  # Unique ID
        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def mark_complete(self):
        """Mark task as completed."""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def mark_incomplete(self):
        """Mark task as incomplete."""
        self.completed = False
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create task from dictionary."""
        task = cls(data['title'], data.get('description', ''), data.get('priority', 'medium'))
        task.id = data['id']
        task.completed = data.get('completed', False)
        task.created_at = data.get('created_at', datetime.now().isoformat())
        task.completed_at = data.get('completed_at')
        return task
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        priority_symbols = {"low": "↓", "medium": "→", "high": "↑"}
        priority_symbol = priority_symbols.get(self.priority, "→")
        
        return f"{status} [{priority_symbol}] {self.title}"

class TaskManager:
    """Manages a collection of tasks with persistence."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """Add a new task."""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = Task(title.strip(), description.strip(), priority)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def update_task(self, task_id: int, title: str = None, description: str = None, 
                   priority: str = None) -> bool:
        """Update an existing task."""
        task = self.get_task(task_id)
        if not task:
            return False
        
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if priority is not None:
            task.priority = priority.lower()
        
        self.save_tasks()
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def toggle_task(self, task_id: int) -> bool:
        """Toggle task completion status."""
        task = self.get_task(task_id)
        if not task:
            return False
        
        if task.completed:
            task.mark_incomplete()
        else:
            task.mark_complete()
        
        self.save_tasks()
        return True
    
    def list_tasks(self, show_completed: bool = True, filter_priority: str = None) -> List[Task]:
        """List tasks with optional filters."""
        filtered_tasks = self.tasks
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        
        if filter_priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == filter_priority.lower()]
        
        # Sort by priority (high -> medium -> low) and then by created date
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(filtered_tasks, key=lambda t: (priority_order.get(t.priority, 1), t.created_at))
    
    def get_stats(self) -> Dict:
        """Get task statistics."""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            if not task.completed:
                priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "high_priority": priority_counts["high"],
            "medium_priority": priority_counts["medium"],
            "low_priority": priority_counts["low"]
        }
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                task_data = json.load(f)
                self.tasks = [Task.from_dict(data) for data in task_data]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

class TaskManagerCLI:
    """Command-line interface for the Task Manager."""
    
    def __init__(self):
        self.manager = TaskManager()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("          TASK MANAGER")
        print("="*50)
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Toggle Task (Complete/Incomplete)")
        print("5. Delete Task")
        print("6. View Statistics")
        print("7. Filter Tasks")
        print("8. Exit")
        print("="*50)
    
    def add_task_interactive(self):
        """Interactive task addition."""
        print("\n--- Add New Task ---")
        title = input("Task title: ").strip()
        
        if not title:
            print("❌ Task title cannot be empty!")
            return
        
        description = input("Description (optional): ").strip()
        
        print("Priority levels: low, medium, high")
        priority = input("Priority (default: medium): ").strip() or "medium"
        
        if priority.lower() not in ["low", "medium", "high"]:
            print("Invalid priority. Using 'medium' as default.")
            priority = "medium"
        
        try:
            task = self.manager.add_task(title, description, priority)
            print(f"✅ Task added successfully! ID: {task.id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def list_tasks_interactive(self):
        """Interactive task listing."""
        print("\n--- Task List ---")
        
        show_completed = input("Show completed tasks? (y/n, default: y): ").strip().lower()
        show_completed = show_completed != 'n'
        
        tasks = self.manager.list_tasks(show_completed=show_completed)
        
        if not tasks:
            print("📝 No tasks found.")
            return
        
        print(f"\nFound {len(tasks)} task(s):")
        print("-" * 60)
        
        for task in tasks:
            created = datetime.fromisoformat(task.created_at).strftime("%m/%d %H:%M")
            print(f"ID: {task.id} | {task} | Created: {created}")
            if task.description:
                print(f"    📄 {task.description}")
            print()
    
    def update_task_interactive(self):
        """Interactive task updating."""
        print("\n--- Update Task ---")
        
        try:
            task_id = int(input("Enter task ID: "))
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print("❌ Task not found!")
            return
        
        print(f"Current task: {task}")
        print(f"Description: {task.description}")
        print(f"Priority: {task.priority}")
        
        new_title = input(f"New title (current: '{task.title}'): ").strip()
        new_description = input(f"New description (current: '{task.description}'): ").strip()
        new_priority = input(f"New priority (current: '{task.priority}'): ").strip()
        
        # Only update non-empty inputs
        title = new_title if new_title else None
        description = new_description if new_description else None
        priority = new_priority if new_priority else None
        
        if self.manager.update_task(task_id, title, description, priority):
            print("✅ Task updated successfully!")
        else:
            print("❌ Failed to update task!")
    
    def toggle_task_interactive(self):
        """Interactive task toggling."""
        print("\n--- Toggle Task Status ---")
        
        try:
            task_id = int(input("Enter task ID: "))
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print("❌ Task not found!")
            return
        
        old_status = "completed" if task.completed else "pending"
        
        if self.manager.toggle_task(task_id):
            new_status = "completed" if task.completed else "pending"
            print(f"✅ Task status changed from {old_status} to {new_status}!")
        else:
            print("❌ Failed to toggle task!")
    
    def delete_task_interactive(self):
        """Interactive task deletion."""
        print("\n--- Delete Task ---")
        
        try:
            task_id = int(input("Enter task ID: "))
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print("❌ Task not found!")
            return
        
        print(f"Task to delete: {task}")
        confirm = input("Are you sure? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if self.manager.delete_task(task_id):
                print("✅ Task deleted successfully!")
            else:
                print("❌ Failed to delete task!")
        else:
            print("❌ Deletion cancelled.")
    
    def show_statistics(self):
        """Display task statistics."""
        print("\n--- Task Statistics ---")
        stats = self.manager.get_stats()
        
        print(f"📊 Total Tasks: {stats['total']}")
        print(f"✅ Completed: {stats['completed']}")
        print(f"⏳ Pending: {stats['pending']}")
        print("\nPending by Priority:")
        print(f"  🔴 High: {stats['high_priority']}")
        print(f"  🟡 Medium: {stats['medium_priority']}")
        print(f"  🟢 Low: {stats['low_priority']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            print(f"\n📈 Completion Rate: {completion_rate:.1f}%")
    
    def filter_tasks_interactive(self):
        """Interactive task filtering."""
        print("\n--- Filter Tasks ---")
        print("Available filters:")
        print("1. By Priority (high/medium/low)")
        print("2. Pending tasks only")
        print("3. Completed tasks only")
        
        choice = input("Choose filter (1-3): ").strip()
        
        if choice == "1":
            priority = input("Enter priority (high/medium/low): ").strip().lower()
            if priority in ["high", "medium", "low"]:
                tasks = self.manager.list_tasks(filter_priority=priority)
                print(f"\n--- {priority.title()} Priority Tasks ---")
            else:
                print("❌ Invalid priority!")
                return
        elif choice == "2":
            tasks = self.manager.list_tasks(show_completed=False)
            print("\n--- Pending Tasks ---")
        elif choice == "3":
            tasks = [task for task in self.manager.tasks if task.completed]
            print("\n--- Completed Tasks ---")
        else:
            print("❌ Invalid choice!")
            return
        
        if not tasks:
            print("📝 No tasks found matching the filter.")
            return
        
        print(f"Found {len(tasks)} task(s):")
        print("-" * 60)
        
        for task in tasks:
            created = datetime.fromisoformat(task.created_at).strftime("%m/%d %H:%M")
            print(f"ID: {task.id} | {task} | Created: {created}")
            if task.description:
                print(f"    📄 {task.description}")
            print()
    
    def run(self):
        """Run the CLI application."""
        print("🚀 Welcome to Task Manager!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                self.add_task_interactive()
            elif choice == "2":
                self.list_tasks_interactive()
            elif choice == "3":
                self.update_task_interactive()
            elif choice == "4":
                self.toggle_task_interactive()
            elif choice == "5":
                self.delete_task_interactive()
            elif choice == "6":
                self.show_statistics()
            elif choice == "7":
                self.filter_tasks_interactive()
            elif choice == "8":
                print("\n👋 Thank you for using Task Manager!")
                break
            else:
                print("❌ Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point of the application."""
    try:
        cli = TaskManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
