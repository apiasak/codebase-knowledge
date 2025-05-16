# Technical Context: Streamlit GUI for Codebase-to-Tutorial AI

## 1. Technologies Used
- **Primary Language**: Python (version 3.x)
- **Framework**: Streamlit
    - For building the user interface (input forms, buttons, output display).
- **Subprocess Management**: Python's `subprocess` module
    - For executing the `main.py` script as a separate process.
    - For capturing its `stdout` and `stderr`.
- **File System Operations**: Python's `os` module (e.g., `os.path.expanduser` for tilde expansion).
- **Development Environment**: Standard Python development setup.
- **Version Control**: Git (assumed).

## 2. Development Setup
- A Python environment with Streamlit installed (`pip install streamlit`).
- The existing `main.py` script and its dependencies (as per `requirements.txt`).
- A new Python script file, likely `streamlit_app.py`, will contain the Streamlit GUI code.
- The GUI application will be run from the command line using `streamlit run streamlit_app.py`.
- The `main.py` script will be invoked by `streamlit_app.py`.

## 3. Technical Constraints
- The Streamlit app must be able to construct and execute CLI commands.
- Handling of potentially long-running processes (`main.py`) and displaying their output in a non-blocking way in Streamlit is a key challenge. This might involve asynchronous programming patterns or threading if Streamlit's native handling isn't sufficient for real-time output.
- Ensuring robust error handling and display from the `main.py` script.
- Cross-platform compatibility for path handling and command execution (though primary development is on macOS as per system info).

## 4. Dependencies
- `streamlit`: The core dependency for the GUI.
- Dependencies of `main.py` (as listed in `requirements.txt` of the project).
- Python standard libraries: `subprocess`, `os`, `shlex` (for command parsing/construction).
