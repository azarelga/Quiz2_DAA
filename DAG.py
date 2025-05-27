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

        # Check for cycles (if dependent_task already has prerequisite_task as a dependency)
        for neighbor in self.graph[dependent_task]:
            if (neighbor == prerequisite_task) or (
                prerequisite_task in self.graph[neighbor]
            ):
                raise ValueError(
                    f"Cannot add dependency: {dependent_task} already depends on {prerequisite_task}, which creates a cycle."
                )

        # Add the edge
        self.graph[prerequisite_task].append(dependent_task)
        # Increment in-degree of the dependent task
        self.in_degree[dependent_task] += 1

    def get_execution_order(self):
        # Implements Kahn's algorithm for topological sort
        queue = [task for task in self.in_degree if self.in_degree[task] == 0]
        execution_order = []

        while queue:
            current_task = queue.pop(0)
            execution_order.append(current_task)

            for neighbor_task in self.graph[current_task]:
                self.in_degree[neighbor_task] -= 1
                if self.in_degree[neighbor_task] == 0:
                    queue.append(neighbor_task)

        if len(execution_order) == len(self.graph):
            return execution_order
        else:
            return "Error: Cycle detected or graph not fully processed."  # Cycle exists


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
