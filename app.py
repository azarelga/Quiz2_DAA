import streamlit as st
from DAG import TaskSchedulerDAG

# Initialize TaskSchedulerDAG and session state for input values and flags
if "scheduler" not in st.session_state:
    st.session_state.scheduler = TaskSchedulerDAG()
    st.session_state.new_task_name_value = ""
    st.session_state.prerequisite_task_value = ""
    st.session_state.dependent_task_value = ""
    # st.session_state.execution_display_value = "" # Not changing this for now
    # Flags to signal clearing
    st.session_state.clear_new_task_input = False
    st.session_state.clear_dependency_inputs = False

# Initialize execution_display separately if not covered above
if "execution_display" not in st.session_state:
    st.session_state.execution_display = ""

# Process Clearing Flags Before Widget Instantiation
if st.session_state.clear_new_task_input:
    st.session_state.new_task_name_value = ""
    st.session_state.clear_new_task_input = False  # Reset flag

if st.session_state.clear_dependency_inputs:
    st.session_state.prerequisite_task_value = ""
    st.session_state.dependent_task_value = ""
    st.session_state.clear_dependency_inputs = False  # Reset flag

# Streamlit title
st.title("Task Scheduler UI")

# Add New Task section
st.subheader("Add New Task")
# Use new_task_name_input for reading, new_task_name_value for displaying/clearing
st.text_input(
    "Task Name", key="new_task_name_input", value=st.session_state.new_task_name_value
)

if st.button("Add Task", key="add_task_button"):
    task_name_to_add = (
        st.session_state.new_task_name_input
    )  # Read from widget's current state
    if task_name_to_add:  # Check if the string is not empty
        st.session_state.scheduler.add_task(task_name_to_add)
        st.success(f"Task '{task_name_to_add}' added.")
        st.session_state.clear_new_task_input = True  # Signal to clear on next rerun
    else:
        st.warning("Task name cannot be empty.")

# Add Dependency section
st.subheader("Add Dependency")
# Use _input for reading, _value for displaying/clearing
st.text_input(
    "Prerequisite Task",
    key="prerequisite_task_input",
    value=st.session_state.prerequisite_task_value,
)
st.text_input(
    "Dependent Task",
    key="dependent_task_input",
    value=st.session_state.dependent_task_value,
)

if st.button("Add Dependency", key="add_dependency_button"):
    prereq_task = st.session_state.prerequisite_task_input
    depend_task = st.session_state.dependent_task_input
    if prereq_task and depend_task:
        try:
            st.session_state.scheduler.add_dependency(prereq_task, depend_task)
            st.success(f"Dependency added: {prereq_task} -> {depend_task}")
            st.session_state.clear_dependency_inputs = (
                True  # Signal to clear on next rerun
            )
        except ValueError as e:
            st.error(str(e))
    else:
        st.warning("Both prerequisite and dependent task names are required.")

# Execution Order section
st.subheader("Execution Order")

if st.button("Get Execution Order", key="get_order_button"):
    result = st.session_state.scheduler.get_execution_order()
    if isinstance(result, list):
        order_str = " -> ".join(result)
        st.session_state.execution_display = order_str
        st.info(f"Execution Order: {order_str}")
    else:  # Error string
        st.session_state.execution_display = result
        st.error(result)

# The text_area's content is bound to st.session_state.execution_display by its key.
st.text_area("Execution Order/Errors", key="execution_display")
