# Overview

This is a **Learning Progress Tracker** application built with Streamlit. The application helps users track their learning journey across different career paths by displaying structured roadmaps with beginner, intermediate, and advanced learning stages. The system loads career roadmap data from JSON files and provides an interactive interface for users to monitor their progress through various skill development stages.

The application is designed to eventually integrate with a roadmap generation page, where career paths and proficiency levels will be dynamically selected and passed to the tracker interface.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture

**Technology Choice: Streamlit**
- **Rationale**: Streamlit was chosen for rapid prototyping and deployment of data-driven applications with minimal frontend code
- **Approach**: Uses Streamlit's declarative Python API to build the user interface
- **Configuration**: Wide layout mode with custom page title and icon for better UX
- **State Management**: Utilizes Streamlit's `session_state` to persist user progress data, selected career, and proficiency level across page reruns during a browser session

## Data Architecture

**Current Implementation: File-based JSON storage**
- **Data Format**: Structured JSON containing career objects with roadmaps organized by proficiency levels (Beginner, Intermediate, Advanced)
- **Schema Structure**:
  - Career metadata: name, required skills, interest tags
  - Roadmap: nested dictionary with proficiency levels as keys and task lists as values
  - Resources: array of learning resources and references
- **Future Integration**: Designed to be replaced by data passed from a roadmap generation page or external data sources (CSV, API, database)

## Error Handling

**File Loading Strategy**
- Implements try-except blocks for robust file operations
- Provides user-friendly error messages through Streamlit's error display system
- Handles both FileNotFoundError and JSONDecodeError scenarios gracefully

## Design Patterns

**Modular Function Design**
- Separation of concerns: data loading, state initialization, and UI rendering are separated into distinct functions
- Functions include comprehensive docstrings for future maintainability
- Code is structured to facilitate easy migration from file-based to dynamic data sources

**Session State Pattern**
- Three primary state variables: `progress_data` (tracks completion), `selected_career` (current career path), `selected_level` (proficiency level)
- Initialization guards prevent state overwrites on reruns
- Designed for future integration with multi-page navigation

# External Dependencies

## Core Framework
- **Streamlit**: Web application framework for building the interactive UI and handling user interactions

## Data Processing
- **json** (Python standard library): Parsing and loading career roadmap data from JSON files

## Future Integration Points
- Roadmap generation page (planned): Will provide dynamic career selection and level assignment
- Potential database integration (planned): Migration path from file-based to database-driven storage
- External APIs (planned): Career data and learning resources could be fetched from external sources