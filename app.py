import streamlit as st
import json

st.set_page_config(
    page_title="Learning Progress Tracker",
    page_icon="📊",
    layout="wide"
)

def load_roadmap_data(file_path="attached_assets/Untitled_1761631078778.json"):
    """
    Load career roadmap data from JSON file.
    
    INTEGRATION NOTE: In the integrated version, this will be replaced by
    data passed from the roadmap page via set_tracker_data() function.
    
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
    
    Session state structure:
    - progress_data: Dict mapping task keys to status
    - tracker_career: Career set by roadmap page (or None for standalone)
    - tracker_level: Level set by roadmap page (or None for standalone)
    - tracker_tasks: Tasks set by roadmap page (or None for standalone)
    - standalone_mode: Boolean indicating if running in standalone mode
    """
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {}
    
    if 'tracker_career' not in st.session_state:
        st.session_state.tracker_career = None
    
    if 'tracker_level' not in st.session_state:
        st.session_state.tracker_level = None
    
    if 'tracker_tasks' not in st.session_state:
        st.session_state.tracker_tasks = None
    
    if 'standalone_mode' not in st.session_state:
        st.session_state.standalone_mode = True


def set_tracker_data(career, level, tasks):
    """
    PUBLIC API: Set the career, level, and tasks for the tracker.
    
    This function is called by the roadmap page to configure the tracker
    with the selected career path, level, and corresponding tasks.
    
    Args:
        career: String - Career name (e.g., "Data Scientist")
        level: String - Learning level ("Beginner", "Intermediate", or "Advanced")
        tasks: List[str] - List of task descriptions for this career/level
    
    Example usage from roadmap page:
        import streamlit as st
        from app import set_tracker_data
        
        set_tracker_data(
            career="Data Scientist",
            level="Beginner",
            tasks=["Learn Python basics", "Study statistics", ...]
        )
    """
    st.session_state.tracker_career = career
    st.session_state.tracker_level = level
    st.session_state.tracker_tasks = tasks
    st.session_state.standalone_mode = False


def get_tracker_data():
    """
    Get the current tracker configuration.
    
    Returns:
        Tuple of (career, level, tasks) or (None, None, None) if not configured
    """
    return (
        st.session_state.tracker_career,
        st.session_state.tracker_level,
        st.session_state.tracker_tasks
    )


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
        status: New status to set ("Not Started", "In Progress", or "Completed")
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
        Tuple of (completed_count, in_progress_count, total_count, percentage)
    """
    if not tasks:
        return 0, 0, 0, 0
    
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for i in range(total_tasks)
        if get_task_status(career, level, i) == "Completed"
    )
    
    in_progress_tasks = sum(
        1 for i in range(total_tasks)
        if get_task_status(career, level, i) == "In Progress"
    )
    
    percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    return completed_tasks, in_progress_tasks, total_tasks, percentage


def get_status_color(status):
    """
    Return color coding for different status types.
    
    Args:
        status: Task status string
    
    Returns:
        Color hex code for the status
    """
    colors = {
        "Not Started": "#E8E8E8",
        "In Progress": "#FFA500",
        "Completed": "#4CAF50"
    }
    return colors.get(status, "#E8E8E8")


def get_status_emoji(status):
    """
    Return emoji for different status types.
    
    Args:
        status: Task status string
    
    Returns:
        Emoji string for the status
    """
    emojis = {
        "Not Started": "⚪",
        "In Progress": "🟡",
        "Completed": "✅"
    }
    return emojis.get(status, "⚪")


def render_standalone_selector(roadmap_data):
    """
    STANDALONE MODE ONLY: Render sidebar selectors for testing.
    
    This function is only used when the tracker runs in standalone mode.
    In integrated mode (when data is set via set_tracker_data()), 
    this function is not called.
    
    Args:
        roadmap_data: List of career dictionaries
    
    Returns:
        Tuple of (career_name, level, tasks) or (None, None, None)
    """
    with st.sidebar:
        st.markdown("### ⚙️ Standalone Mode")
        st.caption("⚠️ This sidebar is for testing only. It will not appear when integrated with the roadmap page.")
        
        if not roadmap_data:
            st.error("No career data available")
            return None, None, None
        
        career_names = [career['career'] for career in roadmap_data]
        
        selected_career_name = st.selectbox(
            "Career Path",
            options=career_names,
            key="standalone_career"
        )
        
        selected_level = st.selectbox(
            "Learning Level",
            options=["Beginner", "Intermediate", "Advanced"],
            key="standalone_level"
        )
        
        selected_career = next(
            (career for career in roadmap_data if career['career'] == selected_career_name),
            None
        )
        
        if selected_career:
            tasks = selected_career['roadmap'].get(selected_level, [])
            return selected_career_name, selected_level, tasks
        
        return None, None, None


def display_progress_overview(career, level, tasks):
    """
    Display overall progress statistics and visual progress bar.
    
    Args:
        career: Career name
        level: Learning level
        tasks: List of tasks
    """
    completed, in_progress, total, percentage = calculate_progress(career, level, tasks)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Tasks",
            value=total
        )
    
    with col2:
        st.metric(
            label="✅ Completed",
            value=completed,
            delta=f"{percentage:.0f}%"
        )
    
    with col3:
        st.metric(
            label="🟡 In Progress",
            value=in_progress
        )
    
    with col4:
        st.metric(
            label="⚪ Not Started",
            value=total - completed - in_progress
        )
    
    st.markdown("### Progress Overview")
    st.progress(percentage / 100, text=f"{percentage:.1f}% Complete")
    
    st.divider()


def on_status_change_callback(career, level, idx):
    """
    Callback function for status selectbox changes.
    This ensures the status update happens before the rerun.
    
    Args:
        career: Career name
        level: Learning level
        idx: Task index
    """
    key = f"status_{career}_{level}_{idx}"
    new_status = st.session_state[key]
    update_task_status(career, level, idx, new_status)


def display_task_list(career, level, tasks):
    """
    Display the main task tracking interface.
    Shows all tasks with their current status and allows status updates.
    
    Args:
        career: Career name
        level: Learning level
        tasks: List of tasks to display and track
    """
    if not tasks:
        st.info(f"No tasks available for {level} level.")
        return
    
    st.markdown("### 📋 Task Progress")
    
    for idx, task in enumerate(tasks):
        current_status = get_task_status(career, level, idx)
        status_color = get_status_color(current_status)
        status_emoji = get_status_emoji(current_status)
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(
                    f"""
                    <div style="
                        padding: 18px;
                        border-left: 5px solid {status_color};
                        background-color: #f8f9fa;
                        border-radius: 8px;
                        margin-bottom: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    ">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 20px;">{status_emoji}</span>
                            <div>
                                <span style="color: #666; font-size: 14px;">Task {idx + 1}</span>
                                <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;">{task}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.selectbox(
                    "Status",
                    options=["Not Started", "In Progress", "Completed"],
                    index=["Not Started", "In Progress", "Completed"].index(current_status),
                    key=f"status_{career}_{level}_{idx}",
                    label_visibility="collapsed",
                    on_change=on_status_change_callback,
                    args=(career, level, idx)
                )


def display_status_legend():
    """
    Display a legend explaining the status indicators.
    """
    with st.expander("ℹ️ Status Guide"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **⚪ Not Started**  
            Tasks you haven't begun yet
            """)
        
        with col2:
            st.markdown("""
            **🟡 In Progress**  
            Tasks you're currently working on
            """)
        
        with col3:
            st.markdown("""
            **✅ Completed**  
            Tasks you've finished
            """)


def render_tracker(career, level, tasks):
    """
    Render the complete tracker UI for given career, level, and tasks.
    
    This is the main rendering function that can be called from the roadmap page
    or used in standalone mode.
    
    Args:
        career: Career name
        level: Learning level
        tasks: List of tasks to track
    """
    if not career or not level or not tasks:
        st.info("👈 No tracking data available. Please configure the tracker from the roadmap page.")
        return
    
    st.markdown(f"### {career} - {level} Level")
    st.markdown("")
    
    display_progress_overview(career, level, tasks)
    display_task_list(career, level, tasks)
    
    st.divider()
    display_status_legend()


def main():
    """
    Main application function for the Learning Progress Tracker.
    
    INTEGRATION CONTRACT:
    ====================
    
    To integrate with the roadmap page, use the set_tracker_data() function:
    
    1. From the roadmap page, after user selects career and level:
       
       from app import set_tracker_data
       
       set_tracker_data(
           career="Data Scientist",
           level="Beginner",
           tasks=["Task 1", "Task 2", ...]
       )
    
    2. Then navigate to or embed this tracker page
    
    3. The tracker will automatically use the provided data and hide the sidebar
    
    STANDALONE MODE:
    ================
    
    When running independently (no data provided via set_tracker_data()),
    the tracker operates in standalone mode with a sidebar for testing.
    This allows development and testing without the roadmap page.
    """
    initialize_session_state()
    
    st.title("📊 Learning Progress Tracker")
    st.markdown("""
    Track your progress through learning tasks. Update the status of each task as you 
    work through your learning journey and visualize your overall progress.
    """)
    st.divider()
    
    career, level, tasks = get_tracker_data()
    
    if career and level and tasks:
        render_tracker(career, level, tasks)
    else:
        roadmap_data = load_roadmap_data()
        
        if roadmap_data:
            career, level, tasks = render_standalone_selector(roadmap_data)
            
            if career and level and tasks:
                render_tracker(career, level, tasks)
            else:
                st.info("👈 Please select a career path and level from the sidebar to start tracking.")
        else:
            st.error("Unable to load roadmap data. Please check the data source configuration.")


if __name__ == "__main__":
    main()
