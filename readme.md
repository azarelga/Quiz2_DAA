# Task Scheduler with Streamlit UI

This project implements a task scheduler using a Directed Acyclic Graph (DAG) and provides a web-based user interface built with Streamlit to interact with it.

## Features

* Add tasks to the scheduler.
* Define dependencies between tasks (i.e., specify which task must be completed before another can start).
* Calculate and display the valid execution order of tasks based on their dependencies.
* Detects and reports errors such as cycles in dependencies.

## Implementation

The core task scheduling logic is in `DAG.py`, which uses Kahn's algorithm for topological sorting.
The Streamlit UI is defined in `app.py`.

## Setup and Usage

1. **Clone this repository (if you haven't already):**

    ```bash
    git clone https://github.com/azarelga/quiz2_daa 
    cd quiz2_daa
    ```

2. **Create and activate a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    Make sure you have Python 3.7+ installed.

    ```bash
    pip install streamlit
    ```

4. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

    This will open the application in your web browser.

## How to Use the UI

* **Add Task:** Enter a unique task name in the "Add New Task" section and click "Add Task".
* **Add Dependency:** Enter the prerequisite task name and the dependent task name in the "Add Dependency" section. Click "Add Dependency".
* **Get Execution Order:** Click the "Get Execution Order" button to see the sequence in which tasks should be performed. Results or any errors will be displayed below.
