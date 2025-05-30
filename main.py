from app.classifier import TaskClassifier
from app.task_manager import TaskManager

def show_tasks(tasks):
    print("\n🗂️ Your Tasks:")
    if not tasks:
        print("📭 No tasks found.")
    for task in tasks:
        print(f"🆔 {task[0]} | 📝 {task[1]} | 🏷️ {task[2]} | 📅 {task[4]} | ✅ {task[3]}")

def menu():
    print("\n🤖 What would you like to do?")
    print("1. Add new task")
    print("2. View all tasks")
    print("3. View only pending tasks")
    print("4. View only completed tasks")
    print("5. Mark task as done")
    print("6. Delete task")
    print("7. Edit task") 
    print("8. Search tasks") 
    print("9. Delete all completed tasks")
    print("0. Exit")

if __name__ == "__main__":
    clf = TaskClassifier()
    tm = TaskManager()

    while True:
        menu()
        choice = input("Enter option (0-9): ")



        if choice == "1":
            task = input("Enter your task: ").strip()
            if not task:
                  print("❗ Task cannot be empty.")
                  continue
            category = clf.classify_task(task)
            tm.add_task(task, category)
            print(f"\n📌 Task: {task}")
            print(f"🗂️ Predicted Category: {category}")
            print("✅ Task saved to database!")

        elif choice == "2":
            show_tasks(tm.get_all_tasks())

        elif choice == "3":
            tasks = [t for t in tm.get_all_tasks() if t[3] == "pending"]
            show_tasks(tasks)

        elif choice == "4":
            tasks = [t for t in tm.get_all_tasks() if t[3] == "done"]
            show_tasks(tasks)

        elif choice == "5":
            task_id = int(input("Enter task ID to mark as done: "))
            tm.mark_done(task_id)
            print("✅ Task marked as done!")

        elif choice == "6":
            task_id = int(input("Enter task ID to delete: "))
            tm.delete_task(task_id)
            print("🗑️ Task deleted!")

        elif choice == "7":
            task_id = int(input("Enter task ID to edit: "))
            new_text = input("New task text (leave empty to keep same): ")
            new_category = input("New category (leave empty to keep same): ")

            new_text = new_text.strip() if new_text.strip() else None
            new_category = new_category.strip() if new_category.strip() else None

            tm.edit_task(task_id, new_text, new_category)
            print("✏️ Task updated!") 

        elif choice == "8":
            keyword = input("Enter keyword to search: ").strip()
            if not keyword:
                print("❗ Keyword cannot be empty.")
                continue
            
            results = tm.search_tasks(keyword)
            if results:
                print(f"\n🔍 Search results for '{keyword}':")
                show_tasks(results)
            else:
                print(f"📭 No tasks found for '{keyword}'.")

        elif choice == "9":
            confirm = input("Are you sure you want to delete all completed tasks? (y/n): ").strip().lower()
            if confirm == 'y':
                tm.delete_completed_tasks()
                print("🧹 All completed tasks deleted!")
            else:
                print("❌ Cancelled.")



        elif choice == "0":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Try again.")
