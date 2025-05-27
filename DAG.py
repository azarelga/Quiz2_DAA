class TaskSchedulerDAG:
    def __init__(self):
        self.graph = {}  # Stores task dependencies (adjacency list)
        self.in_degree = {}  # Stores the number of prerequisites for each task

    def add_task(self, task_name):
        if task_name not in self.graph:
            self.graph[task_name] = []
            self.in_degree[task_name] = 0

    def add_dependency(self, prerequisite_task, dependent_task):
        # Ensure tasks exist
        if prerequisite_task not in self.graph:
            raise ValueError(f"Task '{prerequisite_task}' does not exist.")
        if dependent_task not in self.graph:
            raise ValueError(f"Task '{dependent_task}' does not exist.")

        # Check for self-dependency
        if prerequisite_task == dependent_task:
            raise ValueError("A task cannot depend on itself.")

        # Check for cycles using DFS
        def has_path(start, target, visited=None):
            if visited is None:
                visited = set()
            if start == target:
                return True
            visited.add(start)
            for neighbor in self.graph[start]:
                if neighbor not in visited:
                    if has_path(neighbor, target, visited):
                        return True
            return False

        if has_path(dependent_task, prerequisite_task):
            raise ValueError(
                f"Cannot add dependency: adding {prerequisite_task} -> {dependent_task} would create a cycle."
            )

        # Add the edge
        self.graph[prerequisite_task].append(dependent_task)
        self.in_degree[dependent_task] += 1

    def get_execution_order(self):
        in_degree = self.in_degree.copy()  # Copy to avoid modifying original
        # Implements Kahn's algorithm for topological sort
        queue = [task for task in in_degree if in_degree[task] == 0]
        execution_order = []

        while queue:
            current_task = queue.pop(0)
            execution_order.append(current_task)

            for neighbor_task in self.graph[current_task]:
                in_degree[neighbor_task] -= 1
                if in_degree[neighbor_task] == 0:
                    queue.append(neighbor_task)

        return execution_order


# --- Example Usage ---
scheduler = TaskSchedulerDAG()

if __name__ == "__main__":
    while True:
        try:
            print("1. Add a task")
            print("2. Add a dependency")
            print("3. Get execution order")
            print("4. Exit")
            choice = input("Choose an option (1-4): ")
            match choice:
                case "1":
                    task_name = input("Enter task name: ")
                    scheduler.add_task(task_name)
                    print(f"Task '{task_name}' added.")
                case "2":
                    prerequisite = input("Enter prerequisite task: ")
                    dependent = input("Enter dependent task: ")
                    scheduler.add_dependency(prerequisite, dependent)
                    print(f"Dependency added: {prerequisite} -> {dependent}")
                case "3":
                    order = scheduler.get_execution_order()
                    if isinstance(order, list):
                        print("Execution order:", " -> ".join(order))
                    else:
                        print(order)  # Print error message
                case "4":
                    print("Exiting...")
                    break
                case _:
                    print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")
            continue
