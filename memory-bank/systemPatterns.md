# System Patterns: Streamlit GUI for Codebase-to-Tutorial AI

## 1. System Architecture
- **Two-Process Architecture**:
    - **Process 1 (GUI)**: The Streamlit application (`streamlit_app.py`) acting as the user interface and command orchestrator.
    - **Process 2 (Worker)**: The `main.py` script, launched as a subprocess by the Streamlit app, performing the actual codebase analysis and tutorial generation.
- **User Interface (UI)**: Handled by Streamlit components, providing forms for argument input and areas for displaying output from `main.py`.
- **Logic**:
    - **GUI Logic (`streamlit_app.py`)**:
        - Rendering input widgets.
        - Collecting and validating user-provided arguments.
        - Constructing the `python main.py` command string.
        - Launching `main.py` using `subprocess.Popen`.
        - Capturing and displaying `stdout`/`stderr` from `main.py` (potentially streaming).
    - **Core Logic (`main.py`)**: Unchanged; performs codebase analysis and tutorial generation as per its existing functionality.
- **Data Flow**:
    1. User configures parameters in the Streamlit UI.
    2. On "Generate" action, `streamlit_app.py` collects these parameters.
    3. `streamlit_app.py` constructs the command and launches `main.py` as a subprocess.
    4. `main.py` executes, reading from the specified codebase and writing tutorial files to the output directory.
    5. `main.py`'s `stdout` and `stderr` are piped back to `streamlit_app.py`.
    6. `streamlit_app.py` displays this output to the user.

## 2. Key Technical Decisions
- **GUI Framework**: Streamlit, for rapid UI development.
- **Process Invocation**: `subprocess.Popen` for launching `main.py` non-blockingly, allowing the Streamlit app to remain responsive and potentially stream output.
- **Command Construction**: Use of `shlex` to ensure arguments are correctly quoted and formatted for the subprocess.
- **Path Handling**: `os.path.expanduser` for tilde expansion.

## 3. Design Patterns in Use
- **Frontend-Backend (Loose Analogy)**: Streamlit app as the frontend, `main.py` as the backend processing engine.
- **Process Orchestration**: The Streamlit app orchestrates the execution of `main.py`.
- **Event-Driven**: UI interactions (button clicks, input changes) drive the application's behavior.

## 4. Component Relationships
- **Streamlit Input Widgets**: `st.text_input`, `st.text_area`, `st.number_input`, `st.checkbox`, `st.radio`, `st.selectbox`, `st.file_uploader` (if direct file handling becomes part of `main.py`'s capability via GUI).
- **Streamlit Output Widgets**: `st.text_area`, `st.code`, `st.markdown`, `st.empty` (for dynamic updates) to display `main.py` output.
- **Button (`st.button`)**: To trigger the execution of `main.py`.
- **`subprocess.Popen`**: To manage the lifecycle of the `main.py` process.
- **`main.py`**: The core script being wrapped by the GUI.
