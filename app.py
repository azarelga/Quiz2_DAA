import streamlit as st
from DAG import TaskSchedulerDAG
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx

# 1. Page Config (MUST be first st command)
st.set_page_config(
    page_title="Task Scheduler DAG",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Custom CSS for enhanced styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    border: 1px solid #e1e5e9;
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 1rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #2d3748;
    margin: 0;
}

.metric-label {
    font-size: 0.9rem;
    color: #718096;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.success-alert {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.error-alert {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.task-item {
    background: #f8f9fa;
    padding: 0.75rem 1rem;
    margin: 0.25rem 0;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    font-weight: 500;
}

.stButton > button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.sidebar .stSelectbox > div > div {
    background-color: #f8f9fa;
}
</style>
""",
    unsafe_allow_html=True,
)

# Initialize TaskSchedulerDAG and session state
if "scheduler" not in st.session_state:
    st.session_state.scheduler = TaskSchedulerDAG()

    # COMMENT THESE LINES IF YOU DONT WANT TO USE DUMMY DATA
    # ------ #
    from dummy import load_dummy_data_into_session

    st.session_state.scheduler = load_dummy_data_into_session()
    # ------ #

    st.session_state.new_task_name_value = ""
    st.session_state.prerequisite_task_value = ""
    st.session_state.dependent_task_value = ""
    st.session_state.clear_new_task_input = False
    st.session_state.clear_dependency_inputs = False
    st.session_state.execution_display = ""
    st.session_state.show_graph = False

# Process clearing flags
if st.session_state.clear_new_task_input:
    st.session_state.new_task_name_value = ""
    st.session_state.clear_new_task_input = False

if st.session_state.clear_dependency_inputs:
    st.session_state.prerequisite_task_value = ""
    st.session_state.dependent_task_value = ""
    st.session_state.clear_dependency_inputs = False

# Header
st.markdown(
    """
    <div class="main-header">
        <h1>📊 Task Scheduler DAG</h1>
        <p>Manage tasks and dependencies with intelligent scheduling</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar for controls
with st.sidebar:
    st.markdown("# 🎛️ Metrics")

    # Metrics
    tasks = list(st.session_state.scheduler.graph.keys())
    total_tasks = len(tasks)
    total_dependencies = sum(
        len(deps) for deps in st.session_state.scheduler.graph.values()
    )

    # Stack Vertically
    st.markdown(
        f"""
        <div class="metric-card">
            <p class="metric-value">{total_tasks}</p>
            <p class="metric-label">Tasks</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <p class="metric-value">{total_dependencies}</p>
            <p class="metric-label">Dependencies</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Add Task Section
    st.markdown("### ➕ Add New Task")
    new_task_name = st.text_input(
        "Task Name",
        value=st.session_state.new_task_name_value,
        placeholder="Enter task name...",
        key="new_task_input",
    )

    if st.button("Add Task", key="add_task_btn", use_container_width=True):
        if new_task_name.strip():
            if new_task_name not in st.session_state.scheduler.graph:
                st.session_state.scheduler.add_task(new_task_name)
                st.success(f"✅ Task '{new_task_name}' added successfully!")
                st.session_state.clear_new_task_input = True
                st.rerun()
            else:
                st.error(f"❌ Task '{new_task_name}' already exists!")
        else:
            st.error("❌ Task name cannot be empty!")

    st.markdown("---")

    # Add Dependency Section
    st.markdown("### 🔗 Add Dependency")

    if tasks:
        prerequisite = st.selectbox(
            "Prerequisite Task", options=[""] + tasks, index=0, key="prereq_select"
        )

        dependent = st.selectbox(
            "Dependent Task", options=[""] + tasks, index=0, key="dependent_select"
        )

        if st.button("Add Dependency", key="add_dep_btn", use_container_width=True):
            if prerequisite and dependent:
                try:
                    st.session_state.scheduler.add_dependency(
                        prerequisite, dependent)
                    st.success(
                        f"✅ Dependency added: {prerequisite} → {dependent}")
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ {str(e)}")
            else:
                st.error("❌ Please select both prerequisite and dependent tasks!")
    else:
        st.info("Add some tasks first to create dependencies")

    st.markdown("---")

    # Visualization Toggle
    st.markdown("### 📈 Visualization")
    st.session_state.show_graph = st.toggle(
        "Show Task Graph", value=st.session_state.show_graph
    )

# Main content area
if not tasks:
    st.markdown(
        """
        <div class="card">
            <h3>🚀 Get Started</h3>
            <p>Welcome to the Task Scheduler! Start by adding some tasks using the sidebar controls.</p>
            <ol>
                <li>Add tasks using the "Add New Task" section</li>
                <li>Define dependencies between tasks</li>
                <li>Get the optimal execution order</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(
        ["📋 Current Tasks", "⚡ Execution Order", "📊 Visualization"]
    )

    with tab1:
        st.markdown("### Current Tasks Overview")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(
                """
                <div class="card">
                    <h4>📝 Task List</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for task in tasks:
                dependencies = [
                    k for k, v in st.session_state.scheduler.graph.items() if task in v
                ]
                dep_text = (
                    f" (depends on: {', '.join(dependencies)})" if dependencies else ""
                )
                st.markdown(
                    f'<div class="task-item">🔹 {task}{dep_text}</div>',
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown(
                """
                <div class="card">
                    <h4>🔗 Dependencies</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            has_dependencies = False
            for task, deps in st.session_state.scheduler.graph.items():
                if deps:
                    has_dependencies = True
                    for dep in deps:
                        st.markdown(
                            f'<div class="task-item">📍 {task} → {dep}</div>',
                            unsafe_allow_html=True,
                        )

            if not has_dependencies:
                st.info("No dependencies defined yet")

    with tab2:
        st.markdown("### Execution Order Analysis")

        if st.button(
            "🚀 Calculate Execution Order", key="calc_order", use_container_width=True
        ):
            result = st.session_state.scheduler.get_execution_order()
            if isinstance(result, list):
                if result:
                    st.session_state.execution_display = " → ".join(result)

                    # Display as cards
                    st.markdown("#### Optimal Execution Sequence")
                    cols = st.columns(min(len(result), 5))
                    for i, task in enumerate(result):
                        with cols[i % 5]:
                            st.markdown(
                                f"""
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                           color: white; padding: 1rem; border-radius: 8px; text-align: center; margin: 0.5rem 0;">
                                    <div style="font-size: 0.8rem; opacity: 0.8;">Step {i + 1}</div>
                                    <div style="font-weight: 600; font-size: 1.1rem;">{task}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                else:
                    st.info("No tasks to schedule")
            else:
                st.error(f"❌ {result}")

        if st.session_state.execution_display:
            st.markdown("#### Quick Reference")
            st.code(st.session_state.execution_display, language="text")

    with tab3:
        if st.session_state.show_graph and tasks:
            st.markdown("### Task Dependency Graph")

            # Create network graph using networkx and plotly
            G = nx.DiGraph()

            # Add nodes
            for task in tasks:
                G.add_node(task)

            # Add edges
            for task, deps in st.session_state.scheduler.graph.items():
                for dep in deps:
                    G.add_edge(task, dep)

            if G.edges():
                # Calculate layout
                try:
                    pos = nx.spring_layout(G, k=3, iterations=50)
                except:
                    pos = nx.random_layout(G)

                # Create plotly figure
                fig = go.Figure()

                # Add edges with arrows
                annotations = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]

                    # Calculate arrow position (closer to target node)
                    dx = x1 - x0
                    dy = y1 - y0
                    length = (dx**2 + dy**2) ** 0.5

                    if length > 0:
                        # Adjust arrow to end before the node (accounting for node size)
                        arrow_end_x = x1 - 0.08 * (dx / length)
                        arrow_end_y = y1 - 0.08 * (dy / length)

                        # Add line
                        fig.add_trace(
                            go.Scatter(
                                x=[x0, arrow_end_x],
                                y=[y0, arrow_end_y],
                                mode="lines",
                                line=dict(color="#888", width=2),
                                hoverinfo="none",
                                showlegend=False,
                            )
                        )

                        # Add arrow annotation
                        annotations.append(
                            dict(
                                x=arrow_end_x,
                                y=arrow_end_y,
                                ax=x0,
                                ay=y0,
                                xref="x",
                                yref="y",
                                axref="x",
                                ayref="y",
                                arrowhead=2,
                                arrowsize=1.5,
                                arrowwidth=2,
                                arrowcolor="#888",
                                showarrow=True,
                            )
                        )

                # Add nodes
                node_x = [pos[node][0] for node in G.nodes()]
                node_y = [pos[node][1] for node in G.nodes()]
                node_text = list(G.nodes())

                fig.add_trace(
                    go.Scatter(
                        x=node_x,
                        y=node_y,
                        mode="markers+text",
                        text=node_text,
                        textposition="middle center",
                        textfont=dict(color="black", size=12, family="Inter"),
                        hoverinfo="text",
                        marker=dict(
                            size=60, color="gray", line=dict(width=3, color="white")
                        ),
                        showlegend=False,
                    )
                )

                fig.update_layout(
                    title="Task Dependency Visualization",
                    showlegend=False,
                    hovermode="closest",
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=annotations
                    + [
                        dict(
                            text="Arrows show task dependencies (prerequisite → dependent)",
                            showarrow=False,
                            xref="paper",
                            yref="paper",
                            x=0.005,
                            y=-0.002,
                            xanchor="left",
                            yanchor="bottom",
                            font=dict(color="#888", size=12),
                        )
                    ],
                    xaxis=dict(showgrid=False, zeroline=False,
                               showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False,
                               showticklabels=False),
                    height=600,
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add some dependencies to see the graph visualization")
        elif not st.session_state.show_graph:
            st.info("Enable 'Show Task Graph' in the sidebar to see visualization")
        else:
            st.info("Add some tasks to see visualization")
