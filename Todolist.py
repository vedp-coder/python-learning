

# To-Do List Application
def todo_list():
    tasks = []
    
    while True:
        print("\nTo-Do List Application")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Exit")
        
        choice = input("Select option (1-4): ")
        
        if choice == "1":
            task = input("Enter task: ")
            tasks.append({"task": task, "completed": False})
            print("Task added!")
        
        elif choice == "2":
            if tasks:
                for i, task in enumerate(tasks, 1):
                    status = "✓" if task["completed"] else " "
                    print(f"{i}. [{status}] {task['task']}")
            else:
                print("No tasks yet!")
        
        elif choice == "3":
            if tasks:
                try:
                    task_num = int(input("Enter task number to complete: ")) - 1
                    if 0 <= task_num < len(tasks):
                        tasks[task_num]["completed"] = True
                        print("Task marked as complete!")
                    else:
                        print("Invalid task number")
                except ValueError:
                    print("Please enter a valid number")
            else:
                print("No tasks to complete!")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

# Run either application
if __name__ == "__main__":

