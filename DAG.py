class TaskSchedulerDAG:
    def __init__(self):
        self.graph = {}  
        self.in_degree = {} 

    def add_task(self, task_name):
        if task_name not in self.graph:
            self.graph[task_name] = []
            self.in_degree[task_name] = 0

    def add_dependency(self, prerequisite_task, dependent_task):
        self.add_task(prerequisite_task)
        self.add_task(dependent_task)

        self.graph[prerequisite_task].append(dependent_task)
        self.in_degree[dependent_task] += 1

    def get_execution_order(self): # topo sort
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
            return "Error: Cycle detected or graph not fully processed." 

# contoh
scheduler = TaskSchedulerDAG()

# Define tasks and their dependencies
scheduler.add_task("Wake up")
scheduler.add_task("Make Coffee")
scheduler.add_task("Drink Coffee")
scheduler.add_task("Eat Breakfast")
scheduler.add_task("Go to Work")

scheduler.add_dependency("Wake up", "Make Coffee")
scheduler.add_dependency("Wake up", "Eat Breakfast")
scheduler.add_dependency("Make Coffee", "Drink Coffee")
scheduler.add_dependency("Drink Coffee", "Go to Work")
scheduler.add_dependency("Eat Breakfast", "Go to Work")

# contoh cycle
# scheduler.add_dependency("Go to Work", "Wake up") 

order = scheduler.get_execution_order()

if isinstance(order, list):
    print("A valid order to complete tasks:")
    for i, task in enumerate(order):
        print(f"{i+1}. {task}")
else:
    print(order) 
