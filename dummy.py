from DAG import TaskSchedulerDAG
import random


def create_software_development_project():
    """Create a realistic software development project scenario"""
    scheduler = TaskSchedulerDAG()

    # Add all tasks
    tasks = [
        "Requirements Analysis",
        "System Design",
        "Database Design",
        "UI/UX Design",
        "Frontend Setup",
        "Backend Setup",
        "API Development",
        "Database Implementation",
        "User Authentication",
        "Core Features Development",
        "Frontend Implementation",
        "API Integration",
        "Testing Framework Setup",
        "Unit Tests",
        "Integration Tests",
        "UI Testing",
        "Performance Testing",
        "Security Review",
        "Documentation",
        "Code Review",
        "Bug Fixes",
        "Deployment Setup",
        "Production Deployment",
        "User Training",
        "Go Live",
    ]

    for task in tasks:
        scheduler.add_task(task)

    # Add realistic dependencies
    dependencies = [
        ("Requirements Analysis", "System Design"),
        ("Requirements Analysis", "UI/UX Design"),
        ("System Design", "Database Design"),
        ("System Design", "API Development"),
        ("Database Design", "Database Implementation"),
        ("UI/UX Design", "Frontend Setup"),
        ("Frontend Setup", "Frontend Implementation"),
        ("Backend Setup", "API Development"),
        ("API Development", "User Authentication"),
        ("Database Implementation", "User Authentication"),
        ("User Authentication", "Core Features Development"),
        ("Core Features Development", "API Integration"),
        ("Frontend Implementation", "API Integration"),
        ("API Integration", "Testing Framework Setup"),
        ("Testing Framework Setup", "Unit Tests"),
        ("Testing Framework Setup", "Integration Tests"),
        ("Frontend Implementation", "UI Testing"),
        ("Unit Tests", "Performance Testing"),
        ("Integration Tests", "Performance Testing"),
        ("Core Features Development", "Security Review"),
        ("Performance Testing", "Code Review"),
        ("Security Review", "Code Review"),
        ("Code Review", "Documentation"),
        ("Documentation", "Bug Fixes"),
        ("Bug Fixes", "Deployment Setup"),
        ("Deployment Setup", "Production Deployment"),
        ("Production Deployment", "User Training"),
        ("User Training", "Go Live"),
    ]

    for prereq, dependent in dependencies:
        scheduler.add_dependency(prereq, dependent)

    return scheduler


def load_dummy_data_into_session(scenario_name="software"):
    """Load dummy data into Streamlit session state"""
    scenarios = {
        "software": create_software_development_project,
    }

    if scenario_name in scenarios:
        return scenarios[scenario_name]()
    else:
        return create_software_development_project()
