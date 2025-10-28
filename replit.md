# Overview

This is a **Learning Progress Tracker** application built with Streamlit. The application helps users track their learning progress through tasks for different career paths and proficiency levels (Beginner, Intermediate, Advanced). The tracker provides an interactive interface for users to update task statuses (Not Started, In Progress, Completed) and visualize their overall progress with metrics and progress bars.

The application is designed to be **independent from the roadmap generation page** and can be easily integrated via a clean public API. Career selection, level selection, and resources will be handled by a separate roadmap page that will pass data to this tracker.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture

**Technology Choice: Streamlit**
- **Rationale**: Streamlit was chosen for rapid prototyping and deployment of data-driven applications with minimal frontend code
- **Approach**: Uses Streamlit's declarative Python API to build the user interface
- **Configuration**: Wide layout mode with custom page title and icon for better UX
- **State Management**: Utilizes Streamlit's `session_state` to persist user progress data across page reruns during a browser session

## Operation Modes

**Standalone Mode (Development/Testing)**
- Displays a sidebar with career and level selectors for independent testing
- Loads data from local JSON file (attached_assets/Untitled_1761631078778.json)
- Clearly marked as temporary with warning messages
- Automatically enabled when no external data is provided

**Integrated Mode (Production)**
- Receives career, level, and tasks from roadmap page via `set_tracker_data()` API
- Sidebar is hidden when external data is provided
- Designed to be embedded in multi-page Streamlit applications

## Integration Contract

**Public API**
```python
set_tracker_data(career, level, tasks)
```

**Parameters:**
- `career` (str): Career name (e.g., "Data Scientist")
- `level` (str): Learning level ("Beginner", "Intermediate", or "Advanced")
- `tasks` (list[str]): List of task descriptions for the selected career and level

**Usage from Roadmap Page:**
```python
from app import set_tracker_data

# After user selects career and level on roadmap page
set_tracker_data(
    career="Data Scientist",
    level="Beginner",
    tasks=["Task 1", "Task 2", "Task 3", ...]
)
# Then navigate to or render the tracker page
```

## Data Architecture

**Data Format**
- Structured JSON containing career objects with roadmaps organized by proficiency levels
- **Schema Structure**:
  - Career metadata: name, required skills, interest tags
  - Roadmap: nested dictionary with proficiency levels as keys and task lists as values
  - Resources: array of learning resources (handled by roadmap page, not tracker)

**Data Flow**
1. **Standalone Mode**: Data loaded from JSON file on disk
2. **Integrated Mode**: Data passed via `set_tracker_data()` function from roadmap page

## Progress Tracking System

**Session State Variables**
- `progress_data`: Dictionary mapping unique task keys to status values
- `tracker_career`: Career name set by roadmap page (or None in standalone)
- `tracker_level`: Level set by roadmap page (or None in standalone)
- `tracker_tasks`: Task list set by roadmap page (or None in standalone)
- `standalone_mode`: Boolean flag indicating operating mode

**Task Identification**
- Unique keys generated as: `"{career}_{level}_{task_index}"`
- Enables independent progress tracking for each career-level combination
- Progress persists across sessions within the same browser session

**Status Values**
- "Not Started" (⚪ gray indicator)
- "In Progress" (🟡 orange indicator)
- "Completed" (✅ green indicator)

## Error Handling

**File Loading Strategy**
- Implements try-except blocks for robust file operations
- Provides user-friendly error messages through Streamlit's error display system
- Handles both FileNotFoundError and JSONDecodeError scenarios gracefully

**Graceful Degradation**
- Shows informative message when no data is available
- Handles empty task lists without crashing
- Validates data before rendering

## Design Patterns

**Modular Function Design**
- **Data Loading**: `load_roadmap_data()`, `set_tracker_data()`, `get_tracker_data()`
- **Progress Management**: `get_task_status()`, `update_task_status()`, `calculate_progress()`
- **UI Rendering**: `render_tracker()`, `display_progress_overview()`, `display_task_list()`
- **Status Updates**: Callback-based approach using `on_status_change_callback()` to ensure reliable state persistence

**Callback-Based State Updates**
- Status selectbox uses `on_change` callback parameter
- Ensures status updates happen before page rerun
- Prevents race conditions and guarantees data persistence
- Updates trigger automatic page rerun with refreshed metrics

**Separation of Concerns**
- Clear separation between standalone testing UI and core tracker functionality
- Public API clearly documented for integration
- Modular code structure facilitates maintenance and testing

# Technical Implementation Details

## Recent Changes (October 2025)

**Bug Fix: Status Update Persistence**
- Implemented callback-based status updates to fix race condition
- Changed from checking status changes after render to using `on_change` callback
- Ensures session state updates complete before page rerun
- All status changes now persist reliably

**Architecture Refactoring**
- Created clear separation between standalone mode and integrated mode
- Implemented `set_tracker_data()` public API for roadmap page integration
- Removed career details and resources display (now handled by roadmap page)
- Added conditional sidebar rendering based on operating mode

## UI Components

**Main Page**
1. Title and description
2. Career and level heading (e.g., "Data Scientist - Beginner Level")
3. **Progress Overview**: 4 metrics displayed as cards
   - Total Tasks
   - Completed (with percentage delta)
   - In Progress
   - Not Started
4. Progress bar with percentage text
5. **Task List**: Each task shows:
   - Task number and description
   - Color-coded left border (gray/orange/green)
   - Status emoji (⚪/🟡/✅)
   - Status dropdown selector
6. Status legend (expandable)

**Sidebar (Standalone Mode Only)**
- Warning message about testing-only purpose
- Career Path dropdown
- Learning Level dropdown

## Performance Considerations

- Session state used for efficient progress tracking without database calls
- Minimal reruns through callback-based updates
- Efficient progress calculation with single pass over tasks
- Lightweight UI rendering with HTML/CSS styling

# External Dependencies

## Core Framework
- **Streamlit**: Web application framework for building the interactive UI and handling user interactions
- **Python 3.11**: Runtime environment

## Data Processing
- **json** (Python standard library): Parsing and loading career roadmap data from JSON files

## Future Integration Points

**Next Steps for Production Integration:**
1. Roadmap page will call `set_tracker_data()` after user selects career and level
2. Remove standalone mode sidebar from production builds
3. Add lightweight integration tests for cross-page data handoff
4. Document tracker API expectations in shared documentation
5. Consider persistent storage (database) for progress across sessions and users

**Potential Enhancements:**
- Database integration for persistent progress storage
- User authentication to track individual user progress
- Progress history and analytics dashboard
- Export functionality for progress reports
- Task notes and completion timestamps
