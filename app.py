import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Learning Progress Tracker",
    page_icon="📚",
    layout="wide"
)

def load_roadmap_data(file_path="attached_assets/Untitled_1761631078778.json"):
    """
    Load career roadmap data from JSON file.
    This function can be easily modified to load from different sources (CSV, API, database).
    
    Args:
        file_path: Path to the JSON file containing career roadmaps
    
    Returns:
        List of career dictionaries with roadmap data
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"Data file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        st.error("Error reading JSON file. Please check the file format.")
        return []


def initialize_session_state():
    """
    Initialize session state variables for tracking progress.
    Session state persists data across reruns during the same browser session.
    """
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {}
    
    if 'selected_career' not in st.session_state:
        st.session_state.selected_career = None
    
    if 'selected_level' not in st.session_state:
        st.session_state.selected_level = "Beginner"


def get_task_key(career, level, task_index):
    """
    Generate unique key for each task to track progress.
    
    Args:
        career: Career name
        level: Learning level (Beginner/Intermediate/Advanced)
        task_index: Index of the task in the list
    
    Returns:
        Unique string key for the task
    """
    return f"{career}_{level}_{task_index}"


def get_task_status(career, level, task_index):
    """
    Get the current status of a task.
    
    Args:
        career: Career name
        level: Learning level
        task_index: Index of the task
    
    Returns:
        Status string: "Not Started", "In Progress", or "Completed"
    """
    task_key = get_task_key(career, level, task_index)
    return st.session_state.progress_data.get(task_key, "Not Started")


def update_task_status(career, level, task_index, status):
    """
    Update the status of a specific task.
    
    Args:
        career: Career name
        level: Learning level
        task_index: Index of the task
        status: New status to set
    """
    task_key = get_task_key(career, level, task_index)
    st.session_state.progress_data[task_key] = status


def calculate_progress(career, level, tasks):
    """
    Calculate completion percentage for the current level.
    
    Args:
        career: Career name
        level: Learning level
        tasks: List of tasks for this level
    
    Returns:
        Tuple of (completed_count, total_count, percentage)
    """
    if not tasks:
        return 0, 0, 0
    
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for i in range(total_tasks)
        if get_task_status(career, level, i) == "Completed"
    )
    
    percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    return completed_tasks, total_tasks, percentage


def get_status_color(status):
    """
    Return color coding for different status types.
    
    Args:
        status: Task status string
    
    Returns:
        Color name for the status
    """
    colors = {
        "Not Started": "#E8E8E8",
        "In Progress": "#FFA500",
        "Completed": "#4CAF50"
    }
    return colors.get(status, "#E8E8E8")


def display_header():
    """Display the app header with title and description."""
    st.title("📚 Learning Progress Tracker")
    st.markdown("""
    Track your learning journey across different career paths and skill levels.
    Select your career, choose your level, and manage your progress through each task.
    """)
    st.divider()


def display_career_selector(roadmap_data):
    """
    Display career selection dropdown.
    
    Args:
        roadmap_data: List of career dictionaries
    
    Returns:
        Selected career dictionary or None
    """
    if not roadmap_data:
        st.warning("No career data available. Please check your data source.")
        return None
    
    career_names = [career['career'] for career in roadmap_data]
    
    selected_career_name = st.selectbox(
        "🎯 Select Your Career Path",
        options=career_names,
        help="Choose the career path you want to track"
    )
    
    selected_career = next(
        (career for career in roadmap_data if career['career'] == selected_career_name),
        None
    )
    
    if selected_career:
        st.session_state.selected_career = selected_career_name
        
        with st.expander("📋 Career Details"):
            st.markdown(f"**Required Skills:** {', '.join(selected_career['required_skills'])}")
            st.markdown(f"**Interest Tags:** {', '.join(selected_career['interest_tags'])}")
    
    return selected_career


def display_level_selector():
    """
    Display level selection with tabs.
    
    Returns:
        Selected level string
    """
    levels = ["Beginner", "Intermediate", "Advanced"]
    
    st.markdown("### 📊 Select Your Learning Level")
    
    cols = st.columns(3)
    
    for idx, level in enumerate(levels):
        with cols[idx]:
            if st.button(
                level,
                key=f"level_{level}",
                use_container_width=True,
                type="primary" if st.session_state.selected_level == level else "secondary"
            ):
                st.session_state.selected_level = level
                st.rerun()
    
    return st.session_state.selected_level


def display_progress_bar(career, level, tasks):
    """
    Display visual progress bar and statistics.
    
    Args:
        career: Career name
        level: Learning level
        tasks: List of tasks
    """
    completed, total, percentage = calculate_progress(career, level, tasks)
    
    st.markdown(f"### 🎯 {level} Level Progress")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.progress(percentage / 100)
    
    with col2:
        st.metric("Completed", f"{completed}/{total}")
    
    with col3:
        st.metric("Progress", f"{percentage:.0f}%")
    
    st.divider()


def display_tasks(career, level, tasks):
    """
    Display tasks with status tracking for the selected level.
    
    Args:
        career: Career name
        level: Learning level
        tasks: List of tasks to display
    """
    if not tasks:
        st.info(f"No tasks available for {level} level.")
        return
    
    st.markdown("### ✅ Tasks")
    
    for idx, task in enumerate(tasks):
        current_status = get_task_status(career, level, idx)
        status_color = get_status_color(current_status)
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(
                    f"""
                    <div style="
                        padding: 15px;
                        border-left: 4px solid {status_color};
                        background-color: #f8f9fa;
                        border-radius: 5px;
                        margin-bottom: 10px;
                    ">
                        <strong>Task {idx + 1}:</strong> {task}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                new_status = st.selectbox(
                    "Status",
                    options=["Not Started", "In Progress", "Completed"],
                    index=["Not Started", "In Progress", "Completed"].index(current_status),
                    key=f"status_{career}_{level}_{idx}",
                    label_visibility="collapsed"
                )
                
                if new_status != current_status:
                    update_task_status(career, level, idx, new_status)
                    st.rerun()


def display_resources(resources):
    """
    Display learning resources for the selected career.
    
    Args:
        resources: List of resource strings
    """
    if resources:
        with st.expander("📚 Recommended Resources"):
            for resource in resources:
                st.markdown(f"- {resource}")


def display_footer():
    """Display footer with helpful information."""
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p><strong>💡 Tips:</strong></p>
        <ul style="list-style: none; padding: 0;">
            <li>✓ Update task status as you progress through your learning journey</li>
            <li>✓ Your progress is saved during this session</li>
            <li>✓ Use the status dropdown to mark tasks as "In Progress" or "Completed"</li>
            <li>✓ Track your completion percentage at the top of each level</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def main():
    """
    Main application function.
    This orchestrates all components of the Learning Progress Tracker.
    """
    initialize_session_state()
    
    roadmap_data = load_roadmap_data()
    
    display_header()
    
    selected_career = display_career_selector(roadmap_data)
    
    if selected_career:
        st.markdown("---")
        
        selected_level = display_level_selector()
        
        st.markdown("---")
        
        tasks = selected_career['roadmap'].get(selected_level, [])
        
        display_progress_bar(
            selected_career['career'],
            selected_level,
            tasks
        )
        
        display_tasks(
            selected_career['career'],
            selected_level,
            tasks
        )
        
        st.markdown("---")
        
        display_resources(selected_career.get('resources', []))
        
        display_footer()


if __name__ == "__main__":
    main()
